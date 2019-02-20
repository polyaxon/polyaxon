import logging

from polystores.exceptions import PolyaxonStoresException
from rest_framework.exceptions import ValidationError

import conf
import publisher
import stores

from api.experiments.serializers import ExperimentMetricSerializer
from constants.experiments import ExperimentLifeCycle
from db.getters.experiments import get_valid_experiment
from db.redis.heartbeat import RedisHeartBeat
from logs_handlers import collectors
from polyaxon.celery_api import celery_app
from polyaxon.settings import Intervals, SchedulerCeleryTasks
from scheduler import dockerizer_scheduler, experiment_scheduler
from schemas.specifications import ExperimentSpecification
from stores.exceptions import VolumeNotFoundError  # pylint:disable=ungrouped-imports

_logger = logging.getLogger('polyaxon.scheduler.experiments')


def copy_experiment(experiment):
    """If experiment is a restart, we should resume from last check point"""
    try:
        publisher.publish_experiment_job_log(
            log_lines='Copying outputs from experiment `{}` into experiment `{}`'.format(
                experiment.original_experiment.unique_name, experiment.unique_name
            ),
            experiment_uuid=experiment.uuid.hex,
            experiment_name=experiment.unique_name,
            job_uuid='all',
        )
        stores.copy_experiment_outputs(
            persistence_outputs_from=experiment.original_experiment.persistence_outputs,
            persistence_outputs_to=experiment.persistence_outputs,
            experiment_name_from=experiment.original_experiment.unique_name,
            experiment_name_to=experiment.unique_name)

    except OSError:
        publisher.publish_experiment_job_log(
            log_lines='Could not copy the outputs of experiment `{}` into experiment `{}`'.format(
                experiment.original_experiment.unique_name, experiment.unique_name
            ),
            experiment_uuid=experiment.uuid.hex,
            experiment_name=experiment.unique_name,
            job_uuid='all',
        )
        _logger.warning(
            'Could not copy the outputs of experiment `%s` into experiment `%s`',
            experiment.original_experiment.unique_name, experiment.unique_name)


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_BUILD, ignore_result=True)
def experiments_build(experiment_id):
    experiment = get_valid_experiment(experiment_id=experiment_id)
    if not experiment:
        return

    # No need to build the image, start the experiment directly
    if not (experiment.specification.build and experiment.specification.run):
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_START,
            kwargs={'experiment_id': experiment_id},
            countdown=conf.get('GLOBAL_COUNTDOWN'))
        return

    last_status = experiment.last_status
    if not ExperimentLifeCycle.can_transition(status_from=last_status,
                                              status_to=ExperimentLifeCycle.BUILDING):
        _logger.info('Experiment id `%s` cannot transition from `%s` to `%s`.',
                     experiment_id, last_status, ExperimentLifeCycle.BUILDING)
        return

    build_job, image_exists, build_status = dockerizer_scheduler.create_build_job(
        user=experiment.user,
        project=experiment.project,
        config=experiment.specification.build,
        configmap_refs=experiment.specification.configmap_refs,
        secret_refs=experiment.specification.secret_refs,
        code_reference=experiment.code_reference)

    experiment.build_job = build_job
    experiment.save(update_fields=['build_job'])
    if image_exists:
        # The image already exists, so we can start the experiment right away
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_START,
            kwargs={'experiment_id': experiment_id},
            countdown=conf.get('GLOBAL_COUNTDOWN'))
        return

    if not build_status:
        experiment.set_status(ExperimentLifeCycle.FAILED, message='Could not start build process.')
        return

    # Update experiment status to show that its building
    experiment.set_status(ExperimentLifeCycle.BUILDING)


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_CHECK_STATUS, ignore_result=True)
def experiments_check_status(experiment_uuid=None, experiment_id=None):
    experiment = get_valid_experiment(experiment_id=experiment_id, experiment_uuid=experiment_uuid)
    if not experiment:
        return
    experiment.update_status()


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_CHECK_HEARTBEAT, ignore_result=True)
def experiments_check_heartbeat(experiment_id):
    if RedisHeartBeat.experiment_is_alive(experiment_id=experiment_id):
        return

    experiment = get_valid_experiment(experiment_id=experiment_id)
    if not experiment:
        return

    # Experiment is zombie status
    experiment.set_status(ExperimentLifeCycle.FAILED,
                          message='Experiment is in zombie state (no heartbeat was reported).')


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_SET_METRICS, ignore_result=True)
def experiments_set_metrics(experiment_id, data):
    experiment = get_valid_experiment(experiment_id=experiment_id)
    if not experiment:
        return

    kwargs = {}
    if isinstance(data, list):
        kwargs['many'] = True
    serializer = ExperimentMetricSerializer(data=data, **kwargs)
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError:
        _logger.error('Could not create metrics, a validation error was raised.')

    serializer.save(experiment=experiment)


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_START, ignore_result=True)
def experiments_start(experiment_id):
    experiment = get_valid_experiment(experiment_id=experiment_id)
    if not experiment:
        _logger.info('Something went wrong, '
                     'the Experiment `%s` does not exist anymore.', experiment_id)
        return

    if not ExperimentLifeCycle.can_transition(status_from=experiment.last_status,
                                              status_to=ExperimentLifeCycle.SCHEDULED):
        _logger.info('Experiment `%s` cannot transition from `%s` to `%s`.',
                     experiment.unique_name, experiment.last_status, ExperimentLifeCycle.SCHEDULED)
        return None

    experiment_scheduler.start_experiment(experiment)


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_SCHEDULE_DELETION, ignore_result=True)
def experiments_schedule_deletion(experiment_id, immediate=False):
    experiment = get_valid_experiment(experiment_id=experiment_id, include_deleted=True)
    if not experiment:
        _logger.info('Something went wrong, '
                     'the Experiment `%s` does not exist anymore.', experiment_id)
        return

    experiment.archive()

    if experiment.is_stoppable:
        project = experiment.project
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_STOP,
            kwargs={
                'project_name': project.unique_name,
                'project_uuid': project.uuid.hex,
                'experiment_name': experiment.unique_name,
                'experiment_uuid': experiment.uuid.hex,
                'experiment_group_name': None,
                'experiment_group_uuid': None,
                'specification': experiment.config,
                'update_status': True,
                'collect_logs': False,
                'message': 'Experiment is scheduled for deletion.'
            },
            countdown=conf.get('GLOBAL_COUNTDOWN'))

    if immediate:
        celery_app.send_task(
            SchedulerCeleryTasks.DELETE_ARCHIVED_EXPERIMENT,
            kwargs={
                'experiment_id': experiment_id,
            },
            countdown=conf.get('GLOBAL_COUNTDOWN'))


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_STOP,
                 bind=True,
                 max_retries=3,
                 ignore_result=True)
def experiments_stop(self,
                     project_name,
                     project_uuid,
                     experiment_name,
                     experiment_group_name,
                     experiment_group_uuid,
                     experiment_uuid,
                     specification,
                     update_status=True,
                     collect_logs=True,
                     message=None):
    if collect_logs:
        try:
            collectors.logs_collect_experiment_jobs(experiment_uuid=experiment_uuid)
        except (OSError, VolumeNotFoundError, PolyaxonStoresException):
            _logger.warning('Scheduler could not collect '
                            'the logs for experiment `%s`.', experiment_name)
    if specification:
        specification = ExperimentSpecification.read(specification)
        deleted = experiment_scheduler.stop_experiment(
            project_name=project_name,
            project_uuid=project_uuid,
            experiment_name=experiment_name,
            experiment_group_name=experiment_group_name,
            experiment_group_uuid=experiment_group_uuid,
            experiment_uuid=experiment_uuid,
            specification=specification,
        )
    else:
        deleted = True

    if not deleted and self.request.retries < 2:
        _logger.info('Trying again to delete job `%s` in experiment.', experiment_name)
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)
        return

    if not update_status:
        return

    experiment = get_valid_experiment(experiment_uuid=experiment_uuid, include_deleted=True)
    if not experiment:
        _logger.info('Something went wrong, '
                     'the Experiment `%s` does not exist anymore.', experiment_uuid)
        return

    # Update experiment status to show that its stopped
    experiment.set_status(ExperimentLifeCycle.STOPPED,
                          message=message or 'Experiment was stopped')
