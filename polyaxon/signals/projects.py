from hestia.signal_decorators import ignore_raw, ignore_updates, ignore_updates_pre

from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

import auditor
import ownership

from db.models.projects import Project
from event_manager.events.project import PROJECT_DELETED
from libs.paths.projects import delete_project_repos
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks
from signals.utils import remove_bookmarks


@receiver(pre_save, sender=Project, dispatch_uid="project_pre_save")
@ignore_updates_pre
@ignore_raw
def project_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    # Set default owner
    if not instance.has_owner:
        ownership.set_default_owner(instance=instance)


@receiver(post_save, sender=Project, dispatch_uid="project_post_save")
@ignore_updates
@ignore_raw
def project_post_save(sender, **kwargs):
    instance = kwargs['instance']
    # TODO: Clean outputs, logs,
    # Clean repos
    delete_project_repos(instance.unique_name)


@receiver(pre_delete, sender=Project, dispatch_uid="project_pre_delete")
@ignore_raw
def project_pre_delete(sender, **kwargs):
    instance = kwargs['instance']
    # Clean repos
    delete_project_repos(instance.unique_name)
    # Clean outputs and logs
    celery_app.send_task(
        SchedulerCeleryTasks.STORES_SCHEDULE_OUTPUTS_DELETION,
        kwargs={
            'persistence': instance.persistence_outputs,
            'subpath': instance.subpath,
        })
    celery_app.send_task(
        SchedulerCeleryTasks.STORES_SCHEDULE_LOGS_DELETION,
        kwargs={
            'persistence': instance.persistence_logs,
            'subpath': instance.subpath,
        })


@receiver(post_delete, sender=Project, dispatch_uid="project_deleted")
@ignore_raw
def project_post_deleted(sender, **kwargs):
    instance = kwargs['instance']
    auditor.record(event_type=PROJECT_DELETED, instance=instance)
    remove_bookmarks(object_id=instance.id, content_type='project')
