import logging

import conf
import workers

from db.getters.tensorboards import get_valid_tensorboard
from lifecycles.jobs import JobLifeCycle
from options.registry.scheduler import SCHEDULER_GLOBAL_COUNTDOWN_DELAYED
from polyaxon.settings import Intervals, SchedulerCeleryTasks
from scheduler import tensorboard_scheduler
from stores.exceptions import VolumeNotFoundError

_logger = logging.getLogger(__name__)


@workers.app.task(name=SchedulerCeleryTasks.TENSORBOARDS_START, ignore_result=True)
def tensorboards_start(tensorboard_job_id):
    tensorboard = get_valid_tensorboard(tensorboard_job_id=tensorboard_job_id)
    if not tensorboard:
        return None

    if not JobLifeCycle.can_transition(status_from=tensorboard.last_status,
                                       status_to=JobLifeCycle.SCHEDULED):
        _logger.info('Tensorboard `%s` cannot transition from `%s` to `%s`.',
                     tensorboard.unique_name, tensorboard.last_status, JobLifeCycle.SCHEDULED)

    try:
        tensorboard_scheduler.start_tensorboard(tensorboard)
    except VolumeNotFoundError:
        tensorboard.set_status(status=JobLifeCycle.FAILED,
                               message='Tensorboard failed to start, '
                                       'the outputs volume/storage was not found.')


@workers.app.task(name=SchedulerCeleryTasks.TENSORBOARDS_SCHEDULE_DELETION, ignore_result=True)
def tensorboards_schedule_deletion(tensorboard_job_id, immediate=False):
    tensorboard = get_valid_tensorboard(tensorboard_job_id=tensorboard_job_id,
                                        include_deleted=True)
    if not tensorboard:
        return None

    tensorboard.archive()

    if tensorboard.is_stoppable:
        project = tensorboard.project
        workers.send(
            SchedulerCeleryTasks.TENSORBOARDS_STOP,
            kwargs={
                'project_name': project.unique_name,
                'project_uuid': project.uuid.hex,
                'tensorboard_job_name': tensorboard.unique_name,
                'tensorboard_job_uuid': tensorboard.uuid.hex,
                'update_status': True,
                'collect_logs': False,
                'is_managed': tensorboard.is_managed,
                'message': 'Tensorboard is scheduled for deletion.'
            })

    if immediate:
        workers.send(
            SchedulerCeleryTasks.DELETE_ARCHIVED_TENSORBOARD_JOB,
            kwargs={
                'job_id': tensorboard_job_id,
            },
            countdown=conf.get(SCHEDULER_GLOBAL_COUNTDOWN_DELAYED))


@workers.app.task(name=SchedulerCeleryTasks.TENSORBOARDS_STOP,
                  bind=True,
                  max_retries=3,
                  ignore_result=True)
def tensorboards_stop(self,
                      project_name,
                      project_uuid,
                      tensorboard_job_name,
                      tensorboard_job_uuid,
                      update_status=True,
                      collect_logs=False,
                      is_managed=True,
                      message=None):
    if is_managed:
        deleted = tensorboard_scheduler.stop_tensorboard(
            project_name=project_name,
            project_uuid=project_uuid,
            tensorboard_job_name=tensorboard_job_name,
            tensorboard_job_uuid=tensorboard_job_uuid
        )
    else:
        deleted = True

    if not deleted and self.request.retries < 2:
        _logger.info('Trying again to delete job `%s`.', tensorboard_job_name)
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)
        return

    if not update_status:
        return

    tensorboard = get_valid_tensorboard(tensorboard_job_uuid=tensorboard_job_uuid,
                                        include_deleted=True)
    if not tensorboard:
        return None

    # Update tensorboard status to show that its stopped
    tensorboard.set_status(status=JobLifeCycle.STOPPED,
                           message=message or 'Tensorboard was stopped')
