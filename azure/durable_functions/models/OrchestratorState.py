from typing import List, Any


class OrchestratorState:
    def __init__(self,
                 isDone: bool,
                 actions: List[List[Any]],
                 output: Any,
                 error: str = None,
                 customStatus: Any = None):
        self.isDone: bool = isDone
        self.actions: List[List[Any]] = actions
        self.output: Any = output
        self.error: str = error
        self.customStatus: Any = customStatus
