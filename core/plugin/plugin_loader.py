import json

from core.errors.error import Error, ErrorCode
from core.plugin.base_plugin import BasePlugin
from core.utils.log import logger


def _createPlugin(classPath: str, workPath: str, prop: dict) -> (Error, BasePlugin):
    module_path, class_name = classPath.rsplit(".", 1)
    try:
        # 动态导入模块
        module = __import__(module_path, fromlist=[class_name])

        # 获取类对象
        cls = getattr(module, class_name)
        return Error(ErrorCode.SUCCESS), cls(workPath, prop)
    except BaseException:
        logger.warning(f"plugin unable to create {classPath}")
        return Error(ErrorCode.REFLECTOR_ERROR, f'plugin unable to create {classPath}'), None


def loadPlugins(path: str, workPath: str) -> (Error, list):
    plugins = []
    with open(path, 'r') as file:
        properties = json.load(file)
        for item in properties:
            err, plugin = _createPlugin(item['class'], workPath, item)
            if err.code == ErrorCode.SUCCESS:
                plugins.append(plugin)
            else:
                return err, plugins
    return Error(ErrorCode.SUCCESS), plugins
