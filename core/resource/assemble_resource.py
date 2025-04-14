from core.resource.resource import BaseResource, ResType


class AssembleResource(BaseResource):
    def __init__(self):
        super().__init__(type=ResType.ASSEMBLE)
        self._data = {}

    def putRes(self, key: str, res: BaseResource) -> BaseResource:
        oldValue: BaseResource = None
        if key in self._data:
            oldValue = self._data[key]
        self._data[key] = res
        return oldValue

    def getRes(self, key: str) -> BaseResource:
        if key in self._data:
            return self._data[key]
        else:
            return None
