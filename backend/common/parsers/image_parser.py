from common.clients import OcrClient
from common.utils  import FileUtils


class ImageParser:

    def parse(self, file_):
        return OcrClient.ocr(FileUtils.save_inmemoryfile(file_))
