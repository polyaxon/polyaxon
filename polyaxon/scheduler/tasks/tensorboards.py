import logging

from constants.jobs import JobLifeCycle
from db.getters.tensorboards import get_valid_tensorboard
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import Intervals, SchedulerCeleryTasks
from scheduler import tensorboard_scheduler

_logger = logging.getLogger(__name__)


@celery_app.task(name=SchedulerCeleryTasks.TENSORBOARDS_START, ignore_result=True)
def tensorboards_start(tensorboard_job_id):
    tensorboard = get_valid_tensorboard(tensorboard_job_id=tensorboard_job_id)
    if not tensorboard:
        return None

    if not JobLifeCycle.can_transition(status_from=tensorboard.last_status,
                                       status_to=JobLifeCycle.SCHEDULED):
        _logger.info('Tensorboard `%s` cannot transition from `%s` to `%s`.',
                     tensorboard.unique_name, tensorboard.last_status, JobLifeCycle.SCHEDULED)

    tensorboard_scheduler.start_tensorboard(tensorboard)


@celery_app.task(name=SchedulerCeleryTasks.TENSORBOARDS_STOP,
                 bind=True,
                 max_retries=3,
                 ignore_result=True)
def tensorboards_stop(self,
                      project_name,
                      project_uuid,
                      tensorboard_job_name,
                      tensorboard_job_uuid,
                      update_status=True):
    deleted = tensorboard_scheduler.stop_tensorboard(
        project_name=project_name,
        project_uuid=project_uuid,
        tensorboard_job_name=tensorboard_job_name,
        tensorboard_job_uuid=tensorboard_job_uuid
    )

    if not deleted and self.request.retries < 2:
        _logger.info('Trying again to delete job `%s`.', tensorboard_job_name)
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)
        return

    if not update_status:
        return

    tensorboard = get_valid_tensorboard(tensorboard_job_uuid=tensorboard_job_uuid)
    if not tensorboard:
        return None

    # Update tensorboard status to show that its stopped
    tensorboard.set_status(status=JobLifeCycle.STOPPED,
                           message='Tensorboard was stopped')
