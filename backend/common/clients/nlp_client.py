import requests
from django.conf import settings
import logging
from common.utils import TimeUtils

logger = logging.getLogger(__name__)


class NlpClient:
    correct_route = '/api/correct/ernie_rules'
    correct_sync_route = '/api/correct/reload'
    correct_server = settings.CORRECTING_SERVER
    quality_inspect_route = '/api/v1/finance/dialogues/parse'
    quality_inspect_reload_route = '/api/v1/finance/train_model'
    quality_inspect_server = settings.QUALITY_INSPECTION_SERVER
    compare_route = '/api/v1/compare_documents'
    compare_server = settings.COMPARE_SERVER

    @classmethod
    def correct(cls, query):
        response = requests.post(f'{cls.correct_server}{cls.correct_route}', json={
            "query": query
        })
        if response.json()['status'] != 200:
            raise ValueError('纠错服务报错')
        return response.json()['data']

    @classmethod
    def sync_correct_data(cls, username, data):
        json = {"user": username, "file_urls": data}
        logger.info(f'sync correct server {json}')
        response = requests.post(f'{cls.correct_server}{cls.correct_sync_route}', json=json)
        if response.json()['status'] != 200:
            raise ValueError('纠错重新训练服务报错')
        return response.json()['data']

    @classmethod
    def quality_inspection(cls, query, rule_ids=[], threshold=80):
        json = {
            "messages": [{
                "messageId": "dg123",
                "role": "agent",
                "userId": "a3312",
                "tenantId": 20, # TODO: 修改租户id是动态
                "rules_id_list": rule_ids,
                "content": query,
                "sim_threshold": threshold,
                "messageTime": "20211216 00:00:01"
            }]
        }
        logger.info(f'parse quality_inspection server {json}')
        response = requests.post(f'{cls.quality_inspect_server}{cls.quality_inspect_route}', json=json)
        if response.json()['status'] != 200:
            raise ValueError('质检服务报错')
        data = response.json()['data']
        return {} if data is None else data

    @classmethod
    def reload_quality_inspection_model(cls, username, file_path):
        url, datetime = file_path.split(f'/{username}/')
        json = {"user": username, "url": url, "datetime": datetime.replace('.json', '')}
        logger.info(f'reload qt server {json}')
        print(json)
        response = requests.post(f'{cls.quality_inspect_server}{cls.quality_inspect_reload_route}', json=json)
        if response.json()['status'] != 200:
            raise ValueError('纠错重新训练服务报错')
        return response.json()['data']

    @classmethod
    def compare(cls, text1, text2):
        json = { "text1": text1, "text2": text2 }
        logger.info(f'parse compare server {json}')
        response = requests.post(f'{cls.compare_server}{cls.compare_route}', json=json)
        if response.json()['status'] != 200:
            raise ValueError('质检服务报错')
        data = response.json()['data']
        return {} if data is None else data