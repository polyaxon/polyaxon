from hestia.decorators import ignore_raw, ignore_updates

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from db.models.repos import CodeReference, Repo
from libs.paths.utils import delete_path
from libs.repos import git


@receiver(post_save, sender=Repo, dispatch_uid="repo_saved")
@ignore_updates
@ignore_raw
def new_repo(sender, **kwargs):
    instance = kwargs['instance']
    git.set_git_repo(instance)
    last_commit = instance.last_commit
    if not last_commit:
        return None

    # Set code reference
    CodeReference.objects.get_or_create(repo=instance, commit=last_commit[0])


@receiver(post_delete, sender=Repo, dispatch_uid="repo_deleted")
def repo_deleted(sender, **kwargs):
    if kwargs.get('raw'):
        # Ignore signal handling for fixture loading
        return

    instance = kwargs['instance']

    # Clean repo
    delete_path(instance.path)
