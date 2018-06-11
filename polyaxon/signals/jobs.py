from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

import auditor

from constants.jobs import JobLifeCycle
from db.models.jobs import Job, JobStatus
from event_manager.events.job import JOB_FAILED, JOB_NEW_STATUS, JOB_STOPPED, JOB_SUCCEEDED
from libs.decorators import ignore_raw, ignore_updates, ignore_updates_pre
from libs.paths.jobs import delete_job_logs, delete_job_outputs
from libs.repos.utils import assign_code_reference
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks


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


@receiver(pre_delete, sender=Job, dispatch_uid="job_pre_delete")
@ignore_raw
def job_pre_delete(sender, **kwargs):
    job = kwargs['instance']

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
