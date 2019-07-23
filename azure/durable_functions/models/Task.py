from datetime import datetime
from ..interfaces import IAction


class Task:
    def __init__(self):
        self.isCompleted: bool
        self.isFaulted: bool
        self.action: IAction
        self.result = None
        self.timestamp: datetime
        self.id = None
        self.exception = None
