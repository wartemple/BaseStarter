import os
from logging.config import dictConfig

from django.conf import settings
from yunfu.common import ConfigUtils

from celery import Celery
from celery.signals import setup_logging

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('yunfu-due-common', broker=f'pyamqp://guest@{settings.RABBIT_MQ_HOST}:{settings.RABBIT_MQ_PORT}//')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


# 配置日志格式
@setup_logging.connect
def config_loggers(*args, **kwargs):
    dictConfig(ConfigUtils.load(settings.CELERY_LOG_CONFIG_FILE))


# Load task modules from all registered Django apps.
app.autodiscover_tasks()
