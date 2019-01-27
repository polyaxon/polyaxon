from constants.jobs import JobLifeCycle
from db.models.notebooks import NotebookJob
from libs.base_clean import BaseCleanCommand
from scheduler import notebook_scheduler


class Command(BaseCleanCommand):
    @staticmethod
    def _clean() -> None:
        for job in NotebookJob.objects.filter(
                status__status__in=JobLifeCycle.RUNNING_STATUS):
            notebook_scheduler.stop_notebook(
                project_name=job.project.unique_name,
                project_uuid=job.project.uuid.hex,
                notebook_job_name=job.unique_name,
                notebook_job_uuid=job.uuid.hex)
            job.set_status(JobLifeCycle.STOPPED,
                           message='Stop triggered by the cleaning hook.')
