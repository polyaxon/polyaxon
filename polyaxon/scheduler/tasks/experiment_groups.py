import logging

import conf

from constants.experiment_groups import ExperimentGroupLifeCycle
from constants.experiments import ExperimentLifeCycle
from db.getters.experiment_groups import get_running_experiment_group, get_valid_experiment_group
from polyaxon.celery_api import celery_app
from polyaxon.settings import HPCeleryTasks, Intervals, SchedulerCeleryTasks
from scheduler import dockerizer_scheduler

_logger = logging.getLogger(__name__)


def _get_group_or_retry(experiment_group_id, task):
    experiment_group = get_valid_experiment_group(experiment_group_id=experiment_group_id)
    if experiment_group:
        return experiment_group

    # We retry if experiment group does not exist
    if task.request.retries < 2:
        _logger.info('Trying again for ExperimentGroup `%s`.', experiment_group_id)
        task.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)

    _logger.info('Something went wrong, '
                 'the ExperimentGroup `%s` does not exist anymore.', experiment_group_id)
    return None


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_GROUP_CREATE, bind=True, max_retries=None)
def experiments_group_create(self, experiment_group_id):
    experiment_group = _get_group_or_retry(experiment_group_id=experiment_group_id, task=self)
    if not experiment_group:
        return

    last_status = experiment_group.last_status
    if not ExperimentGroupLifeCycle.can_transition(status_from=last_status,
                                                   status_to=ExperimentGroupLifeCycle.RUNNING):
        _logger.info('Experiment group id `%s` cannot transition from `%s` to `%s`.',
                     experiment_group_id, last_status, ExperimentGroupLifeCycle.RUNNING)
        return

    def hp_create():
        experiment_group.set_status(ExperimentGroupLifeCycle.RUNNING)
        celery_app.send_task(
            HPCeleryTasks.HP_CREATE,
            kwargs={'experiment_group_id': experiment_group_id},
            countdown=1)

    # We start first by creating a build if necessary
    # No need to build the image, start the experiment directly
    if not experiment_group.specification.build:
        hp_create()
        return

    _, image_exists, build_status = dockerizer_scheduler.create_build_job(
        user=experiment_group.user,
        project=experiment_group.project,
        config=experiment_group.specification.build,
        configmap_refs=experiment_group.specification.configmap_refs,
        secret_refs=experiment_group.specification.secret_refs,
        code_reference=experiment_group.code_reference)

    if image_exists:
        # The image already exists, so we can start the experiment right away
        hp_create()
        return

    if not build_status:
        experiment_group.set_status(ExperimentGroupLifeCycle.FAILED,
                                    message='Could not start build process.')
        return

    # We start the group process
    hp_create()


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_GROUP_SCHEDULE_DELETION, ignore_result=True)
def experiments_group_schedule_deletion(experiment_group_id, immediate=False):
    experiment_group = get_valid_experiment_group(experiment_group_id=experiment_group_id,
                                                  include_deleted=True)
    if not experiment_group:
        # No need to check this group
        return

    experiment_group.archive()

    if experiment_group.is_stoppable:
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_GROUP_STOP,
            kwargs={
                'experiment_group_id': experiment_group_id,
                'collect_logs': False,
                'message': 'Experiment Group is scheduled for deletion.'
            },
            countdown=conf.get('GLOBAL_COUNTDOWN'))

    if immediate:
        celery_app.send_task(
            SchedulerCeleryTasks.DELETE_ARCHIVED_EXPERIMENT_GROUP,
            kwargs={
                'group_id': experiment_group_id,
            },
            countdown=conf.get('GLOBAL_COUNTDOWN'))


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_GROUP_STOP, ignore_result=True)
def experiments_group_stop(experiment_group_id,
                           collect_logs=True,
                           message=None):
    experiment_group = get_running_experiment_group(experiment_group_id=experiment_group_id,
                                                    include_deleted=True)
    if not experiment_group:
        return

    experiment_group.set_status(ExperimentGroupLifeCycle.STOPPING)
    celery_app.send_task(
        SchedulerCeleryTasks.EXPERIMENTS_GROUP_STOP_EXPERIMENTS,
        kwargs={
            'experiment_group_id': experiment_group_id,
            'pending': False,
            'collect_logs': collect_logs,
            'message': message
        },
        countdown=conf.get('GLOBAL_COUNTDOWN'))


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_GROUP_STOP_EXPERIMENTS, ignore_result=True)
def experiments_group_stop_experiments(experiment_group_id,
                                       pending,
                                       collect_logs=True,
                                       message=None):
    experiment_group = get_running_experiment_group(experiment_group_id=experiment_group_id,
                                                    include_deleted=True)
    if not experiment_group:
        return

    if pending:
        # this won't work for archived groups anyways!
        for experiment in experiment_group.pending_experiments.iterator():
            # Update experiment status to show that its stopped
            experiment.set_status(status=ExperimentLifeCycle.STOPPED, message=message)
    else:
        experiments = experiment_group.all_experiments.exclude(
            status__status__in=ExperimentLifeCycle.DONE_STATUS).distinct().iterator()
        for experiment in experiments:
            if experiment.is_stoppable:
                celery_app.send_task(
                    SchedulerCeleryTasks.EXPERIMENTS_STOP,
                    kwargs={
                        'project_name': experiment.project.unique_name,
                        'project_uuid': experiment.project.uuid.hex,
                        'experiment_name': experiment.unique_name,
                        'experiment_uuid': experiment.uuid.hex,
                        'experiment_group_name': experiment_group.unique_name,
                        'experiment_group_uuid': experiment_group.uuid.hex,
                        'specification': experiment.config,
                        'update_status': True,
                        'collect_logs': collect_logs
                    },
                    countdown=conf.get('GLOBAL_COUNTDOWN'))
            else:
                # Update experiment status to show that its stopped
                experiment.set_status(status=ExperimentLifeCycle.STOPPED, message=message)

    experiment_group.set_status(ExperimentGroupLifeCycle.STOPPED, message=message)


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_GROUP_CHECK_FINISHED,
                 bind=True,
                 max_retries=None,
                 ignore_result=True)
def experiments_group_check_finished(self, experiment_group_id, auto_retry=False):
    experiment_group = get_valid_experiment_group(experiment_group_id=experiment_group_id)
    if not experiment_group or experiment_group.is_done:
        # No need to check this group
        return

    if experiment_group.non_done_experiments.exists():
        if auto_retry:
            self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)
        return

    experiment_group.set_status(status=ExperimentGroupLifeCycle.DONE)
