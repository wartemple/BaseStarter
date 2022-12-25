
from rest_framework.viewsets import ModelViewSet

from .mixins import BulkDeleteModelMixin, ExportModelMixin, UploadModelMixin


class BaseModelViewSet(ModelViewSet, ExportModelMixin, BulkDeleteModelMixin, UploadModelMixin):
    filterset_fields = {
        'id': ['in']
    }
