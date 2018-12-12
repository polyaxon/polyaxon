from crons.tasks.utils import get_date_check
from db.models.build_jobs import BuildJob
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.notebooks import NotebookJob
from db.models.projects import Project
from db.models.tensorboards import TensorboardJob
from polyaxon.celery_api import celery_app
from polyaxon.settings import CleaningIntervals, CronsCeleryTasks


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_PROJECTS, ignore_result=True)
def delete_archived_projects():
    last_date = get_date_check(days=CleaningIntervals.ARCHIVED)
    ids = Project.archived.filter(updated_at__lte=last_date).values_list('id', flat=True)
    for _id in ids:
        celery_app.send_task(
            CronsCeleryTasks.DELETE_ARCHIVED_PROJECT,
            kwargs={'project_id': _id})


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_PROJECT, ignore_result=True)
def delete_archived_project(project_id):
    try:
        Project.archived.get(id=project_id).delete()
    except Project.DoesNotExist:
        pass


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_EXPERIMENT_GROUPS, ignore_result=True)
def delete_archived_experiment_groups():
    last_date = get_date_check(days=CleaningIntervals.ARCHIVED)
    groups = ExperimentGroup.archived.filter(
        # We only check values that will not be deleted by the archived projects
        project__deleted=False,
        updated_at__lte=last_date).values_list('id', flat=True)
    for group in groups:
        celery_app.send_task(
            CronsCeleryTasks.DELETE_ARCHIVED_EXPERIMENT_GROUP,
            kwargs={'group_id': group})


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_EXPERIMENT_GROUP, ignore_result=True)
def delete_archived_experiment_group(group_id):
    try:
        ExperimentGroup.archived.get(id=group_id).delete()
    except ExperimentGroup.DoesNotExist:
        pass


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_EXPERIMENTS, ignore_result=True)
def delete_archived_experiments():
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
            CronsCeleryTasks.DELETE_ARCHIVED_EXPERIMENT,
            kwargs={'experiment_id': _id})


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_EXPERIMENT, ignore_result=True)
def delete_archived_experiment(experiment_id):
    try:
        Experiment.archived.get(id=experiment_id).delete()
    except Experiment.DoesNotExist:
        pass


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_JOBS, ignore_result=True)
def delete_archived_jobs():
    last_date = get_date_check(days=CleaningIntervals.ARCHIVED)
    ids = Job.archived.filter(
        # We only check values that will not be deleted by the archived projects
        project__deleted=False,
        updated_at__lte=last_date).values_list('id', flat=True)
    for _id in ids:
        celery_app.send_task(
            CronsCeleryTasks.DELETE_ARCHIVED_JOB,
            kwargs={'job_id': _id})


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_JOB, ignore_result=True)
def delete_archived_job(job_id):
    try:
        Job.archived.get(id=job_id).delete()
    except Job.DoesNotExist:
        pass


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_BUILD_JOBS, ignore_result=True)
def delete_archived_build_jobs():
    last_date = get_date_check(days=CleaningIntervals.ARCHIVED)
    ids = BuildJob.archived.filter(
        # We only check values that will not be deleted by the archived projects
        project__deleted=False,
        updated_at__lte=last_date).values_list('id', flat=True)
    for _id in ids:
        celery_app.send_task(
            CronsCeleryTasks.DELETE_ARCHIVED_BUILD_JOB,
            kwargs={'job_id': _id})


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_BUILD_JOB, ignore_result=True)
def delete_archived_build_job(job_id):
    try:
        BuildJob.archived.get(id=job_id).delete()
    except BuildJob.DoesNotExist:
        pass


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_NOTEBOOK_JOBS, ignore_result=True)
def delete_archived_notebook_jobs():
    last_date = get_date_check(days=CleaningIntervals.ARCHIVED)
    ids = NotebookJob.archived.filter(
        # We only check values that will not be deleted by the archived projects
        project__deleted=False,
        updated_at__lte=last_date).values_list('id', flat=True)
    for _id in ids:
        celery_app.send_task(
            CronsCeleryTasks.DELETE_ARCHIVED_NOTEBOOK_JOB,
            kwargs={'job_id': _id})


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_NOTEBOOK_JOB, ignore_result=True)
def delete_archived_notebook_job(job_id):
    try:
        NotebookJob.archived.get(id=job_id).delete()
    except NotebookJob.DoesNotExist:
        pass


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_TENSORBOARD_JOBS, ignore_result=True)
def delete_archived_tensorboard_jobs():
    last_date = get_date_check(days=CleaningIntervals.ARCHIVED)
    ids = TensorboardJob.archived.filter(
        # We only check values that will not be deleted by the archived projects
        project__deleted=False,
        updated_at__lte=last_date).values_list('id', flat=True)
    for _id in ids:
        celery_app.send_task(
            CronsCeleryTasks.DELETE_ARCHIVED_TENSORBOARD_JOB,
            kwargs={'job_id': _id})


@celery_app.task(name=CronsCeleryTasks.DELETE_ARCHIVED_TENSORBOARD_JOB, ignore_result=True)
def delete_archived_tensorboard_job(job_id):
    try:
        TensorboardJob.archived.get(id=job_id).delete()
    except TensorboardJob.DoesNotExist:
        pass
