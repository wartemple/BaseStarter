from common.parsers import UrlParser, DocxParser, TxtParser, ImageParser


class ParserFactory:

    @classmethod
    def get_parser(cls, type_: str, file_suffix: str = ''):
        if type_ == 'file':
            if file_suffix == 'txt':
                return TxtParser()
            elif file_suffix == 'docx':
                return DocxParser()
            elif file_suffix in ['png', 'jpg', 'jpeg']:
                return ImageParser()
        elif type_ == 'url':
            return UrlParser()
        raise ValueError(f'not register {type_} {file_suffix} Parser')