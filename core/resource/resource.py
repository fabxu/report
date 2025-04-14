from enum import Enum
from typing import Any


class ResType(Enum):
    TEXT = 1
    IMAGE = 2
    HYPERLINK = 3
    ASSEMBLE = 4


class BaseResource:
    def __init__(self, type: ResType, data: Any = None):
        self._type = type
        self._data = data

    def getType(self) -> ResType:
        return self._type

    def setData(self, data: Any):
        self._data = data

    def getData(self) -> Any:
        return self._data
