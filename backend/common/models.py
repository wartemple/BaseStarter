
import uuid
from django.db import models
from django_softdelete.models import SoftDeleteModel
from enum import Enum
from typing import List, Any


class BaseModel(SoftDeleteModel):
    """基础数据表"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, primary_key=True)
    
    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        abstract = True


class BaseEnum(Enum):

    @classmethod
    def values(cls) -> List[str]:
        return [_.value for _ in cls]

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls.values()

    @classmethod
    def get_value(cls, value: str) -> Any:
        enum_map = {_.value: _ for _ in cls}
        return enum_map[value]
