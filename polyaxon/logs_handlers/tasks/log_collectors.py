from db.models.build_jobs import BuildJob
from db.models.experiment_jobs import ExperimentJob
from db.models.experiments import Experiment
from db.models.jobs import Job
from logs_handlers.log_queries.build_job import process_logs as process_build_logs
from logs_handlers.log_queries.experiment import (
    process_logs as process_experiment_logs,
    process_experiment_jobs_logs,
)
from logs_handlers.log_queries.experiment_job import process_logs as process_experiment_job_logs
from logs_handlers.log_queries.job import process_logs as process_job_logs
from polyaxon.celery_api import celery_app
from polyaxon.config_settings import SchedulerCeleryTasks


@celery_app.task(name=SchedulerCeleryTasks.LOGS_COLLECT_EXPERIMENT_JOBS, ignore_result=True)
def logs_collect_experiment_jobs(experiment_uuid):
    try:
        experiment = Experiment.objects.filter(uuid=experiment_uuid).get()
    except Experiment.DoesNotExist:
        return

    if experiment.jobs.coutn() > 0:
        process_experiment_jobs_logs(experiment=experiment, temp=False)
    else:
        process_experiment_logs(experiment=experiment, temp=False)


@celery_app.task(name=SchedulerCeleryTasks.LOGS_COLLECT_EXPERIMENT_JOB, ignore_result=True)
def logs_collect_experiment_job(experiment_job_uuid):
    try:
        experiment_job = ExperimentJob.objects.filter(
            uuid=experiment_job_uuid).select_related('experiment').get()
        experiment = experiment_job.experiment
    except (ExperimentJob.DoesNotExist, Experiment.DoesNotExist):
        return

    if experiment.jobs.coutn() > 0:
        process_experiment_job_logs(experiment_job=experiment_job, temp=False)
    else:
        process_experiment_logs(experiment=experiment, temp=False)


@celery_app.task(name=SchedulerCeleryTasks.LOGS_COLLECT_JOB, ignore_result=True)
def logs_collect_job(job_uuid):
    try:
        job = Job.objects.filter(uuid=job_uuid).get()
    except Job.DoesNotExist:
        return
    process_job_logs(job=job, temp=False)


@celery_app.task(name=SchedulerCeleryTasks.LOGS_COLLECT_BUILD_JOB, ignore_result=True)
def logs_collect_build_job(build_uuid):
    try:
        build = BuildJob.objects.filter(uuid=build_uuid).get()
    except BuildJob.DoesNotExist:
        return
    process_build_logs(build=build, temp=False)
