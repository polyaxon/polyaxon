import logging

from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from db.getters.build_jobs import get_valid_build_job
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.notebooks import NotebookJob
from db.models.tensorboards import TensorboardJob
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks
from scheduler import dockerizer_scheduler

_logger = logging.getLogger('polyaxon.scheduler.build_jobs')


@celery_app.task(name=SchedulerCeleryTasks.BUILD_JOBS_START, ignore_result=True)
def build_jobs_start(build_job_id):
    build_job = get_valid_build_job(build_job_id=build_job_id)
    if not build_job:
        _logger.info('Something went wrong, '
                     'the BuildJob `%s` does not exist anymore.', build_job_id)
        return

    dockerizer_scheduler.start_dockerizer(build_job)


@celery_app.task(name=SchedulerCeleryTasks.BUILD_JOBS_STOP, ignore_result=True)
def build_jobs_stop(project_name, project_uuid, build_job_name, build_job_uuid, update_status=True):

    dockerizer_scheduler.stop_dockerizer(
        project_name=project_name,
        project_uuid=project_uuid,
        build_job_name=build_job_name,
        build_job_uuid=build_job_uuid)

    if not update_status:
        return

    build_job = get_valid_build_job(build_job_uuid=build_job_uuid)
    if not build_job:
        _logger.info('Something went wrong, '
                     'the BuildJob `%s` does not exist anymore.', build_job_uuid)
        return

    # Update build job status to show that its stopped
    build_job.set_status(status=JobLifeCycle.STOPPED,
                         message='BuildJob was stopped')


def notify_build_job_failed(build_job):
    message = 'Build failed'
    details = 'build_job_id: {}, {}'.format(build_job.id, build_job.uuid.hex)

    jobs = Job.objects.filter(build_job=build_job)
    for job in jobs:
        job.set_status(JobLifeCycle.FAILED, message=message, details=details)

    tensorboard_jobs = TensorboardJob.objects.filter(build_job=build_job)
    for tensorboard_job in tensorboard_jobs:
        tensorboard_job.set_status(JobLifeCycle.FAILED, message=message, details=details)

    notebook_jobs = NotebookJob.objects.filter(build_job=build_job)
    for notebook_job in notebook_jobs:
        notebook_job.set_status(JobLifeCycle.FAILED, message=message, details=details)

    experiments = Experiment.objects.filter(build_job=build_job)
    for experiment in experiments:
        experiment.set_status(ExperimentLifeCycle.FAILED, message=message, details=details)


def notify_build_job_stopped(build_job):
    message = 'Build stopped'
    details = 'build_job_id: {}, {}'.format(build_job.id, build_job.uuid.hex)

    jobs = Job.objects.filter(build_job=build_job)
    for job in jobs:
        job.set_status(JobLifeCycle.STOPPED, message=message, details=details)

    tensorboard_jobs = TensorboardJob.objects.filter(build_job=build_job)
    for tensorboard_job in tensorboard_jobs:
        tensorboard_job.set_status(JobLifeCycle.STOPPED, message=message, details=details)

    notebook_jobs = NotebookJob.objects.filter(build_job=build_job)
    for notebook_job in notebook_jobs:
        notebook_job.set_status(JobLifeCycle.STOPPED, message=message, details=details)

    experiments = Experiment.objects.filter(build_job=build_job)
    for experiment in experiments:
        experiment.set_status(ExperimentLifeCycle.STOPPED, message=message, details=details)


def notify_build_job_succeeded(build_job):
    job_ids = Job.objects.filter(build_job=build_job).values_list('id', flat=True)
    for job_id in job_ids:
        celery_app.send_task(
            SchedulerCeleryTasks.JOBS_START,
            kwargs={'job_id': job_id})

    tensorboard_job_ids = TensorboardJob.objects.filter(
        build_job=build_job).values_list('id', flat=True)
    for tensorboard_job_id in tensorboard_job_ids:
        celery_app.send_task(
            SchedulerCeleryTasks.TENSORBOARDS_START,
            kwargs={'tensorboard_job_id': tensorboard_job_id})

    notebook_job_ids = NotebookJob.objects.filter(
        build_job=build_job).values_list('id', flat=True)
    for notebook_job_id in notebook_job_ids:
        celery_app.send_task(
            SchedulerCeleryTasks.PROJECTS_NOTEBOOK_START,
            kwargs={'notebook_job_id': notebook_job_id})

    experiment_ids = Experiment.objects.filter(
        build_job=build_job).values_list('id', flat=True)
    for experiment_id in experiment_ids:
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_START,
            kwargs={'experiment_id': experiment_id})


@celery_app.task(name=SchedulerCeleryTasks.BUILD_JOBS_NOTIFY_DONE, ignore_result=True)
def build_jobs_notify_done(build_job_id):
    build_job = get_valid_build_job(build_job_id=build_job_id)
    if not build_job:
        _logger.info('Something went wrong, '
                     'the BuildJob `%s` does not exist anymore.', build_job_id)
        return

    # Notify all dependent jobs, notebooks, tensorboards, and experiments
    # Build job Failed -> Set status Failed with message: build failed
    if build_job.failed:
        notify_build_job_failed(build_job)
        return

    # Build job Stopped -> Stop the dependent jobs
    if build_job.stopped:
        notify_build_job_stopped(build_job)
        return

    # Build job Succeeded -> Start the dependent jobs
    if build_job.succeeded:
        notify_build_job_succeeded(build_job)


@celery_app.task(name=SchedulerCeleryTasks.BUILD_JOBS_SET_DOCKERFILE, ignore_result=True)
def build_jobs_set_dockerfile(build_job_uuid, dockerfile):
    build_job = get_valid_build_job(build_job_uuid=build_job_uuid)
    if not build_job:
        _logger.info('Something went wrong, '
                     'the BuildJob `%s` does not exist anymore.', build_job_uuid)
        return

    build_job.dockerfile = dockerfile
    build_job.save()
