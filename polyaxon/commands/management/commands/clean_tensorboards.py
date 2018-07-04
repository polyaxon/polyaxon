from django.core.management import BaseCommand
from django.db import ProgrammingError

from constants.jobs import JobLifeCycle
from db.models.tensorboards import TensorboardJob
from scheduler import tensorboard_scheduler


class Command(BaseCommand):
    @staticmethod
    def _clean():
        for job in TensorboardJob.objects.filter(
                status__status__in=JobLifeCycle.RUNNING_STATUS):
            tensorboard_scheduler.stop_tensorboard(
                project_name=job.project.unique_name,
                project_uuid=job.project.uuid.hex,
                tensorboard_job_name=job.unique_name,
                tensorboard_job_uuid=job.unique_name)
            job.set_status(JobLifeCycle.STOPPED, message='Cleanup')

    def handle(self, *args, **options):
        try:
            self._clean()
        except ProgrammingError:
            pass
