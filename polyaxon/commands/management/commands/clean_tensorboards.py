from constants.jobs import JobLifeCycle
from db.models.tensorboards import TensorboardJob
from libs.base_clean import BaseCleanCommand
from scheduler import tensorboard_scheduler


class Command(BaseCleanCommand):
    @staticmethod
    def _clean() -> None:
        for job in TensorboardJob.objects.filter(
                status__status__in=JobLifeCycle.RUNNING_STATUS):
            tensorboard_scheduler.stop_tensorboard(
                project_name=job.project.unique_name,
                project_uuid=job.project.uuid.hex,
                tensorboard_job_name=job.unique_name,
                tensorboard_job_uuid=job.uuid.hex)
            job.set_status(JobLifeCycle.STOPPED, message='Stop triggered by the cleaning hook.')
