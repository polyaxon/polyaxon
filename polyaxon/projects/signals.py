from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from libs.decorators import ignore_raw, ignore_updates
from projects.models import Project
from projects.paths import delete_project_logs, delete_project_outputs, delete_project_repos
from runner.schedulers import notebook_scheduler, tensorboard_scheduler


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
    tensorboard_scheduler.stop_tensorboard(instance, update_status=False)
    notebook_scheduler.stop_notebook(instance, update_status=False)
    # Delete tensorboard job
    if instance.tensorboard:
        instance.tensorboard.delete()

    # Delete notebook job
    if instance.notebook:
        instance.notebook.delete()

    # Clean outputs, logs, and repos
    delete_project_outputs(instance.unique_name)
    delete_project_logs(instance.unique_name)
    delete_project_repos(instance.unique_name)
