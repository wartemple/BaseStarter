import json
import os

from .time_utils import TimeUtils
from .hash_utils import HashUtils
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


class FileUtils:
    @classmethod
    def save_json(cls, data, prefix=''):
        local_filename = f"{prefix}{TimeUtils.get_now_datetime_str()}.json"
        with open(local_filename, "w") as out_file:
            out_file.write(json.dumps(data, ensure_ascii=False))
        return local_filename

    @classmethod
    def clear_file(cls, filename):
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print(f"Can not delete the file: {filename} as it doesn't exists")

    @classmethod
    def save_inmemoryfile(cls, file):
        filename = f'{TimeUtils.get_now_datetime_str()}_{file.name}'
        path = default_storage.save(f'media/tmp/{filename}', ContentFile(file.read()))
        return os.path.join(settings.BASE_DIR, path)