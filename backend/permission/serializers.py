from django.contrib.auth.models import Group, Permission, User
from rest_framework import serializers



class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ('id', 'codename', 'name')


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, allow_null=True, queryset=Permission.objects.all())

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')


class RetrieveGroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, allow_null=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, allow_null=True, queryset=Group.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'is_active', 'date_joined', 'last_login', 'groups')

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        super(UserSerializer, self).update(instance, validated_data)
        if 'password' in validated_data:
            # 更新密码过期时间
            instance.profile.reset_password_expired_time()
            # 更新密码
            instance.set_password(validated_data['password'])
            instance.save()
        return instance

    def to_representation(self, obj):
        instance = super(UserSerializer, self).to_representation(obj)
        instance.pop('password', None)
        return instance


class RetrieveUserSerializer(serializers.ModelSerializer):
    groups = RetrieveGroupSerializer(many=True, allow_null=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_active', 'date_joined', 'last_login', 'groups')
