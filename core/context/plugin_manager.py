from .context import Context
from core.errors.error import Error, ErrorCode
from core.plugin.plugin_loader import loadPlugins
from core.resource.resource import BaseResource


class PluginManager:
    def __init__(self, path: str):
        self._plugins: dict = {}
        self._cache: dict = {}
        self.path = path

    def load(self, workPath: str) -> Error:
        err, plugins = loadPlugins(self.path, workPath)
        if err.code == ErrorCode.SUCCESS:
            for plugin in plugins:
                self._plugins[plugin.key] = plugin
        return err

    def create(self, ctx: Context) -> Error:
        for _, plugin in self._plugins.items():
            err = plugin.onCreate(ctx)
            if err.code != ErrorCode.SUCCESS:
                return err

    def process(self, pluginKey: str, ctx: Context) -> (Error, BaseResource):
        if pluginKey in self._cache:
            return Error(ErrorCode.SUCCESS), self._cache[pluginKey]
        if pluginKey in self._plugins:
            err, res = self._plugins[pluginKey].onProcess(ctx)
            if err.code == ErrorCode.SUCCESS:
                self._cache[pluginKey] = res
            return err, res
        return Error(ErrorCode.NOT_FOUND_ERROR, f"Not found {pluginKey}"), None

    def destroy(self):
        for plugin in self._plugins:
            plugin.onDestroy()
        self._plugins = {}
        self._cache = {}
