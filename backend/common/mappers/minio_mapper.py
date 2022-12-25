from minio import Minio
from django.conf import settings
from common.utils import TimeUtils, FileUtils


class MinioMapper:
    def __init__(self,):
        self.client = Minio(
            settings.MINIO['url'], access_key=settings.MINIO['user'], secret_key=settings.MINIO['password'],
            secure=False
        )

    def init(self, bucket_name):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
        else:
            print(f"Bucket {bucket_name} already exists")

    def set_json(self, tenant_name, data, bucket_name, prefix=""):
        self.init(bucket_name)
        locals_filename = f'{FileUtils.save_json(data, prefix)}'
        remote_path = f'{tenant_name}/{locals_filename}'
        self.client.fput_object(bucket_name, remote_path, locals_filename, content_type="application/json")
        FileUtils.clear_file(locals_filename)
        return f'http://{settings.MINIO["url"]}/{bucket_name}/{remote_path}'

    def set_file(self, filepath, bucket_name, filename, prefix=''):
        remote_path = f'{prefix}/{TimeUtils.get_now_datetime_str()}{filename}'
        self.client.fput_object(bucket_name, remote_path, filepath)
        return f'http://{settings.MINIO["url"]}/{bucket_name}/{remote_path}'