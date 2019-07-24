from typing import Callable, Iterator, Any
from datetime import datetime
from .interfaces import IFunctionContext

class Orchestrator:
    def __init__(self,
            activity_func: Callable[[IFunctionContext], Iterator[Any]]):
        self.fn : Callable[[IFunctionContext], Iterator[Any]] = activity_func
        self.currentUtcDateTime: datetime
        self.customStatus: Any
        self.newGuidCounter: int

    async def handle(context: IFunctionContext):
        state: List[HistoryEvent] = context.bindings.history
        input: Any = context.bindings.input
        instanceId: str = context.bindings.instanceId

def orchestator(fn):
    return lambda context: Orchestrator(fn).handle(context)