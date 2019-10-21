from hestia.signal_decorators import ignore_raw, ignore_updates

from django.db.models.signals import post_save
from django.dispatch import receiver

from db.models.repos import CodeReference, ExternalRepo, Repo
from libs.repos import git


@receiver(post_save, sender=Repo, dispatch_uid="new_repo")
@ignore_updates
@ignore_raw
def new_repo(sender, **kwargs):
    instance = kwargs['instance']
    git.internal.set_git_repo(instance)
    try:
        last_commit = instance.last_commit
    except ValueError:
        return None

    # Set code reference
    CodeReference.objects.get_or_create(repo=instance, commit=last_commit[0])


@receiver(post_save, sender=ExternalRepo, dispatch_uid="new_external_repo")
@ignore_updates
@ignore_raw
def new_external_repo(sender, **kwargs):
    instance = kwargs['instance']
    git.external.set_git_repo(instance)
    try:
        last_commit = instance.last_commit
    except ValueError:
        return None

    # Set code reference
    CodeReference.objects.get_or_create(external_repo=instance,
                                        commit=last_commit[0],
                                        git_url=instance.git_url)
