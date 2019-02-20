import conf

from crons.tasks.utils import get_date_check
from db.models.build_jobs import BuildJob
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.notebooks import NotebookJob
from db.models.projects import Project
from db.models.tensorboards import TensorboardJob
from polyaxon.celery_api import celery_app
from polyaxon.settings import CleaningIntervals, CronsCeleryTasks, SchedulerCeleryTasks


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_PROJECTS, ignore_result=True)
def delete_archived_projects() -> None:
    last_date = get_date_check(days=CleaningIntervals.ARCHIVED)
    ids = Project.archived.filter(updated_at__lte=last_date).values_list('id', flat=True)
    for _id in ids:
        celery_app.send_task(
            SchedulerCeleryTasks.DELETE_ARCHIVED_PROJECT,
            kwargs={'project_id': _id},
            countdown=conf.get('GLOBAL_COUNTDOWN'))


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_EXPERIMENT_GROUPS, ignore_result=True)
def delete_archived_experiment_groups() -> None:
    last_date = get_date_check(days=CleaningIntervals.ARCHIVED)
    groups = ExperimentGroup.archived.filter(
        # We only check values that will not be deleted by the archived projects
        project__deleted=False,
        updated_at__lte=last_date).values_list('id', flat=True)
    for group in groups:
        celery_app.send_task(
            SchedulerCeleryTasks.DELETE_ARCHIVED_EXPERIMENT_GROUP,
            kwargs={'group_id': group},
            countdown=conf.get('GLOBAL_COUNTDOWN'))


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_EXPERIMENTS, ignore_result=True)
def delete_archived_experiments() -> None:
    last_date = get_date_check(days=CleaningIntervals.ARCHIVED)
    ids = Experiment.archived.filter(
        # We only check values that will not be deleted by the archived projects
        project__deleted=False,
        updated_at__lte=last_date).exclude(
        # We exclude as well experiments that will be deleted in groups
        experiment_group__deleted=False,
    ).values_list('id', flat=True)
    for _id in ids:
        celery_app.send_task(
            SchedulerCeleryTasks.DELETE_ARCHIVED_EXPERIMENT,
            kwargs={'experiment_id': _id},
            countdown=conf.get('GLOBAL_COUNTDOWN'))


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_JOBS, ignore_result=True)
def delete_archived_jobs() -> None:
    last_date = get_date_check(days=CleaningIntervals.ARCHIVED)
    ids = Job.archived.filter(
        # We only check values that will not be deleted by the archived projects
        project__deleted=False,
        updated_at__lte=last_date).values_list('id', flat=True)
    for _id in ids:
        celery_app.send_task(
            SchedulerCeleryTasks.DELETE_ARCHIVED_JOB,
            kwargs={'job_id': _id},
            countdown=conf.get('GLOBAL_COUNTDOWN'))


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_BUILD_JOBS, ignore_result=True)
def delete_archived_build_jobs() -> None:
    last_date = get_date_check(days=CleaningIntervals.ARCHIVED)
    ids = BuildJob.archived.filter(
        # We only check values that will not be deleted by the archived projects
        project__deleted=False,
        updated_at__lte=last_date).values_list('id', flat=True)
    for _id in ids:
        celery_app.send_task(
            SchedulerCeleryTasks.DELETE_ARCHIVED_BUILD_JOB,
            kwargs={'job_id': _id},
            countdown=conf.get('GLOBAL_COUNTDOWN'))


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_NOTEBOOK_JOBS, ignore_result=True)
def delete_archived_notebook_jobs() -> None:
    last_date = get_date_check(days=CleaningIntervals.ARCHIVED)
    ids = NotebookJob.archived.filter(
        # We only check values that will not be deleted by the archived projects
        project__deleted=False,
        updated_at__lte=last_date).values_list('id', flat=True)
    for _id in ids:
        celery_app.send_task(
            SchedulerCeleryTasks.DELETE_ARCHIVED_NOTEBOOK_JOB,
            kwargs={'job_id': _id},
            countdown=conf.get('GLOBAL_COUNTDOWN'))


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_TENSORBOARD_JOBS, ignore_result=True)
def delete_archived_tensorboard_jobs() -> None:
    last_date = get_date_check(days=CleaningIntervals.ARCHIVED)
    ids = TensorboardJob.archived.filter(
        # We only check values that will not be deleted by the archived projects
        project__deleted=False,
        updated_at__lte=last_date).values_list('id', flat=True)
    for _id in ids:
        celery_app.send_task(
            SchedulerCeleryTasks.DELETE_ARCHIVED_TENSORBOARD_JOB,
            kwargs={'job_id': _id},
            countdown=conf.get('GLOBAL_COUNTDOWN'))
