from ..models import DurableOrchestrationContext
from ..models import DurableOrchestrationBindings


class IFunctionContext:
    def __init__(self):
        self.df: DurableOrchestrationContext
        self.bindings: DurableOrchestrationBindings
