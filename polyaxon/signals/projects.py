from hestia.decorators import ignore_raw, ignore_updates, ignore_updates_pre

from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

import auditor
import ownership

from db.models.projects import Project
from event_manager.events.project import PROJECT_DELETED
from libs.paths.projects import delete_project_logs, delete_project_outputs, delete_project_repos
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
    # Clean outputs, logs, and repos
    delete_project_outputs(persistence_outputs=None, project_name=instance.unique_name)
    delete_project_logs(instance.unique_name)
    delete_project_repos(instance.unique_name)


@receiver(pre_delete, sender=Project, dispatch_uid="project_pre_delete")
@ignore_raw
def project_pre_delete(sender, **kwargs):
    instance = kwargs['instance']
    # Clean outputs, logs, and repos
    delete_project_outputs(persistence_outputs=None, project_name=instance.unique_name)
    delete_project_logs(instance.unique_name)
    delete_project_repos(instance.unique_name)


@receiver(post_delete, sender=Project, dispatch_uid="project_deleted")
@ignore_raw
def project_post_deleted(sender, **kwargs):
    instance = kwargs['instance']
    auditor.record(event_type=PROJECT_DELETED, instance=instance)
    remove_bookmarks(object_id=instance.id, content_type='project')
