import logging

import conf
import workers

from db.getters.projects import get_valid_project
from lifecycles.experiment_groups import ExperimentGroupLifeCycle
from lifecycles.experiments import ExperimentLifeCycle
from lifecycles.jobs import JobLifeCycle
from options.registry.scheduler import SCHEDULER_GLOBAL_COUNTDOWN_DELAYED
from polyaxon.settings import SchedulerCeleryTasks

_logger = logging.getLogger(__name__)


@workers.app.task(name=SchedulerCeleryTasks.PROJECTS_SCHEDULE_DELETION, ignore_result=True)
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
        workers.send(
            SchedulerCeleryTasks.EXPERIMENTS_GROUP_STOP,
            kwargs={
                'experiment_group_id': group,
                'collect_logs': False,
                'message': message,
            })

    experiments = project.all_experiments.exclude(
        experiment_group__isnull=True,
        status__status__in=ExperimentLifeCycle.DONE_STATUS).distinct().iterator()
    for experiment in experiments:
        if experiment.is_stoppable:
            workers.send(
                SchedulerCeleryTasks.EXPERIMENTS_STOP,
                kwargs={
                    'project_name': experiment.project.unique_name,
                    'project_uuid': experiment.project.uuid.hex,
                    'experiment_name': experiment.unique_name,
                    'experiment_uuid': experiment.uuid.hex,
                    'experiment_group_name': None,
                    'experiment_group_uuid': None,
                    'specification': experiment.content,
                    'update_status': True,
                    'collect_logs': False,
                    'is_managed': experiment.is_managed,
                    'message': message,
                })
        else:
            # Update experiment status to show that its stopped
            experiment.set_status(status=ExperimentLifeCycle.STOPPED, message=message)

    jobs = project.all_jobs.exclude(status__status__in=JobLifeCycle.DONE_STATUS).distinct()
    for job in jobs.values_list('id', flat=True):
        workers.send(
            SchedulerCeleryTasks.JOBS_SCHEDULE_DELETION,
            kwargs={'job_id': job})

    builds = project.all_build_jobs.exclude(status__status__in=JobLifeCycle.DONE_STATUS).distinct()
    for build in builds.values_list('id', flat=True):
        workers.send(
            SchedulerCeleryTasks.BUILD_JOBS_SCHEDULE_DELETION,
            kwargs={'build_job_id': build})

    notebooks = project.all_notebook_jobs.exclude(
        status__status__in=JobLifeCycle.DONE_STATUS).distinct()
    for notebook in notebooks.values_list('id', flat=True):
        workers.send(
            SchedulerCeleryTasks.PROJECTS_NOTEBOOK_SCHEDULE_DELETION,
            kwargs={'notebook_job_id': notebook})

    tensorboards = project.all_tensorboard_jobs.exclude(
        status__status__in=JobLifeCycle.DONE_STATUS).distinct()
    for tensorboard in tensorboards.values_list('id', flat=True):
        workers.send(
            SchedulerCeleryTasks.TENSORBOARDS_SCHEDULE_DELETION,
            kwargs={'tensorboard_job_id': tensorboard})

    if immediate:
        workers.send(
            SchedulerCeleryTasks.DELETE_ARCHIVED_PROJECT,
            kwargs={
                'project_id': project_id,
            },
            countdown=conf.get(SCHEDULER_GLOBAL_COUNTDOWN_DELAYED))
