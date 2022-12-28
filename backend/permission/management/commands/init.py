import logging

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from permission.generators import PermissionGenerator
from permission.models import PermissionDO

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        # 权限
        generator = PermissionGenerator()
        permissions = generator.generate()
        PermissionDO.save(permissions)
        logger.info('create permissions success!')

        # 用户组：系统管理员
        content_type = ContentType.objects.get(app_label='permission', model='auth')
        permissions = Permission.objects.filter(content_type=content_type)
        admin_group, created = Group.objects.get_or_create(name='系统管理员')
        admin_group = Group.objects.get(id=admin_group.id)
        for permission in permissions:
            admin_group.permissions.add(permission)
        logger.info('create admin group success!')
        # 用户组：普通用户
        default_permissions = Permission.objects.filter(content_type=content_type, codename__in=['default', 'auth__user__password'])
        staff_group, created = Group.objects.get_or_create(name='普通用户')
        staff_group = Group.objects.get(id=staff_group.id)
        staff_group.permissions.set(default_permissions)
        logger.info('create default group success!')

        # 超级用户admin
        username, email, password, group_names = self._get_superuser_info()
        if User.objects.filter(username=username).exists():
            logger.info('user(admin) is already exist!')
            user = User.objects.get(username=username)
            for group_name in group_names:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            user.save()
        else:
            User.objects.create_superuser(username, email, password)
            user = User.objects.get(username=username)
            for group_name in group_names:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            user.save()
            logger.info('create user(admin) success!')

    def _get_superuser_info(self,):
        name, email, password, group_names = 'admin', 'admin@byjk.com', '123456', ['系统管理员']
        return name, email, password, group_names
