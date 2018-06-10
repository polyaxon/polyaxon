from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver

import auditor

from db.models.projects import Project
from event_manager.events.project import PROJECT_DELETED
from libs.decorators import ignore_raw, ignore_updates
from libs.paths.projects import delete_project_logs, delete_project_outputs, delete_project_repos
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks


@receiver(post_save, sender=Project, dispatch_uid="project_post_save")
@ignore_updates
@ignore_raw
def project_post_save(sender, **kwargs):
    instance = kwargs['instance']
    # Clean outputs, logs, and repos
    delete_project_outputs(instance.unique_name)
    delete_project_logs(instance.unique_name)
    delete_project_repos(instance.unique_name)


@receiver(pre_delete, sender=Project, dispatch_uid="project_pre_delete")
@ignore_raw
def project_pre_delete(sender, **kwargs):
    instance = kwargs['instance']
    # Clean outputs, logs, and repos
    delete_project_outputs(instance.unique_name)
    delete_project_logs(instance.unique_name)
    delete_project_repos(instance.unique_name)


@receiver(pre_delete, sender=Project, dispatch_uid="project_stop_jobs")
@ignore_raw
def project_stop_jobs(sender, **kwargs):
    from scheduler import notebook_scheduler, tensorboard_scheduler

    instance = kwargs['instance']
    tensorboard_scheduler.stop_tensorboard(instance.tensorboard, update_status=False)
    notebook_scheduler.stop_notebook(instance.notebook, update_status=False)
    for build_job in instance.build_jobs.all():
        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_STOP,
            kwargs={
                'project_name': instance.unique_name,
                'project_uuid': instance.uuid.hex,
                'build_job_name': build_job.unique_name,
                'build_job_uuid': build_job.uuid.hex,
                'update_status': False
            })


@receiver(post_delete, sender=Project, dispatch_uid="project_deleted")
@ignore_raw
def project_post_deleted(sender, **kwargs):
    instance = kwargs['instance']
    auditor.record(event_type=PROJECT_DELETED, instance=instance)
