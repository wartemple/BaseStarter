
from django.contrib.auth.models import Group, User, Permission
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from common.viewsets import BaseModelViewSet
from django.contrib.contenttypes.models import ContentType


from .serializers import GroupSerializer, PermissionSerializer, UserSerializer


class PermissionViewSet(BaseModelViewSet):
    """
    权限接口
    """
    serializer_class = PermissionSerializer

    def get_queryset(self):
        content_type = ContentType.objects.get(app_label='permission', model='auth')
        return Permission.objects.filter(content_type=content_type).order_by('id')



class GroupViewSet(BaseModelViewSet):
    """
    角色接口
    """
    verbose_name = '角色'
    serializer_class = GroupSerializer
    queryset = Group.objects.all().prefetch_related('permissions').order_by('id')
    search_fields = ('name',)


class UserViewSet(BaseModelViewSet):
    """
    用户接口
    """
    verbose_name = '用户'
    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related('groups').order_by('id')
    search_fields = ('username',)
    filterset_fields = {'is_active': ['exact'], 'groups': ['exact']}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, pk):
        self._verify_user(request)
        return super(UserViewSet, self).partial_update(request, pk)

    def _verify_user(self, request):
        username = request.data.get('username', None)
        old_password = request.data.pop('old_password', None)
        password = request.data.get('password', None)
        password2 = request.data.pop('password2', None)
        if old_password:
            if not password or not password2:
                raise ValueError('请输入密码')
            if password != password2:
                raise ValueError('新密码两次不一致')
            if password == old_password:
                raise ValueError('新旧密码应该不同')
            user_data = {'username': username, 'password': old_password}
            serializer = AuthTokenSerializer(data=user_data, context={'request': request})
            if not serializer.is_valid() or serializer.validated_data['user'] != request.user:
                raise ValueError('旧用户名密码错误')
        elif password and password2:
            if password != password2:
                raise ValueError('新密码两次不一致')
        else:
            request.data.pop('password', None)

    @action(detail=False, methods=['PATCH'])
    def password(self, request):
        self.request.data['username'] = request.user.username
        self._verify_user(request)
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)