import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

import auditor

from constants.jobs import JobLifeCycle
from db.models.jobs import Job, JobStatus
from event_manager.events.job import JOB_FAILED, JOB_NEW_STATUS, JOB_STOPPED, JOB_SUCCEEDED
from libs.decorators import ignore_raw, ignore_updates, ignore_updates_pre
from libs.repos.utils import assign_code_reference

logger = logging.getLogger('polyaxon.plugins')


@receiver(pre_save, sender=Job, dispatch_uid="job_pre_save")
@ignore_updates_pre
@ignore_raw
def job_pre_save(sender, **kwargs):
    assign_code_reference(kwargs['instance'])


@receiver(post_save, sender=Job, dispatch_uid="job_post_save")
@ignore_updates
@ignore_raw
def job_post_save(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(status=JobLifeCycle.CREATED)


@receiver(post_save, sender=JobStatus, dispatch_uid="job_status_post_save")
@ignore_updates
@ignore_raw
def job_status_post_save(sender, **kwargs):
    instance = kwargs['instance']
    job = instance.job
    previous_status = job.last_status
    # Update job last_status
    job.status = instance
    job.save()
    auditor.record(event_type=JOB_NEW_STATUS,
                   instance=job,
                   previous_status=previous_status,
                   target='project')
    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=JOB_STOPPED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')

    if instance.status == JobLifeCycle.FAILED:
        auditor.record(event_type=JOB_FAILED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')

    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=JOB_SUCCEEDED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')
