import os

from core.errors.error import Error, ErrorCode
from core.utils.log import logger


def mkdir(path: str) -> Error:
    try:
        if not os.path.isdir(path):
            os.makedirs(path)
        return Error(ErrorCode.SUCCESS)
    except OSError:
        logger.warning(f"Unable to create {path}")
        return Error(ErrorCode.ACCESS_ERROR, f'Unable to create {path}')
