import logging

from hestia.signal_decorators import ignore_raw, ignore_updates

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

import auditor

from constants.experiment_groups import ExperimentGroupLifeCycle
from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from db.models.build_jobs import BuildJobStatus
from db.models.experiment_groups import ExperimentGroupStatus
from db.models.experiment_jobs import ExperimentJobStatus
from db.models.experiments import ExperimentStatus
from db.models.jobs import JobStatus
from db.models.notebooks import NotebookJobStatus
from db.models.tensorboards import TensorboardJobStatus
from db.redis.tll import RedisTTL
from event_manager.events.build_job import (
    BUILD_JOB_DONE,
    BUILD_JOB_FAILED,
    BUILD_JOB_NEW_STATUS,
    BUILD_JOB_STOPPED,
    BUILD_JOB_SUCCEEDED
)
from event_manager.events.experiment import (
    EXPERIMENT_DONE,
    EXPERIMENT_FAILED,
    EXPERIMENT_NEW_STATUS,
    EXPERIMENT_STOPPED,
    EXPERIMENT_SUCCEEDED
)
from event_manager.events.experiment_group import (
    EXPERIMENT_GROUP_DONE,
    EXPERIMENT_GROUP_NEW_STATUS,
    EXPERIMENT_GROUP_STOPPED
)
from event_manager.events.job import (
    JOB_DONE,
    JOB_FAILED,
    JOB_NEW_STATUS,
    JOB_STOPPED,
    JOB_SUCCEEDED
)
from event_manager.events.notebook import (
    NOTEBOOK_FAILED,
    NOTEBOOK_NEW_STATUS,
    NOTEBOOK_STOPPED,
    NOTEBOOK_SUCCEEDED
)
from event_manager.events.tensorboard import (
    TENSORBOARD_FAILED,
    TENSORBOARD_NEW_STATUS,
    TENSORBOARD_STOPPED,
    TENSORBOARD_SUCCEEDED
)
from polyaxon.celery_api import celery_app
from polyaxon.settings import HPCeleryTasks, SchedulerCeleryTasks
from signals.run_time import (
    set_finished_at,
    set_job_finished_at,
    set_job_started_at,
    set_started_at
)

_logger = logging.getLogger('polyaxon.signals.statuses')


@receiver(post_save, sender=BuildJobStatus, dispatch_uid="build_job_status_post_save")
@ignore_updates
@ignore_raw
def build_job_status_post_save(sender, **kwargs):
    instance = kwargs['instance']
    job = instance.job
    previous_status = job.last_status

    # Update job last_status
    job.status = instance
    set_job_started_at(instance=job, status=instance.status)
    set_job_finished_at(instance=job, status=instance.status)
    job.save(update_fields=['status', 'started_at', 'finished_at'])
    auditor.record(event_type=BUILD_JOB_NEW_STATUS,
                   instance=job,
                   previous_status=previous_status)
    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=BUILD_JOB_STOPPED,
                       instance=job,
                       previous_status=previous_status)

    if instance.status == JobLifeCycle.FAILED:
        auditor.record(event_type=BUILD_JOB_FAILED,
                       instance=job,
                       previous_status=previous_status)

    if instance.status == JobLifeCycle.SUCCEEDED:
        auditor.record(event_type=BUILD_JOB_SUCCEEDED,
                       instance=job,
                       previous_status=previous_status)

    # Check if we need to schedule a job stop
    if instance.status in (JobLifeCycle.FAILED, JobLifeCycle.SUCCEEDED):
        _logger.info('The build job  `%s` failed or is done, '
                     'send signal to stop.', job.unique_name)
        # Schedule stop for this job
        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_STOP,
            kwargs={
                'project_name': job.project.unique_name,
                'project_uuid': job.project.uuid.hex,
                'build_job_name': job.unique_name,
                'build_job_uuid': job.uuid.hex,
                'update_status': False,
                'collect_logs': True,
            },
            countdown=RedisTTL.get_for_build(build_id=job.id))

    # handle done status
    if JobLifeCycle.is_done(instance.status):
        auditor.record(event_type=BUILD_JOB_DONE,
                       instance=job,
                       previous_status=previous_status)
        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_NOTIFY_DONE,
            kwargs={'build_job_id': job.id})


@receiver(post_save, sender=JobStatus, dispatch_uid="job_status_post_save")
@ignore_updates
@ignore_raw
def job_status_post_save(sender, **kwargs):
    instance = kwargs['instance']
    job = instance.job
    previous_status = job.last_status
    # Update job last_status
    job.status = instance
    set_job_started_at(instance=job, status=instance.status)
    set_job_finished_at(instance=job, status=instance.status)
    job.save(update_fields=['status'])
    auditor.record(event_type=JOB_NEW_STATUS,
                   instance=job,
                   previous_status=previous_status)
    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=JOB_STOPPED,
                       instance=job,
                       previous_status=previous_status)

    if instance.status == JobLifeCycle.FAILED:
        auditor.record(event_type=JOB_FAILED,
                       instance=job,
                       previous_status=previous_status)

    if instance.status == JobLifeCycle.SUCCEEDED:
        auditor.record(event_type=JOB_SUCCEEDED,
                       instance=job,
                       previous_status=previous_status)
    if JobLifeCycle.is_done(instance.status):
        auditor.record(event_type=JOB_DONE,
                       instance=job,
                       previous_status=previous_status)

    # Check if we need to schedule a job stop
    if not job.specification:
        return

    if instance.status in (JobLifeCycle.FAILED, JobLifeCycle.SUCCEEDED):
        _logger.debug('The build job  `%s` failed or is done, '
                      'send signal to stop.', job.unique_name)
        # Schedule stop for this job because
        celery_app.send_task(
            SchedulerCeleryTasks.JOBS_STOP,
            kwargs={
                'project_name': job.project.unique_name,
                'project_uuid': job.project.uuid.hex,
                'job_name': job.unique_name,
                'job_uuid': job.uuid.hex,
                'update_status': False,
                'collect_logs': True,
            },
            countdown=RedisTTL.get_for_job(job_id=job.id))


@receiver(post_save, sender=NotebookJobStatus, dispatch_uid="notebook_job_status_post_save")
@ignore_updates
@ignore_raw
def notebook_job_status_post_save(sender, **kwargs):
    instance = kwargs['instance']
    job = instance.job
    previous_status = job.last_status
    # Update job last_status
    job.status = instance
    set_job_started_at(instance=job, status=instance.status)
    set_job_finished_at(instance=job, status=instance.status)
    job.save(update_fields=['status', 'started_at', 'finished_at'])
    auditor.record(event_type=NOTEBOOK_NEW_STATUS,
                   instance=job,
                   previous_status=previous_status,
                   target='project')
    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=NOTEBOOK_STOPPED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')

    if instance.status == JobLifeCycle.FAILED:
        auditor.record(event_type=NOTEBOOK_FAILED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')
        # Schedule stop for this notebook
        celery_app.send_task(
            SchedulerCeleryTasks.PROJECTS_NOTEBOOK_STOP,
            kwargs={
                'project_name': job.project.unique_name,
                'project_uuid': job.project.uuid.hex,
                'notebook_job_name': job.unique_name,
                'notebook_job_uuid': job.uuid.hex,
                'update_status': False
            })

    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=NOTEBOOK_SUCCEEDED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')


@receiver(post_save, sender=TensorboardJobStatus, dispatch_uid="tensorboard_job_status_post_save")
@ignore_updates
@ignore_raw
def tensorboard_job_status_post_save(sender, **kwargs):
    instance = kwargs['instance']
    job = instance.job
    previous_status = job.last_status
    # Update job last_status
    job.status = instance
    set_job_started_at(instance=job, status=instance.status)
    set_job_finished_at(instance=job, status=instance.status)
    job.save(update_fields=['status', 'started_at', 'finished_at'])
    auditor.record(event_type=TENSORBOARD_NEW_STATUS,
                   instance=job,
                   previous_status=previous_status,
                   target='project')
    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=TENSORBOARD_STOPPED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')

    if instance.status == JobLifeCycle.FAILED:
        auditor.record(event_type=TENSORBOARD_FAILED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')
        # Schedule stop for this tensorboard
        celery_app.send_task(
            SchedulerCeleryTasks.TENSORBOARDS_STOP,
            kwargs={
                'project_name': job.project.unique_name,
                'project_uuid': job.project.uuid.hex,
                'tensorboard_job_name': job.unique_name,
                'tensorboard_job_uuid': job.uuid.hex,
                'update_status': False
            })

    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=TENSORBOARD_SUCCEEDED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')


@receiver(post_save, sender=ExperimentGroupStatus, dispatch_uid="experiment_group_status_post_save")
@ignore_updates
@ignore_raw
def experiment_group_status_post_save(sender, **kwargs):
    instance = kwargs['instance']
    experiment_group = instance.experiment_group
    previous_status = experiment_group.last_status

    # update experiment last_status
    experiment_group.status = instance
    if instance.status == ExperimentGroupLifeCycle.RUNNING:
        experiment_group.started_at = now()

    set_started_at(instance=experiment_group,
                   status=instance.status,
                   starting_statuses=[ExperimentGroupLifeCycle.RUNNING])
    set_finished_at(instance=experiment_group,
                    status=instance.status,
                    is_done=ExperimentGroupLifeCycle.is_done)
    experiment_group.save(update_fields=['status', 'started_at', 'finished_at'])
    auditor.record(event_type=EXPERIMENT_GROUP_NEW_STATUS,
                   instance=experiment_group,
                   previous_status=previous_status)

    if instance.status == ExperimentGroupLifeCycle.STOPPED:
        auditor.record(event_type=EXPERIMENT_GROUP_STOPPED,
                       instance=experiment_group,
                       previous_status=previous_status)

    if ExperimentGroupLifeCycle.is_done(instance.status):
        auditor.record(event_type=EXPERIMENT_GROUP_DONE,
                       instance=experiment_group,
                       previous_status=previous_status)


@receiver(post_save, sender=ExperimentJobStatus, dispatch_uid="experiment_job_status_post_save")
@ignore_updates
@ignore_raw
def experiment_job_status_post_save(sender, **kwargs):
    instance = kwargs['instance']
    job = instance.job

    job.status = instance
    set_job_started_at(instance=job, status=instance.status)
    set_job_finished_at(instance=job, status=instance.status)
    job.save(update_fields=['status', 'started_at', 'finished_at'])

    # check if the new status is done to remove the containers from the monitors
    if job.is_done:
        from db.redis.containers import RedisJobContainers

        RedisJobContainers.remove_job(job.uuid.hex)

    # Check if we need to change the experiment status
    experiment = instance.job.experiment
    if experiment.is_done:
        return

    celery_app.send_task(
        SchedulerCeleryTasks.EXPERIMENTS_CHECK_STATUS,
        kwargs={'experiment_id': experiment.id},
        countdown=1)


@receiver(post_save, sender=ExperimentStatus, dispatch_uid="experiment_status_post_save")
@ignore_updates
@ignore_raw
def experiment_status_post_save(sender, **kwargs):
    instance = kwargs['instance']
    experiment = instance.experiment
    previous_status = experiment.last_status

    # update experiment last_status
    experiment.status = instance
    set_started_at(instance=experiment,
                   status=instance.status,
                   starting_statuses=[ExperimentLifeCycle.STARTING, ExperimentLifeCycle.RUNNING],
                   running_status=ExperimentLifeCycle.RUNNING)
    set_finished_at(instance=experiment,
                    status=instance.status,
                    is_done=ExperimentLifeCycle.is_done)
    experiment.save(update_fields=['status', 'started_at', 'finished_at'])
    auditor.record(event_type=EXPERIMENT_NEW_STATUS,
                   instance=experiment,
                   previous_status=previous_status)

    if instance.status == ExperimentLifeCycle.SUCCEEDED:
        # update all workers with succeeded status, since we will trigger a stop mechanism
        for job in experiment.jobs.all():
            if not job.is_done:
                job.set_status(JobLifeCycle.SUCCEEDED, message='Master is done.')
        auditor.record(event_type=EXPERIMENT_SUCCEEDED,
                       instance=experiment,
                       previous_status=previous_status)
    if instance.status == ExperimentLifeCycle.FAILED:
        auditor.record(event_type=EXPERIMENT_FAILED,
                       instance=experiment,
                       previous_status=previous_status)

    if instance.status == ExperimentLifeCycle.STOPPED:
        auditor.record(event_type=EXPERIMENT_STOPPED,
                       instance=experiment,
                       previous_status=previous_status)

    if ExperimentLifeCycle.is_done(instance.status):
        auditor.record(event_type=EXPERIMENT_DONE,
                       instance=experiment,
                       previous_status=previous_status)
        # Check if it's part of an experiment group, and start following tasks
        if not experiment.is_independent:
            celery_app.send_task(
                HPCeleryTasks.HP_START,
                kwargs={'experiment_group_id': experiment.experiment_group.id},
                countdown=1)


@receiver(post_save, sender=ExperimentStatus, dispatch_uid="handle_new_experiment_status")
@ignore_raw
def handle_new_experiment_status(sender, **kwargs):
    instance = kwargs['instance']
    experiment = instance.experiment
    if not experiment.specification:
        return

    stop_condition = (
        instance.status in (ExperimentLifeCycle.FAILED, ExperimentLifeCycle.SUCCEEDED) and
        experiment.jobs.count() > 0
    )
    if stop_condition:
        _logger.debug('One of the workers failed or Master for experiment `%s` is done, '
                      'send signal to other workers to stop.', experiment.unique_name)
        # Schedule stop for this experiment because other jobs may be still running
        group = experiment.experiment_group
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_STOP,
            kwargs={
                'project_name': experiment.project.unique_name,
                'project_uuid': experiment.project.uuid.hex,
                'experiment_name': experiment.unique_name,
                'experiment_uuid': experiment.uuid.hex,
                'experiment_group_name': group.unique_name if group else None,
                'experiment_group_uuid': group.uuid.hex if group else None,
                'specification': experiment.config,
                'update_status': False,
                'collect_logs': True,
            },
            countdown=RedisTTL.get_for_experiment(experiment_id=experiment.id))
