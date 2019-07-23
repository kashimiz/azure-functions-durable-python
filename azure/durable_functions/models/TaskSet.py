from typing import List
from ..interfaces import IAction


class TaskSet:
    def __init__(self):
        self.isCompleted: bool
        self.isFaulted: bool
        self.actions: List[IAction]
        self.result = None
        self.exception = None
