from typing import Any, List

from common.viewsets import BaseModelViewSet
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


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


class PermissionGenerator:
    """权限生成器
    """
    default_verbose_name = {
        "permission": "权限",
        "group": "角色",
        "user": "用户"
    }

    def __init__(self):
        self.default_action2verbose = {
            'create': '新建',
            'read': '查看',
            'update': '编辑',
            'delete': '删除',
            'export': '导出',
            'upload': '导入'
        }

    def generate(self) -> List[PermissionDO]:
        """生成权限
        1. 获取所有的视图类
        2. 新增相关权限
        3. 对权限进行后处理
        """
        model_viewset_classes = self._get_model_viewset()
        permissions = [PermissionDO(codename="admin", name="管理员权限"), PermissionDO(codename="default", name="默认权限")]
        for model_viewset_class in model_viewset_classes:
            permissions.extend(self._generate_permissions(model_viewset_class))
        self._post_process(permissions)
        return permissions

    def _get_model_viewset(self) -> Any:
        return BaseModelViewSet.__subclasses__()

    def _generate_permissions(self, model_viewset_class: BaseModelViewSet) -> List[PermissionDO]:
        """针对视图集生成对应的接口权限
        1. 获取视图集相关模型
        2. 获取视图集相关默认权限
        3. 获取自定义的接口权限
        4.
        """
        model = self._get_model(model_viewset_class)
        results = self._get_default_permissions(model)
        custom_action_objects = self._get_custom_actions(model_viewset_class)
        for custom_action_object in custom_action_objects:
            action_name = custom_action_object.kwargs['name'].lower()
            codename = f"{model._meta.app_label}__{model._meta.model_name}__{action_name}"
            action_verbose_name = custom_action_object.kwargs.get('verbose_name', custom_action_object.kwargs['name'].lower())
            entity_name = self.default_verbose_name.get(model._meta.verbose_name, model._meta.verbose_name)
            name = f'{action_verbose_name}{entity_name}'
            results.append(PermissionDO(codename=codename, name=name))
        return results

    def _post_process(self, permissions: List[PermissionDO]):
        for permission in permissions:
            if permission.codename in settings.DEFAULT_CUSTOM_PERMISSIONS_CODENAME2NAME:
                permission.name = settings.DEFAULT_CUSTOM_PERMISSIONS_CODENAME2NAME[permission.codename]

    def _get_model(self, model_viewset_class: BaseModelViewSet):
        serializer_class = model_viewset_class().get_serializer_class()
        return serializer_class.Meta.model

    def _get_default_permissions(self, model) -> List[PermissionDO]:
        entity_name = self.default_verbose_name.get(model._meta.verbose_name, model._meta.verbose_name)
        results = [
            PermissionDO(codename=f'{model._meta.app_label}__{model._meta.model_name}', name=f"{entity_name}管理")
        ]
        for action_name, action_verbose in self.default_action2verbose.items():
            codename = f"{model._meta.app_label}__{model._meta.model_name}__{action_name}"
            name = f'{action_verbose}{entity_name}'
            results.append(PermissionDO(codename=codename, name=name))
        return results

    def _get_custom_actions(self, model_viewset_class: BaseModelViewSet):
        results = []
        for function in dir(model_viewset_class):
            if callable(getattr(model_viewset_class, function)) and hasattr(
                    getattr(model_viewset_class, function), 'mapping'):
                results.append(getattr(model_viewset_class, function))
        return results
