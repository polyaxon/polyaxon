from django.core.management import BaseCommand
from django.db.models import Q

from projects.models import Project
from spawner import scheduler


class Command(BaseCommand):
    def handle(self, *args, **options):
        for project in Project.objects.filter(Q(has_tensorboard=True) | Q(has_notebook=True)):
            if project.has_notebook:
                scheduler.stop_notebook(project)
            if project.has_tensorboard:
                scheduler.stop_tensorboard(project)
