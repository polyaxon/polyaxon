from hestia.signal_decorators import ignore_raw, ignore_updates, ignore_updates_pre

from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from constants.jobs import JobLifeCycle
from db.models.notebooks import NotebookJob
from libs.repos.utils import assign_code_reference
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks
from signals.outputs import set_outputs, set_outputs_refs
from signals.utils import set_persistence, set_tags


@receiver(pre_save, sender=NotebookJob, dispatch_uid="notebook_job_pre_save")
@ignore_updates_pre
@ignore_raw
def notebook_job_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    set_tags(instance=instance)
    set_persistence(instance=instance)
    set_outputs(instance=instance)
    set_outputs_refs(instance=instance)
    assign_code_reference(instance)


@receiver(post_save, sender=NotebookJob, dispatch_uid="notebook_job_post_save")
@ignore_updates
@ignore_raw
def notebook_job_post_save(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(status=JobLifeCycle.CREATED)


@receiver(pre_delete, sender=NotebookJob, dispatch_uid="notebook_job_pre_delete")
@ignore_raw
def notebook_job_pre_delete(sender, **kwargs):
    job = kwargs['instance']

    celery_app.send_task(
        SchedulerCeleryTasks.PROJECTS_NOTEBOOK_STOP,
        kwargs={
            'project_name': job.project.unique_name,
            'project_uuid': job.project.uuid.hex,
            'notebook_job_name': job.unique_name,
            'notebook_job_uuid': job.uuid.hex,
            'update_status': False
        })
