from docx import Document

from core.resource.resource import BaseResource


class BaseGen:
    def genContent(self, doc: Document, resource: BaseResource, run, paragraph) -> bool:
        pass
