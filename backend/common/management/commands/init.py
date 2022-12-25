from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = '初始化app'

    def handle(self, *args, **options):
        User.objects.create_superuser('admin','byjk_123456')
