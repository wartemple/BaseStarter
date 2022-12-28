# 使用django 默认的权限登录
from typing import List

from common.models import BaseModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


class Auth(BaseModel):
    """
    权限model类
    用于保存用户权限
    """


class PermissionDO:

    def __init__(self, codename, name):
        """
        codename：{app_label}__{model_name}__{action_name}
        name：{action_verbose}{model_verbose}
        """
        self.codename = codename
        self.name = name

    @classmethod
    def save(cls, permission_data_objects: List['PermissionDO']):
        content_type = ContentType.objects.get(app_label='permission', model='auth')
        codenames = [permission_data_object.codename for permission_data_object in permission_data_objects]
        for permission_obj in Permission.objects.filter(content_type=content_type):
            if permission_obj.codename not in codenames:
                permission_obj.delete()
        for permission_data_object in permission_data_objects:
            if Permission.objects.filter(codename=permission_data_object.codename).exists():
                Permission.objects.filter(codename=permission_data_object.codename).update(
                    name=permission_data_object.name)
                continue
            if not Permission.objects.filter(
                    codename=permission_data_object.codename, name=permission_data_object.name).exists():
                Permission(
                    content_type=content_type,
                    codename=permission_data_object.codename,
                    name=permission_data_object.name).save()