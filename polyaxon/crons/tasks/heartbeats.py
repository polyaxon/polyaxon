from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from db.models.build_jobs import BuildJob
from db.models.experiments import Experiment
from db.models.jobs import Job
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import CronsCeleryTasks, SchedulerCeleryTasks


@celery_app.task(name=CronsCeleryTasks.HEARTBEAT_EXPERIMENTS, ignore_result=True)
def heartbeat_experiments():
    created_and_done = (
        ExperimentLifeCycle.DONE_STATUS |
        {ExperimentLifeCycle.CREATED, ExperimentLifeCycle.BUILDING})
    experiments = Experiment.objects.exclude(status__status__in=created_and_done)
    for experiment in experiments:
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_CHECK_HEARTBEAT,
            kwargs={'experiment_id': experiment.id})


@celery_app.task(name=CronsCeleryTasks.HEARTBEAT_JOBS, ignore_result=True)
def heartbeat_jobs():
    created_and_done = JobLifeCycle.DONE_STATUS | JobLifeCycle.STARTING_STATUS
    jobs = Job.objects.exclude(status__status__in=created_and_done)
    for job in jobs:
        celery_app.send_task(
            SchedulerCeleryTasks.JOBS_CHECK_HEARTBEAT,
            kwargs={'job_id': job.id})


@celery_app.task(name=CronsCeleryTasks.HEARTBEAT_BUILDS, ignore_result=True)
def heartbeat_builds():
    created_and_done = JobLifeCycle.DONE_STATUS | JobLifeCycle.STARTING_STATUS
    build_jobs = BuildJob.objects.exclude(status__status__in=created_and_done)
    for build_job in build_jobs:
        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_CHECK_HEARTBEAT,
            kwargs={'build_job_id': build_job.id})
