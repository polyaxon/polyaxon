import conf

from constants import content_types
from options.registry.scheduler import SCHEDULER_GLOBAL_COUNTDOWN
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks


def stop_experiment(experiment: 'Experiment', message: str = None):
    celery_app.send_task(
        SchedulerCeleryTasks.EXPERIMENTS_STOP,
        kwargs={
            'project_name': experiment.project.unique_name,
            'project_uuid': experiment.project.uuid.hex,
            'experiment_name': experiment.unique_name,
            'experiment_uuid': experiment.uuid.hex,
            'specification': experiment.content,
            'update_status': True,
            'collect_logs': True,
            'is_managed': experiment.is_managed,
            'message': message
        },
        countdown=conf.get(SCHEDULER_GLOBAL_COUNTDOWN))


def stop_experiment_group(group: 'ExperimentGroup', message: str = None):
    celery_app.send_task(
        SchedulerCeleryTasks.EXPERIMENTS_GROUP_STOP,
        kwargs={'experiment_group_id': group.id,
                'collect_logs': True,
                'message': message},
        countdown=conf.get(SCHEDULER_GLOBAL_COUNTDOWN))


def stop_job(job: 'Job', message: str = None):
    celery_app.send_task(
        SchedulerCeleryTasks.JOBS_STOP,
        kwargs={
            'project_name': job.project.unique_name,
            'project_uuid': job.project.uuid.hex,
            'job_name': job.unique_name,
            'job_uuid': job.uuid.hex,
            'update_status': False,
            'collect_logs': True,
            'is_managed': job.is_managed,
            'message': message
        },
        countdown=conf.get(SCHEDULER_GLOBAL_COUNTDOWN))


def stop_build_job(job: 'BuildJob', message: str = None):
    celery_app.send_task(
        SchedulerCeleryTasks.BUILD_JOBS_STOP,
        kwargs={
            'project_name': job.project.unique_name,
            'project_uuid': job.project.uuid.hex,
            'build_job_name': job.unique_name,
            'build_job_uuid': job.uuid.hex,
            'update_status': False,
            'collect_logs': True,
            'is_managed': job.is_managed,
            'message': message
        },
        countdown=conf.get(SCHEDULER_GLOBAL_COUNTDOWN))


def stop_notebook_job(job: 'NotebookJob', message: str = None):
    celery_app.send_task(
        SchedulerCeleryTasks.PROJECTS_NOTEBOOK_STOP,
        kwargs={
            'project_name': job.project.unique_name,
            'project_uuid': job.project.uuid.hex,
            'notebook_job_name': job.unique_name,
            'notebook_job_uuid': job.uuid.hex,
            'update_status': True,
            'collect_logs': False,
            'is_managed': job.is_managed,
            'message': message
        },
        countdown=conf.get(SCHEDULER_GLOBAL_COUNTDOWN))


def stop_tensorboard_job(job: 'TensorboardJob', message: str = None):
    celery_app.send_task(
        SchedulerCeleryTasks.TENSORBOARDS_STOP,
        kwargs={
            'project_name': job.project.unique_name,
            'project_uuid': job.project.uuid.hex,
            'tensorboard_job_name': job.unique_name,
            'tensorboard_job_uuid': job.uuid.hex,
            'update_status': True,
            'collect_logs': False,
            'is_managed': job.is_managed,
            'message': message
        },
        countdown=conf.get(SCHEDULER_GLOBAL_COUNTDOWN))


ENTITIES = {
    content_types.EXPERIMENT: stop_experiment,
    content_types.EXPERIMENT_GROUP: stop_experiment_group,
    content_types.BUILD_JOB: stop_build_job,
    content_types.JOB: stop_job,
    content_types.TENSORBOARD_JOB: stop_tensorboard_job,
    content_types.NOTEBOOK_JOB: stop_notebook_job,
}


def stop_entity(operation_run: 'OperationRun', message: str = None):
    ENTITIES[operation_run.operation.entity_type](operation_run.entity, message=message)
