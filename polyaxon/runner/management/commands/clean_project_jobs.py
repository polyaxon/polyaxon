from django.core.management import BaseCommand
from django.db import ProgrammingError
from django.db.models import Q

from projects.models import Project
from runner.schedulers import notebook_scheduler, tensorboard_scheduler


class Command(BaseCommand):
    @staticmethod
    def _clean():
        for project in Project.objects.filter(Q(has_tensorboard=True) | Q(has_notebook=True)):
            if project.has_notebook:
                notebook_scheduler.stop_notebook(project, update_status=False)
            if project.has_tensorboard:
                tensorboard_scheduler.stop_tensorboard(project, update_status=False)

    def handle(self, *args, **options):
        try:
            self._clean()
        except ProgrammingError:
            pass
