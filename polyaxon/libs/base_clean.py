from django.core.management import BaseCommand
from django.db import DatabaseError


class BaseCleanCommand(BaseCommand):
    @staticmethod
    def _clean():
        raise NotImplementedError

    def handle(self, *args, **options):
        try:
            self._clean()
            import time;
            time.sleep(180)
        except DatabaseError:
            pass
