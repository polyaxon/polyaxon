from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver

import auditor

from event_manager.events.project import PROJECT_DELETED
from libs.decorators import ignore_raw, ignore_updates
from db.models.projects import Project
from projects.paths import delete_project_logs, delete_project_outputs, delete_project_repos


@receiver(post_save, sender=Project, dispatch_uid="project_saved")
@ignore_updates
@ignore_raw
def new_project(sender, **kwargs):
    instance = kwargs['instance']
    # Clean outputs, logs, and repos
    delete_project_outputs(instance.unique_name)
    delete_project_logs(instance.unique_name)
    delete_project_repos(instance.unique_name)


@receiver(pre_delete, sender=Project, dispatch_uid="project_deleted")
@ignore_raw
def project_pre_deleted(sender, **kwargs):
    instance = kwargs['instance']
    # Clean outputs, logs, and repos
    delete_project_outputs(instance.unique_name)
    delete_project_logs(instance.unique_name)
    delete_project_repos(instance.unique_name)


@receiver(post_delete, sender=Project, dispatch_uid="project_deleted")
@ignore_raw
def project_post_deleted(sender, **kwargs):
    instance = kwargs['instance']
    auditor.record(event_type=PROJECT_DELETED, instance=instance)
