from core.resource.resource import BaseResource, ResType


class HyperlinkInfo:
    def __init__(self, link: str, text: str):
        self.link = link
        self.text = text


class HyperlinkResource(BaseResource):
    def __init__(self, link: str, text: str):
        super().__init__(type=ResType.HYPERLINK)
        self._data = HyperlinkInfo(link, text)
