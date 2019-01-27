from kombu import Exchange

from django.core.management import BaseCommand

from polyaxon.celery_api import celery_app


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        Exchange('internal', type='topic', channel=celery_app.connection().channel()).declare()
