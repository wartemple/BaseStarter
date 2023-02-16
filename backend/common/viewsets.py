
from rest_framework.viewsets import ModelViewSet

from .mixins import BulkDeleteModelMixin, ExportModelMixin, UploadModelMixin


class BaseModelViewSet(ModelViewSet, ExportModelMixin, BulkDeleteModelMixin, UploadModelMixin):
    filterset_fields = {
        'id': ['in']
    }
    
    def get_serializer_class(self):
        if hasattr(self, "detail_serializer_class") and hasattr(self, "request") and self.detail_serializer_class is not None and self.request.method == 'GET':
            return self.detail_serializer_class
        return self.serializer_class