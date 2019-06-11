from hestia.paths import delete_path
from hestia.signal_decorators import ignore_raw, ignore_updates

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

import auditor

from db.models.projects import Project
from db.models.repos import Repo
from events.registry.project import PROJECT_DELETED
from libs.paths.projects import delete_project_repos
from signals.bookmarks import remove_bookmarks


@receiver(post_save, sender=Project, dispatch_uid="project_post_save")
@ignore_updates
@ignore_raw
def project_post_save(sender, **kwargs):
    instance = kwargs['instance']
    # TODO: Clean outputs, logs,
    # Clean repos
    delete_project_repos(instance.unique_name)


@receiver(post_delete, sender=Project, dispatch_uid="project_deleted")
@ignore_raw
def project_post_deleted(sender, **kwargs):
    instance = kwargs['instance']
    auditor.record(event_type=PROJECT_DELETED, instance=instance)
    remove_bookmarks(object_id=instance.id, content_type='project')


@receiver(post_delete, sender=Repo, dispatch_uid="repo_deleted")
def repo_deleted(sender, **kwargs):
    if kwargs.get('raw'):
        # Ignore signal handling for fixture loading
        return

    instance = kwargs['instance']

    # Clean repo
    delete_path(instance.path)
