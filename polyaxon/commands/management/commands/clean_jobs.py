from django.core.management import BaseCommand
from django.db import ProgrammingError

from constants.jobs import JobLifeCycle
from db.models.jobs import Job
from scheduler import job_scheduler


class Command(BaseCommand):
    @staticmethod
    def _clean():
        for job in Job.objects.filter(
                status__status__in=JobLifeCycle.RUNNING_STATUS):
            job_scheduler.stop_job(
                project_name=job.project.unique_name,
                project_uuid=job.project.uuid.hex,
                job_name=job.unique_name,
                job_uuid=job.unique_name,
                specification=job.specification)
            job.set_status(JobLifeCycle.STOPPED, message='Cleanup')

    def handle(self, *args, **options):
        try:
            self._clean()
        except ProgrammingError:
            pass
