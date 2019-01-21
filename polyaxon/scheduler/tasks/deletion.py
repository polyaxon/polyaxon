from db.models.build_jobs import BuildJob
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.notebooks import NotebookJob
from db.models.projects import Project
from db.models.tensorboards import TensorboardJob
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks


@celery_app.task(name=SchedulerCeleryTasks.DELETE_ARCHIVED_PROJECT, ignore_result=True)
def delete_archived_project(project_id):
    try:
        Project.archived.get(id=project_id).delete()
    except Project.DoesNotExist:
        pass


@celery_app.task(name=SchedulerCeleryTasks.DELETE_ARCHIVED_EXPERIMENT_GROUP, ignore_result=True)
def delete_archived_experiment_group(group_id):
    try:
        ExperimentGroup.archived.get(id=group_id).delete()
    except ExperimentGroup.DoesNotExist:
        pass


@celery_app.task(name=SchedulerCeleryTasks.DELETE_ARCHIVED_EXPERIMENT, ignore_result=True)
def delete_archived_experiment(experiment_id):
    try:
        Experiment.archived.get(id=experiment_id).delete()
    except Experiment.DoesNotExist:
        pass


@celery_app.task(name=SchedulerCeleryTasks.DELETE_ARCHIVED_JOB, ignore_result=True)
def delete_archived_job(job_id):
    try:
        Job.archived.get(id=job_id).delete()
    except Job.DoesNotExist:
        pass


@celery_app.task(name=SchedulerCeleryTasks.DELETE_ARCHIVED_BUILD_JOB, ignore_result=True)
def delete_archived_build_job(job_id):
    try:
        BuildJob.archived.get(id=job_id).delete()
    except BuildJob.DoesNotExist:
        pass


@celery_app.task(name=SchedulerCeleryTasks.DELETE_ARCHIVED_NOTEBOOK_JOB, ignore_result=True)
def delete_archived_notebook_job(job_id):
    try:
        NotebookJob.archived.get(id=job_id).delete()
    except NotebookJob.DoesNotExist:
        pass


@celery_app.task(name=SchedulerCeleryTasks.DELETE_ARCHIVED_TENSORBOARD_JOB, ignore_result=True)
def delete_archived_tensorboard_job(job_id):
    try:
        TensorboardJob.archived.get(id=job_id).delete()
    except TensorboardJob.DoesNotExist:
        pass
