from typing import Any

from core.resource.resource import BaseResource, ResType


class ImageResource(BaseResource):
    def __init__(self, data: str = None):
        super().__init__(type=ResType.IMAGE, data=data)
