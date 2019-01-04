import logging

from hestia.signal_decorators import (
    check_specification,
    ignore_raw,
    ignore_updates,
    ignore_updates_pre
)

from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

import auditor

from constants.jobs import JobLifeCycle
from db.models.jobs import Job, JobStatus
from db.redis.tll import RedisTTL
from event_manager.events.job import (
    JOB_DELETED,
    JOB_DONE,
    JOB_FAILED,
    JOB_NEW_STATUS,
    JOB_STOPPED,
    JOB_SUCCEEDED
)
from libs.repos.utils import assign_code_reference
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks
from signals.outputs import set_outputs, set_outputs_refs
from signals.run_time import set_job_finished_at, set_job_started_at
from signals.utils import remove_bookmarks, set_persistence, set_tags

_logger = logging.getLogger('polyaxon.signals.jobs')


@receiver(pre_save, sender=Job, dispatch_uid="job_pre_save")
@ignore_updates_pre
@ignore_raw
def job_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    set_tags(instance=instance)
    set_persistence(instance=instance)
    set_outputs(instance=instance)
    set_outputs_refs(instance=instance)

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

    # TODO: Clean outputs and logs


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


@receiver(pre_delete, sender=Job, dispatch_uid="job_pre_delete")
@ignore_raw
def job_pre_delete(sender, **kwargs):
    job = kwargs['instance']

    # Delete outputs and logs
    celery_app.send_task(
        SchedulerCeleryTasks.STORES_SCHEDULE_OUTPUTS_DELETION,
        kwargs={
            'persistence': job.persistence_outputs,
            'subpath': job.subpath,
        })
    celery_app.send_task(
        SchedulerCeleryTasks.STORES_SCHEDULE_LOGS_DELETION,
        kwargs={
            'persistence': job.persistence_logs,
            'subpath': job.subpath,
        })

    if not job.is_running:
        return

    celery_app.send_task(
        SchedulerCeleryTasks.JOBS_STOP,
        kwargs={
            'project_name': job.project.unique_name,
            'project_uuid': job.project.uuid.hex,
            'job_name': job.unique_name,
            'job_uuid': job.uuid.hex,
            'update_status': False,
            'collect_logs': False,
        })


@receiver(post_delete, sender=Job, dispatch_uid="job_post_delete")
@ignore_raw
def job_post_delete(sender, **kwargs):
    instance = kwargs['instance']
    auditor.record(event_type=JOB_DELETED, instance=instance)
    remove_bookmarks(object_id=instance.id, content_type='job')


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
