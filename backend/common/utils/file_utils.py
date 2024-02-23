import os

from libs.time_utils import TimeUtils
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


class FileUtils:

    @classmethod
    def save_inmemoryfile(cls, file):
        filename = f'{TimeUtils.get_now_datetime_str()}_{file.name}'
        path = default_storage.save(f'media/tmp/{filename}', ContentFile(file.read()))
        return os.path.join(settings.BASE_DIR, path)
