from rest_framework.response import Response
from io import StringIO
from common.utils import ViewUtils
import pandas as pd
import chardet
import csv
from rest_framework import status
from django.db import transaction


class ExportModelMixin:
    # 导出模型

    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(data=queryset, many=True)
        serializer.is_valid()
        return ViewUtils.get_excel_response(serializer.data, 'export')


class BulkDeleteModelMixin:
    # 批量删除模型
    def bulk_delete(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UploadModelMixin:
    # 导入模型

    def upload(self, request, *args, **kwargs):
        raw_data = request.data['file'].read()
        encoding = chardet.detect(raw_data)['encoding']
        csv_file = StringIO(raw_data.decode(encoding))
        reader = csv.DictReader(csv_file)
        serializer = self.get_serializer()
        model_class = serializer.Meta.model
        objs = []
        for row in reader:
            model = model_class()
            for filed, title in self.import_filed2title.items():
                setattr(model, filed, row[title])
            self.set_obj_field(model)
            objs.append(model)
        csv_file.close()
        with transaction.atomic():
            model_class.objects.bulk_create(objs)
        return Response({"message": "upload success"})

    def set_obj_field(self, model):
        pass