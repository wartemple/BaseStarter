
import hashlib
import time
import uuid
from pathlib import Path

class HashUtils:

    @classmethod
    def get_md5(cls, text):
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    @classmethod
    def get_uuid(cls, text):
        return hashlib.md5(f"{text}{time.time()}".encode("utf-8")).hexdigest()

    @classmethod
    def get_save_dir(cls, instance, name):
        """获取上传文件保存目录"""
        return cls.join_path('upload', str(uuid.uuid1()), name)

    @staticmethod
    def join_path(path, *args):
        """连接路径"""
        return Path(path).joinpath(*args)