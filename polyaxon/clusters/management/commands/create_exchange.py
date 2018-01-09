from django.core.management import BaseCommand
from kombu import Exchange

from polyaxon.celery_api import app as celery_app


class Command(BaseCommand):
    def handle(self, *args, **options):
        Exchange('internal', type='topic', channel=celery_app.connection().channel()).declare()
