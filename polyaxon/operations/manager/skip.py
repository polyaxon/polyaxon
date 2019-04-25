import conf

from constants import content_types
from lifecycles.operations import OperationStatuses
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks


def skip_experiment(experiment: 'Experiment', message: str = None):
    experiment.set_status(OperationStatuses.SKIPPED)
    celery_app.send_task(
        SchedulerCeleryTasks.EXPERIMENTS_STOP,
        kwargs={
            'project_name': experiment.project.unique_name,
            'project_uuid': experiment.project.uuid.hex,
            'experiment_name': experiment.unique_name,
            'experiment_uuid': experiment.uuid.hex,
            'specification': experiment.config,
            'update_status': False,
            'collect_logs': False,
            'is_managed': experiment.is_managed,
            'message': message
        },
        countdown=conf.get('GLOBAL_COUNTDOWN'))


def skip_experiment_group(group: 'ExperimentGroup', message: str = None):
    group.set_status(OperationStatuses.SKIPPED)
    celery_app.send_task(
        SchedulerCeleryTasks.EXPERIMENTS_GROUP_STOP_EXPERIMENTS,
        kwargs={'experiment_group_id': group.id,
                'pending': False,
                'collect_logs': False,
                'update_status': False,
                'message': message},
        countdown=conf.get('GLOBAL_COUNTDOWN'))


def skip_job(job: 'Job', message: str = None):
    job.set_status(OperationStatuses.SKIPPED)
    celery_app.send_task(
        SchedulerCeleryTasks.JOBS_STOP,
        kwargs={
            'project_name': job.project.unique_name,
            'project_uuid': job.project.uuid.hex,
            'job_name': job.unique_name,
            'job_uuid': job.uuid.hex,
            'update_status': False,
            'collect_logs': False,
            'is_managed': job.is_managed,
            'message': message
        },
        countdown=conf.get('GLOBAL_COUNTDOWN'))


def skip_build_job(job: 'BuildJob', message: str = None):
    job.set_status(OperationStatuses.SKIPPED)
    celery_app.send_task(
        SchedulerCeleryTasks.BUILD_JOBS_STOP,
        kwargs={
            'project_name': job.project.unique_name,
            'project_uuid': job.project.uuid.hex,
            'build_job_name': job.unique_name,
            'build_job_uuid': job.uuid.hex,
            'update_status': False,
            'collect_logs': False,
            'is_managed': job.is_managed,
            'message': message
        },
        countdown=conf.get('GLOBAL_COUNTDOWN'))


def skip_notebook_job(job: 'NotebookJob', message: str = None):
    job.set_status(OperationStatuses.SKIPPED)
    celery_app.send_task(
        SchedulerCeleryTasks.PROJECTS_NOTEBOOK_STOP,
        kwargs={
            'project_name': job.project.unique_name,
            'project_uuid': job.project.uuid.hex,
            'notebook_job_name': job.unique_name,
            'notebook_job_uuid': job.uuid.hex,
            'update_status': False,
            'collect_logs': False,
            'is_managed': job.is_managed,
            'message': message
        },
        countdown=conf.get('GLOBAL_COUNTDOWN'))


def skip_tensorboard_job(job: 'TensorboardJob', message: str = None):
    job.set_status(OperationStatuses.SKIPPED)
    celery_app.send_task(
        SchedulerCeleryTasks.TENSORBOARDS_STOP,
        kwargs={
            'project_name': job.project.unique_name,
            'project_uuid': job.project.uuid.hex,
            'tensorboard_job_name': job.unique_name,
            'tensorboard_job_uuid': job.uuid.hex,
            'update_status': False,
            'collect_logs': False,
            'is_managed': job.is_managed,
            'message': message
        },
        countdown=conf.get('GLOBAL_COUNTDOWN'))


ENTITIES = {
    content_types.EXPERIMENT: skip_experiment,
    content_types.EXPERIMENT_GROUP: skip_experiment_group,
    content_types.BUILD_JOB: skip_build_job,
    content_types.JOB: skip_job,
    content_types.TENSORBOARD_JOB: skip_tensorboard_job,
    content_types.NOTEBOOK_JOB: skip_notebook_job,
}


def skip_entity(operation_run: 'OperationRun', message: str = None):
    ENTITIES[operation_run.operation.entity_type](operation_run.entity, message=message)
