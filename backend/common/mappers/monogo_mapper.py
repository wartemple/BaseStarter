from pymongo import MongoClient
from bson.son import SON
import datetime
from django.conf import settings


class MongoMapper:

    def __init__(self) -> None:
        host = settings.DATABASES['mongo']['CLIENT']['HOST']
        port = settings.DATABASES['mongo']['CLIENT']['port']
        username = settings.DATABASES['mongo']['CLIENT']['username']
        password = settings.DATABASES['mongo']['CLIENT']['password']
        self.client = MongoClient(host=host,
                                  port=int(port),
                                  username=username,
                                  password=password)

    def aggr_last_week_hot_questions(self, threshold: float = 0.75, before_days: int = 7, limit: int = 5):
        with self.client.start_session(causal_consistency=True) as my_session:
            with my_session.start_transaction():
                db = self.client.tracker_store
                collection = db.conversations
                today = datetime.datetime.now()
                last_week = today - datetime.timedelta(before_days)
                pipeline = [{
                    '$unwind': '$events'
                }, {
                    '$match': {
                        'events.parse_data.response_selector.faq.response.confidence':
                        {
                            '$gte': threshold
                        },
                        'events.event': 'user',
                        'events.timestamp': {
                            '$gte': datetime.datetime.timestamp(last_week)
                        }
                    }
                }, {
                    '$group': {
                        '_id':
                        '$events.parse_data.response_selector.faq.response.intent_response_key',
                        'count': {
                            '$sum': 1
                        }
                    }
                }, {
                    '$sort': SON([
                        ('count', -1),
                    ])
                }, {
                    '$limit': limit
                }]
                results = collection.aggregate(pipeline)
                return results
