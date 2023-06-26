# 使用django 默认的权限登录

from common.models import BaseModel


class Auth(BaseModel):
    """
    权限model类
    用于保存用户权限
    """
