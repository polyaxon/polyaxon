import workers

from db.models.build_jobs import BuildJob
from db.models.experiments import Experiment
from db.models.jobs import Job
from lifecycles.experiments import ExperimentLifeCycle
from lifecycles.jobs import JobLifeCycle
from polyaxon.settings import CronsCeleryTasks, SchedulerCeleryTasks


@workers.app.task(name=CronsCeleryTasks.HEARTBEAT_EXPERIMENTS, ignore_result=True)
def heartbeat_experiments() -> None:
    experiments = Experiment.objects.filter(status__status__in=ExperimentLifeCycle.HEARTBEAT_STATUS)
    for experiment in experiments.values_list('id', flat=True):
        workers.send(
            SchedulerCeleryTasks.EXPERIMENTS_CHECK_HEARTBEAT,
            kwargs={'experiment_id': experiment})


@workers.app.task(name=CronsCeleryTasks.HEARTBEAT_JOBS, ignore_result=True)
def heartbeat_jobs() -> None:
    jobs = Job.objects.filter(status__status__in=JobLifeCycle.HEARTBEAT_STATUS)
    for job in jobs.values_list('id', flat=True):
        workers.send(
            SchedulerCeleryTasks.JOBS_CHECK_HEARTBEAT,
            kwargs={'job_id': job})


@workers.app.task(name=CronsCeleryTasks.HEARTBEAT_BUILDS, ignore_result=True)
def heartbeat_builds() -> None:
    build_jobs = BuildJob.objects.filter(status__status__in=JobLifeCycle.HEARTBEAT_STATUS)
    for build_job in build_jobs.values_list('id', flat=True):
        workers.send(
            SchedulerCeleryTasks.BUILD_JOBS_CHECK_HEARTBEAT,
            kwargs={'build_job_id': build_job})
