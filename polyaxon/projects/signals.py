from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from libs.decorators import ignore_raw, ignore_updates
from projects.models import Project
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
def project_deleted(sender, **kwargs):
    instance = kwargs['instance']
    # Clean outputs, logs, and repos
    delete_project_outputs(instance.unique_name)
    delete_project_logs(instance.unique_name)
    delete_project_repos(instance.unique_name)
