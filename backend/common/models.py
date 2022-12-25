
import uuid
from django.db import models
from django_softdelete.models import SoftDeleteModel


class BaseModel(SoftDeleteModel):
    """基础数据表"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    username = models.CharField(verbose_name="用户名称", max_length=128, default="admin")
    tenant_name = models.CharField(verbose_name="租户名称", max_length=128, default="admin")

    class Meta:
        abstract = True
