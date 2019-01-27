from constants.jobs import JobLifeCycle
from db.models.jobs import Job
from libs.base_clean import BaseCleanCommand
from scheduler import job_scheduler


class Command(BaseCleanCommand):
    @staticmethod
    def _clean() -> None:
        for job in Job.objects.filter(
                status__status__in=JobLifeCycle.RUNNING_STATUS):
            job_scheduler.stop_job(
                project_name=job.project.unique_name,
                project_uuid=job.project.uuid.hex,
                job_name=job.unique_name,
                job_uuid=job.uuid.hex)
            job.set_status(JobLifeCycle.STOPPED,
                           message='Stop triggered by the cleaning hook.')
