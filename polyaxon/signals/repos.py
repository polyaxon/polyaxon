import os

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from db.models.repos import CodeReference, ExternalRepo, Repo
from libs.decorators import ignore_raw, ignore_updates
from libs.paths import create_path, delete_path
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


@receiver(post_delete, sender=ExternalRepo, dispatch_uid="repo_deleted")
def repo_deleted(sender, **kwargs):
    if kwargs.get('raw'):
        # Ignore signal handling for fixture loading
        return

    instance = kwargs['instance']

    # Clean repo
    delete_path(instance.path)


@receiver(post_save, sender=ExternalRepo, dispatch_uid="external_repo_saved")
@ignore_updates
@ignore_raw
def new_external_repo(sender, **kwargs):
    instance = kwargs['instance']

    # Check that the user has a dir
    if not os.path.isdir(instance.user_path):
        create_path(instance.user_path)

    # Check that the project has a dir
    if not os.path.isdir(instance.project_path):
        create_path(instance.project_path)

    # Create a new repo
    git.clone_git_repo(repo_path=instance.path, git_url=instance.git_url)


@receiver(post_delete, sender=Repo, dispatch_uid="external_repo_deleted")
def external_repo_deleted(sender, **kwargs):
    if kwargs.get('raw'):
        # Ignore signal handling for fixture loading
        return

    instance = kwargs['instance']

    # Clean repo
    delete_path(instance.path)
