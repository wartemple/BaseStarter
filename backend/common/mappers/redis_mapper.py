import redis
from django.conf import settings
import json
from django.utils.safestring import mark_safe


class RedisMapper:
    def __init__(self) -> None:
        pool = redis.ConnectionPool(
            host=settings.REDIS['host'], port=settings.REDIS['port'], db=0, password=settings.REDIS['password'])
        self.client = redis.Redis(
            connection_pool=pool, decode_responses=True, encoding="utf-8")

    def set_array(self, key, items):
        self.client.rpush("key", *items)

    def get_array(self, key, start_index=0, end_index=-1):
        return self.client.lrange(key, start_index, end_index)

    def set_hash_results(self, key, value):
        self.client.set(key, json.dumps(value, ensure_ascii=False))
        self.client.expire(key, 10)

    def get_hash_results(self, key):
        if not self.client.exists(key):
            return None
        results = json.loads(mark_safe(self.client.get(key)))
        if "Context" not in results or "RecallList" not in results:
            return None
        return results
