from enum import Enum


class ErrorCode(Enum):
    SUCCESS = 0
    UNKNOWN_ERROR = 1
    NOT_SUPPORT = 2
    ACCESS_ERROR = 3
    PARSER_ERROR = 4
    REQUEST_ERROR = 5
    DATA_ERROR = 6
    REFLECTOR_ERROR = 7
    NOT_FOUND_ERROR = 8
    INTERNAL_ERROR = 9


class Error:
    def __init__(self, code: ErrorCode, msg: str = None):
        self.code = code
        self.msg = msg

    def __str__(self):
        return f"Error[code: {self.code}, msg: {self.msg}]"
