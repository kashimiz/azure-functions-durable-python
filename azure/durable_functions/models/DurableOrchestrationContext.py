from datetime import datetime
from ..interfaces import ITaskMethods
from . import (Task, RetryOptions)


class DurableOrchestrationContext:

    def __init__(self):
        self.instanceId: str
        self.isReplaying: bool
        self.parentInstanceId: str

        # self.currentUtcDateTime: Date
        self.currentUtcDateTime: datetime
        self.Task: ITaskMethods

        def callActivity(name: str, input=None) -> Task:
            raise NotImplementedError("This is a placeholder.")

        def callActivityWithRetry(
                name: str, retryOptions: RetryOptions, input=None) -> Task:
            raise NotImplementedError("This is a placeholder.")

        def callSubOrchestrator(
                name: str, input=None, instanceId: str = None) -> Task:
            raise NotImplementedError("This is a placeholder.")

        # TODO: more to port over
