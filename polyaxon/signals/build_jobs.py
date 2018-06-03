from django.db.models.signals import post_save
from django.dispatch import receiver

import auditor
from constants.jobs import JobLifeCycle
from db.models.build_jobs import BuildJob, BuildJobStatus
from event_manager.events.build_job import (
    BUILD_JOB_NEW_STATUS,
    BUILD_JOB_STOPPED,
    BUILD_JOB_FAILED,
    BUILD_JOB_SUCCEEDED
)
from libs.decorators import ignore_updates, ignore_raw


@receiver(post_save, sender=BuildJob, dispatch_uid="build_job_saved")
@ignore_updates
@ignore_raw
def new_tensorboard_job(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(status=JobLifeCycle.CREATED)


@receiver(post_save, sender=BuildJobStatus, dispatch_uid="new_build_job_status_saved")
@ignore_updates
@ignore_raw
def new_build_job_status_saved(sender, **kwargs):
    instance = kwargs['instance']
    job = instance.job
    previous_status = job.last_status
    # Update job last_status
    job.job_status = instance
    job.save()
    auditor.record(event_type=BUILD_JOB_NEW_STATUS,
                   instance=job,
                   previous_status=previous_status,
                   target='project')
    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=BUILD_JOB_STOPPED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')

    if instance.status == JobLifeCycle.FAILED:
        auditor.record(event_type=BUILD_JOB_FAILED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')

    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=BUILD_JOB_SUCCEEDED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')
