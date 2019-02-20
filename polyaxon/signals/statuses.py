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
from event_manager.events.build_job import (
    BUILD_JOB_CREATED,
    BUILD_JOB_DONE,
    BUILD_JOB_FAILED,
    BUILD_JOB_NEW_STATUS,
    BUILD_JOB_STOPPED,
    BUILD_JOB_SUCCEEDED
)
from event_manager.events.experiment import (
    EXPERIMENT_CREATED,
    EXPERIMENT_DONE,
    EXPERIMENT_FAILED,
    EXPERIMENT_NEW_STATUS,
    EXPERIMENT_STOPPED,
    EXPERIMENT_SUCCEEDED
)
from event_manager.events.experiment_group import (
    EXPERIMENT_GROUP_CREATED,
    EXPERIMENT_GROUP_DONE,
    EXPERIMENT_GROUP_NEW_STATUS,
    EXPERIMENT_GROUP_STOPPED
)
from event_manager.events.experiment_job import EXPERIMENT_JOB_NEW_STATUS
from event_manager.events.job import (
    JOB_CREATED,
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
    job.save(update_fields=['status', 'started_at', 'updated_at', 'finished_at'])
    auditor.record(event_type=BUILD_JOB_NEW_STATUS,
                   instance=job,
                   previous_status=previous_status)
    if instance.status == JobLifeCycle.CREATED:
        auditor.record(event_type=BUILD_JOB_CREATED, instance=job)
    elif instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=BUILD_JOB_STOPPED,
                       instance=job,
                       previous_status=previous_status)
    elif instance.status == JobLifeCycle.FAILED:
        auditor.record(event_type=BUILD_JOB_FAILED,
                       instance=job,
                       previous_status=previous_status)
    elif instance.status == JobLifeCycle.SUCCEEDED:
        auditor.record(event_type=BUILD_JOB_SUCCEEDED,
                       instance=job,
                       previous_status=previous_status)

    # handle done status
    if JobLifeCycle.is_done(instance.status):
        auditor.record(event_type=BUILD_JOB_DONE,
                       instance=job,
                       previous_status=previous_status)


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
    job.save(update_fields=['status', 'started_at', 'updated_at', 'finished_at'])
    auditor.record(event_type=JOB_NEW_STATUS,
                   instance=job,
                   previous_status=previous_status)

    if instance.status == JobLifeCycle.CREATED:
        auditor.record(event_type=JOB_CREATED, instance=job)
    elif instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=JOB_STOPPED,
                       instance=job,
                       previous_status=previous_status)
    elif instance.status == JobLifeCycle.FAILED:
        auditor.record(event_type=JOB_FAILED,
                       instance=job,
                       previous_status=previous_status)
    elif instance.status == JobLifeCycle.SUCCEEDED:
        auditor.record(event_type=JOB_SUCCEEDED,
                       instance=job,
                       previous_status=previous_status)
    if JobLifeCycle.is_done(instance.status):
        auditor.record(event_type=JOB_DONE,
                       instance=job,
                       previous_status=previous_status)


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
    job.save(update_fields=['status', 'started_at', 'updated_at', 'finished_at'])
    auditor.record(event_type=NOTEBOOK_NEW_STATUS,
                   instance=job,
                   previous_status=previous_status,
                   target='project')
    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=NOTEBOOK_STOPPED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')
    elif instance.status == JobLifeCycle.FAILED:
        auditor.record(event_type=NOTEBOOK_FAILED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')
    elif instance.status == JobLifeCycle.STOPPED:
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
    job.save(update_fields=['status', 'started_at', 'updated_at', 'finished_at'])
    auditor.record(event_type=TENSORBOARD_NEW_STATUS,
                   instance=job,
                   previous_status=previous_status,
                   target='project')
    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=TENSORBOARD_STOPPED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')
    elif instance.status == JobLifeCycle.FAILED:
        auditor.record(event_type=TENSORBOARD_FAILED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')
    elif instance.status == JobLifeCycle.STOPPED:
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
    experiment_group.save(update_fields=['status', 'started_at', 'updated_at', 'finished_at'])
    auditor.record(event_type=EXPERIMENT_GROUP_NEW_STATUS,
                   instance=experiment_group,
                   previous_status=previous_status)

    if instance.status == ExperimentGroupLifeCycle.CREATED:
        auditor.record(event_type=EXPERIMENT_GROUP_CREATED, instance=experiment_group)
    elif instance.status == ExperimentGroupLifeCycle.STOPPED:
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
    job.save(update_fields=['status', 'started_at', 'updated_at', 'finished_at'])

    # check if the new status is done to remove the containers from the monitors
    if job.is_done:
        from db.redis.containers import RedisJobContainers

        RedisJobContainers.remove_job(job.uuid.hex)

    # Check if we need to change the experiment status
    auditor.record(event_type=EXPERIMENT_JOB_NEW_STATUS, instance=job)


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
    experiment.save(update_fields=['status', 'started_at', 'updated_at', 'finished_at'])
    auditor.record(event_type=EXPERIMENT_NEW_STATUS,
                   instance=experiment,
                   previous_status=previous_status)

    if instance.status == ExperimentLifeCycle.CREATED:
        auditor.record(event_type=EXPERIMENT_CREATED, instance=experiment)
    elif instance.status == ExperimentLifeCycle.SUCCEEDED:
        # update all workers with succeeded status, since we will trigger a stop mechanism
        for job in experiment.jobs.all():
            if not job.is_done:
                job.set_status(JobLifeCycle.SUCCEEDED, message='Master is done.')
        auditor.record(event_type=EXPERIMENT_SUCCEEDED,
                       instance=experiment,
                       previous_status=previous_status)
    elif instance.status == ExperimentLifeCycle.FAILED:
        auditor.record(event_type=EXPERIMENT_FAILED,
                       instance=experiment,
                       previous_status=previous_status)
    elif instance.status == ExperimentLifeCycle.STOPPED:
        auditor.record(event_type=EXPERIMENT_STOPPED,
                       instance=experiment,
                       previous_status=previous_status)

    if ExperimentLifeCycle.is_done(instance.status):
        auditor.record(event_type=EXPERIMENT_DONE,
                       instance=experiment,
                       previous_status=previous_status)
