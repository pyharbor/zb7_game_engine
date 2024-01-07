from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    pass


class StackItem:
    def __init__(self, op: str, object, context=None):
        self.op = op
        self.object = object
        self.context = context

    def __str__(self):
        return f"{self.op} {self.object} {self.context}"