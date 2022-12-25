from docx import Document


class DocxParser:
    def parse(self, file_):
        document = Document(file_)
        content = ''
        for paragraph in document.paragraphs:
            content += paragraph.text
        return content
