from core import constant
from core.context.context import Context
from core.errors.error import Error
from core.resource.resource import BaseResource
from core.utils import file_utils


class BasePlugin:
    def __init__(self, workPath: str, prop: dict):
        self._workdir = workPath + prop["key"] + "/"
        self.key = prop["key"]
        self.name = prop[constant.KEY_NAME]
        self.des = prop["des"]
        self.version = prop[constant.KEY_VERSION]
        file_utils.mkdir(self._workdir)

    def onCreate(self, ctx: Context) -> Error:
        pass

    def onProcess(self, ctx: Context, params: str = None) -> (Error, BaseResource):
        pass

    def onDestroy(self) -> Error:
        pass
