import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

import auditor

from constants.jobs import JobLifeCycle
from db.models.build_jobs import BuildJob, BuildJobStatus
from event_manager.events.build_job import (
    BUILD_JOB_FAILED,
    BUILD_JOB_NEW_STATUS,
    BUILD_JOB_STOPPED,
    BUILD_JOB_SUCCEEDED
)
from libs.decorators import ignore_raw, ignore_updates
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks

_logger = logging.getLogger('polyaxon.signals.build_jobs')


@receiver(post_save, sender=BuildJob, dispatch_uid="build_job_saved")
@ignore_updates
@ignore_raw
def new_build_job(sender, **kwargs):
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


@receiver(post_save, sender=BuildJobStatus, dispatch_uid="handle_new_build_job_status")
@ignore_raw
def handle_new_build_job_status(sender, **kwargs):
    instance = kwargs['instance']
    build_job = instance.job
    if not build_job.specification:
        return

    if instance.status in (JobLifeCycle.FAILED, JobLifeCycle.SUCCEEDED):
        _logger.info('The worker `%s` failed or is done, '
                     'send signal to stop.', build_job.unique_name)
        # Schedule stop for this experiment because other jobs may be still running
        celery_app.send_task(
            SchedulerCeleryTasks.BUILDS_STOP,
            kwargs={'build_job_id': build_job.id,
                    'update_status': False})
