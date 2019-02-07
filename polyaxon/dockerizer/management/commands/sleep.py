import logging
import time

from django.core.management.base import BaseCommand

_logger = logging.getLogger('polyaxon.dockerizer.commands')


class Command(BaseCommand):
    """Management utility to start building a docker image."""
    help = 'Used to initialize a context to build a docker image.'

    def handle(self, *args, **options):
        time.sleep(60*60)
