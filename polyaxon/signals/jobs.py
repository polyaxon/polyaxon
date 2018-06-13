import logging

from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

import auditor

from constants.jobs import JobLifeCycle
from db.models.jobs import Job, JobStatus
from event_manager.events.job import (
    JOB_DELETED,
    JOB_FAILED,
    JOB_NEW_STATUS,
    JOB_STOPPED,
    JOB_SUCCEEDED
)
from libs.decorators import check_specification, ignore_raw, ignore_updates, ignore_updates_pre
from libs.paths.jobs import delete_job_logs, delete_job_outputs
from libs.repos.utils import assign_code_reference
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks

_logger = logging.getLogger('polyaxon.signals.jobs')


@receiver(pre_save, sender=Job, dispatch_uid="job_pre_save")
@ignore_updates_pre
@ignore_raw
def job_pre_save(sender, **kwargs):
    instance = kwargs['instance']

    # Add code reference
    # Check if :
    # the job is new
    # that it has an build section
    # that is not an external repo (because we did not clone it yet)
    # if the instance has a primary key then is getting updated
    condition = (
        instance.specification.build.git or
        instance.code_reference or
        not instance.project.has_code)
    if condition:
        return

    assign_code_reference(instance)


@receiver(post_save, sender=Job, dispatch_uid="job_post_save")
@ignore_updates
@ignore_raw
def job_post_save(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(status=JobLifeCycle.CREATED)

    # Clean outputs and logs
    delete_job_logs(instance.unique_name)
    delete_job_outputs(instance.unique_name)


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
                   previous_status=previous_status)
    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=JOB_STOPPED,
                       instance=job,
                       previous_status=previous_status)

    if instance.status == JobLifeCycle.FAILED:
        auditor.record(event_type=JOB_FAILED,
                       instance=job,
                       previous_status=previous_status)

    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=JOB_SUCCEEDED,
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
                'specification': job.specification,
                'update_status': False
            })


@receiver(pre_delete, sender=Job, dispatch_uid="job_pre_delete")
@ignore_raw
def job_pre_delete(sender, **kwargs):
    job = kwargs['instance']

    # Delete outputs and logs
    delete_job_outputs(job.unique_name)
    delete_job_logs(job.unique_name)

    if not job.is_running:
        return

    celery_app.send_task(
        SchedulerCeleryTasks.JOBS_STOP,
        kwargs={
            'project_name': job.project.unique_name,
            'project_uuid': job.project.uuid.hex,
            'job_name': job.unique_name,
            'job_uuid': job.uuid.hex,
            'specification': job.specification,
            'update_status': False
        })


@receiver(post_delete, sender=Job, dispatch_uid="job_post_delete")
@ignore_raw
def job_post_delete(sender, **kwargs):
    instance = kwargs['instance']
    auditor.record(event_type=JOB_DELETED, instance=instance)


@receiver(post_save, sender=Job, dispatch_uid="start_job")
@check_specification
@ignore_updates
@ignore_raw
def start_job(sender, **kwargs):
    instance = kwargs['instance']
    celery_app.send_task(
        SchedulerCeleryTasks.JOBS_BUILD,
        kwargs={'job_id': instance.id},
        countdown=1)
