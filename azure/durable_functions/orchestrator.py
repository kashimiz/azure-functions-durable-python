import logging
import json
from typing import Callable, Iterator, List, Any, Union, Dict
from datetime import datetime
from dateutil.parser import parse as dtparse
from .interfaces import IFunctionContext, IAction
from .models.actions import CallActivityAction
from .models.history import HistoryEvent, HistoryEventType
from .models import (
    DurableOrchestrationContext,
    Task,
    TaskSet,
    OrchestratorState)


class Orchestrator:
    def __init__(self,
                 activity_func: Callable[[IFunctionContext], Iterator[Any]]):
        self.fn: Callable[[IFunctionContext], Iterator[Any]] = activity_func
        self.currentUtcDateTime: datetime = None
        self.customStatus: Any = None
        self.newGuidCounter: int = 0

    async def handle(self, context_string: str):
        context: Dict[str, Any] = json.loads(context_string)
        logging.warn(f"!!!Calling orchestrator handle {context}")
        context_histories: List[HistoryEvent] = context.get("history")
        context_input = context.get("input")
        context_instanceId = context.get("instanceId")
        context_isReplaying = context.get("isReplaying")
        context_parentInstanceId = context.get("parentInstanceId")

        decisionStartedEvent: HistoryEvent = list(filter(
            # HistoryEventType.OrchestratorStarted
            lambda e: e["EventType"] == HistoryEventType.OrchestratorStarted,
            context_histories))[0]

        self.currentUtcDateTime = dtparse(decisionStartedEvent["Timestamp"])
        self.newGuidCounter = 0

        durable_context = DurableOrchestrationContext(
            instanceId=context_instanceId,
            isReplaying=context_isReplaying,
            parentInstanceId=context_parentInstanceId,
            callActivity=lambda n, i: self.callActivity(
                state=context_histories,
                name=n,
                input=i),
            currentUtcDateTime=self.currentUtcDateTime)
        activity_context = IFunctionContext(df=durable_context)

        gen = self.fn(activity_context)
        actions: List[List[IAction]] = []
        partialResult: Union[Task, TaskSet] = None

        try:
            while True:
                gen_result = next(gen)
                logging.warn(f"!!!Generator Execution {gen_result}")
                partialResult = gen_result
                if partialResult is not None:
                    gen.send(partialResult.result)
                else:
                    gen.send(None)

                if (isinstance(partialResult, Task)
                   and hasattr(partialResult, "action")):
                    actions.append([partialResult.action])
                elif (isinstance(partialResult, TaskSet)
                      and hasattr(partialResult, "actions")):
                    actions.append(partialResult.actions)

                if self.shouldSuspend(partialResult):
                    response = OrchestratorState(
                        isDone=False,
                        output=None,
                        actions=actions,
                        customStatus=self.customStatus)
                    # TODO: Send response
                    #return response

                if (isinstance(partialResult, Task)
                   or isinstance(partialResult, TaskSet)) and (
                       partialResult.isFaulted):
                    gen.throw(partialResult.exception)
                    continue

                lastTimestamp = dtparse(decisionStartedEvent["Timestamp"])
                decisionStartedEvents = list(
                    filter(lambda e: (
                        e["EventType"] == HistoryEventType.OrchestratorStarted
                        and dtparse(e["Timestamp"]) > lastTimestamp),
                        context_histories))

                if len(decisionStartedEvents) == 0:
                    activity_context.df.currentUtcDateTime = None
                    self.currentTimestamp = None
                else:
                    decisionStartedEvent = decisionStartedEvents[0]
                    newTimestamp = dtparse(decisionStartedEvent["Timestamp"])
                    activity_context.df.currentUtcDateTime = newTimestamp
                    self.currentTimestamp = newTimestamp
        except StopIteration:
            logging.warn("!!!Generator Termination StopIteration")
            response = OrchestratorState(
                isDone=True,
                output=None,  # Should have no output, after generation range
                actions=actions,
                customStatus=self.customStatus)
            # TODO: Send response
            #return response
        except Exception as e:
            logging.warn(f"!!!Generator Termination Other Exception {e}")
            response = OrchestratorState(
                isDone=False,
                output=None,  # Should have no output, after generation range
                actions=actions,
                error=str(e),
                customStatus=self.customStatus)
            # TODO: Send response
            #return response

    def callActivity(self,
                     state: List[HistoryEvent],
                     name: str,
                     input: Any = None) -> Task:
        logging.warn(f"!!!callActivity name={name} input={input}")
        newAction = CallActivityAction(name, input)

        taskScheduled = self.findTaskScheduled(state, name)
        taskCompleted = self.findTaskCompleted(state, taskScheduled)
        taskFailed = self.findTaskFailed(state, taskScheduled)
        self.setProcessed([taskScheduled, taskCompleted, taskFailed])

        if taskCompleted is not None:
            logging.warn("!!!Task Completed")
            return Task(
                isCompleted=True,
                isFaulted=False,
                action=newAction,
                result=self.parseHistoryEvent(taskCompleted),
                timestamp=taskCompleted["Timestamp"],
                id=taskCompleted["TaskScheduledId"])

        if taskFailed is not None:
            logging.warn("!!!Task Failed")
            return Task(
                isCompleted=True,
                isFaulted=True,
                action=newAction,
                result=taskFailed["Reason"],
                timestamp=taskFailed["Timestamp"],
                id=taskFailed["TaskScheduledId"],
                exc=Exception(f"TaskFailed {taskFailed['TaskScheduledId']}")
            )

        return Task(isCompleted=False, isFaulted=False, action=newAction)

    def findTaskScheduled(self, state, name):
        if not name:
            raise ValueError("Name cannot be empty")

        tasks = list(
            filter(lambda e: e["EventType"] == HistoryEventType.TaskScheduled
                   and e["Name"] == name
                   and not e["IsProcessed"], state))

        if len(tasks) == 0:
            return None

        return tasks[0]

    def findTaskCompleted(self, state, scheduledTask):
        tasks = list(
            filter(lambda e: e["EventType"] == HistoryEventType.TaskCompleted
                   and e["TaskScheduledId"] == scheduledTask["EventId"],
                   state))

        if len(tasks) == 0:
            return None

        return tasks[0]

    def findTaskFailed(self, state, scheduledTask):
        tasks = list(
            filter(lambda e: e["EventType"] == HistoryEventType.TaskFailed
                   and e["TaskScheduledId"] == scheduledTask["EventId"],
                   state))

        if len(tasks) == 0:
            return None

        return tasks[0]

    def setProcessed(self, tasks):
        for task in tasks:
            if task:
                task["IsProcessed"] = True

    def parseHistoryEvent(self, directiveResult):
        eventType = directiveResult.get("EventType")
        if eventType is None:
            raise ValueError("EventType is not found in task object")

        if eventType == HistoryEventType.EventRaised:
            return directiveResult["Input"]
        if eventType == HistoryEventType.SubOrchestrationInstanceCreated:
            return directiveResult["Result"]
        if eventType == HistoryEventType.TaskCompleted:
            return directiveResult["Result"]
        return None

    def shouldSuspend(self, partialResult) -> bool:  #  old_name: shouldFinish
        if partialResult is None:
            return False

        if not hasattr(partialResult, "isCompleted"):
            return False

        return not partialResult.isCompleted



    @classmethod
    def create(cls, fn):
        logging.warn("!!!Calling orchestrator create")
        return lambda context: Orchestrator(fn).handle(context)
