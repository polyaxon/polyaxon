import logging

import conf

from constants.experiment_groups import ExperimentGroupLifeCycle
from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from db.getters.projects import get_valid_project
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks

_logger = logging.getLogger(__name__)


@celery_app.task(name=SchedulerCeleryTasks.PROJECTS_SCHEDULE_DELETION, ignore_result=True)
def projects_schedule_deletion(project_id, immediate=False):
    project = get_valid_project(project_id=project_id, include_deleted=True)
    if not project:
        # No need to check this project
        return

    project.archive()
    message = 'Project is scheduled for deletion.'

    groups = project.all_experiment_groups.exclude(
        status__status__in=ExperimentGroupLifeCycle.DONE_STATUS).distinct()
    for group in groups.values_list('id', flat=True):
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_GROUP_STOP,
            kwargs={
                'experiment_group_id': group,
                'collect_logs': False,
                'message': message,
            },
            countdown=conf.get('GLOBAL_COUNTDOWN'))

    experiments = project.all_experiments.exclude(
        experiment_group__isnull=True,
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
                    'experiment_group_name': None,
                    'experiment_group_uuid': None,
                    'specification': experiment.config,
                    'update_status': True,
                    'collect_logs': False,
                    'message': message,
                },
                countdown=conf.get('GLOBAL_COUNTDOWN'))
        else:
            # Update experiment status to show that its stopped
            experiment.set_status(status=ExperimentLifeCycle.STOPPED, message=message)

    jobs = project.all_jobs.exclude(status__status__in=JobLifeCycle.DONE_STATUS).distinct()
    for job in jobs.values_list('id', flat=True):
        celery_app.send_task(
            SchedulerCeleryTasks.JOBS_SCHEDULE_DELETION,
            kwargs={'job_id': job},
            countdown=conf.get('GLOBAL_COUNTDOWN'))

    builds = project.all_build_jobs.exclude(status__status__in=JobLifeCycle.DONE_STATUS).distinct()
    for build in builds.values_list('id', flat=True):
        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_SCHEDULE_DELETION,
            kwargs={'build_job_id': build},
            countdown=conf.get('GLOBAL_COUNTDOWN'))

    notebooks = project.all_notebook_jobs.exclude(
        status__status__in=JobLifeCycle.DONE_STATUS).distinct()
    for notebook in notebooks.values_list('id', flat=True):
        celery_app.send_task(
            SchedulerCeleryTasks.PROJECTS_NOTEBOOK_SCHEDULE_DELETION,
            kwargs={'notebook_job_id': notebook},
            countdown=conf.get('GLOBAL_COUNTDOWN'))

    tensorboards = project.all_tensorboard_jobs.exclude(
        status__status__in=JobLifeCycle.DONE_STATUS).distinct()
    for tensorboard in tensorboards.values_list('id', flat=True):
        celery_app.send_task(
            SchedulerCeleryTasks.TENSORBOARDS_SCHEDULE_DELETION,
            kwargs={'tensorboard_job_id': tensorboard},
            countdown=conf.get('GLOBAL_COUNTDOWN'))

    if immediate:
        celery_app.send_task(
            SchedulerCeleryTasks.DELETE_ARCHIVED_PROJECT,
            kwargs={
                'project_id': project_id,
            },
            countdown=conf.get('GLOBAL_COUNTDOWN'))
