from kombu import Exchange

from django.core.management import BaseCommand

import workers


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        Exchange('internal', type='topic', channel=workers.app.connection().channel()).declare()
