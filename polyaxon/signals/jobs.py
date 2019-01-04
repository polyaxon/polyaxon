import logging

from hestia.signal_decorators import (
    check_specification,
    ignore_raw,
    ignore_updates,
    ignore_updates_pre
)

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from constants.jobs import JobLifeCycle
from db.models.jobs import Job
from libs.repos.utils import assign_code_reference
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks
from signals.outputs import set_outputs, set_outputs_refs
from signals.persistence import set_persistence
from signals.tags import set_tags

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
