

from rest_framework.response import Response
from rest_framework.views import APIView
from common.utils import HashUtils, FileUtils
from common.mappers import MinioMapper


class UploadFileView(APIView):
    minio_mapper = MinioMapper()

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response(status=400)
        local_path = FileUtils.save_inmemoryfile(file)
        remote_path = self.minio_mapper.set_file(local_path, 'media')
        return Response({
			"path": remote_path
		})