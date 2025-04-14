from docx import Document

from core.resource.resource import BaseResource
from doc_engine.generator import BaseGen


class ImageGen(BaseGen):
    def genContent(self, doc: Document, resource: BaseResource, run, paragraph) -> bool:
        section = doc.sections[0]  # 获取文档的第一个节（通常是默认节）
        page_width = section.page_width - section.left_margin - section.right_margin
        imageRun = paragraph.add_run()
        imageRun.add_picture(resource.getData(), width=page_width)
        return True
