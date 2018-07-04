from django.core.management import BaseCommand
from django.db import ProgrammingError

from constants.jobs import JobLifeCycle
from db.models.notebooks import NotebookJob
from scheduler import notebook_scheduler


class Command(BaseCommand):
    @staticmethod
    def _clean():
        for job in NotebookJob.objects.filter(
                status__status__in=JobLifeCycle.RUNNING_STATUS):
            notebook_scheduler.stop_notebook(
                project_name=job.project.unique_name,
                project_uuid=job.project.uuid.hex,
                notebook_job_name=job.unique_name,
                notebook_job_uuid=job.unique_name)
            job.set_status(JobLifeCycle.STOPPED, message='Cleanup')

    def handle(self, *args, **options):
        try:
            self._clean()
        except ProgrammingError:
            pass
