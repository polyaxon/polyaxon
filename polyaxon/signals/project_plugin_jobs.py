import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

import auditor

from constants.jobs import JobLifeCycle
from db.models.plugins import NotebookJob, NotebookJobStatus, TensorboardJob, TensorboardJobStatus
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
from libs.decorators import ignore_raw, ignore_updates, ignore_updates_pre
from libs.repos.utils import assign_code_reference

logger = logging.getLogger('polyaxon.plugins')


@receiver(pre_save, sender=TensorboardJob, dispatch_uid="tensorboard_job_saved")
@ignore_updates_pre
@ignore_raw
def add_tensorboard_code_reference(sender, **kwargs):
    assign_code_reference(kwargs['instance'])


@receiver(post_save, sender=TensorboardJob, dispatch_uid="tensorboard_job_saved")
@ignore_updates
@ignore_raw
def new_tensorboard_job(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(status=JobLifeCycle.CREATED)


@receiver(pre_save, sender=NotebookJob, dispatch_uid="notebook_job_saved")
@ignore_updates_pre
@ignore_raw
def add_notebook_code_reference(sender, **kwargs):
    assign_code_reference(kwargs['instance'])


@receiver(post_save, sender=NotebookJob, dispatch_uid="notebook_job_saved")
@ignore_updates
@ignore_raw
def new_notebook_job(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(status=JobLifeCycle.CREATED)


@receiver(post_save, sender=TensorboardJobStatus, dispatch_uid="new_tensorboard_job_status_saved")
@ignore_updates
@ignore_raw
def new_tensorboard_job_status(sender, **kwargs):
    instance = kwargs['instance']
    job = instance.job
    previous_status = job.last_status
    # Update job last_status
    job.status = instance
    job.save()
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

    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=TENSORBOARD_SUCCEEDED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')


@receiver(post_save, sender=NotebookJobStatus, dispatch_uid="new_notebook_job_status_saved")
@ignore_updates
@ignore_raw
def new_notebook_job_status(sender, **kwargs):
    instance = kwargs['instance']
    job = instance.job
    previous_status = job.last_status
    # Update job last_status
    job.status = instance
    job.save()
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

    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=NOTEBOOK_SUCCEEDED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')
