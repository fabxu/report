from core.resource.resource import BaseResource, ResType


class TextResource(BaseResource):
    def __init__(self, data: str = None):
        super().__init__(type=ResType.TEXT, data=data)
