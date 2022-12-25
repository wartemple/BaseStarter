import requests
from django.conf import settings
from common.mappers import MinioMapper


class OcrClient:
	suffix = '/api/v1/ocr/parse_pic'
	images_bucket = "ocr_data"
	minio_mapper = MinioMapper()

	@classmethod
	def ocr(cls, file_path):
		filename = file_path.split('/')[-1]
		remote_link = cls.minio_mapper.set_file(file_path, bucket_name='images', filename=filename)
		url = f'{settings.OCR_SERVER}{cls.suffix}'
		response = requests.post(url, json={"link": remote_link})
		if response.json()['status'] != 200:
			return ''
		text = ''
		for word in response.json()['data']:
			print(word)
			text += word['words']
		return text
