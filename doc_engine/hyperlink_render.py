from docx import Document

from core.resource.resource import BaseResource
from doc_engine.generator import BaseGen


class HyperlinkGen(BaseGen):
    def genContent(self, doc: Document, resource: BaseResource, run, paragraph) -> bool:
        return False
