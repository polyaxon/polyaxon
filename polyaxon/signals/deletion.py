from hestia.signal_decorators import check_specification, ignore_raw

from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver

import auditor

from db.models.build_jobs import BuildJob
from db.models.cloning_strategies import CloningStrategy
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.notebooks import NotebookJob
from db.models.projects import Project
from db.models.tensorboards import TensorboardJob
from event_manager.events.build_job import BUILD_JOB_DELETED
from event_manager.events.experiment import EXPERIMENT_DELETED
from event_manager.events.experiment_group import EXPERIMENT_GROUP_DELETED
from event_manager.events.job import JOB_DELETED
from libs.paths.projects import delete_project_repos
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks
from signals.bookmarks import remove_bookmarks


@receiver(pre_delete, sender=BuildJob, dispatch_uid="build_job_pre_delete")
@ignore_raw
def build_job_pre_delete(sender, **kwargs):
    job = kwargs['instance']

    # Delete outputs and logs
    celery_app.send_task(
        SchedulerCeleryTasks.STORES_SCHEDULE_LOGS_DELETION,
        kwargs={
            'persistence': job.persistence_logs,
            'subpath': job.subpath,
        })

    if not job.is_running:
        return

    celery_app.send_task(
        SchedulerCeleryTasks.BUILD_JOBS_STOP,
        kwargs={
            'project_name': job.project.unique_name,
            'project_uuid': job.project.uuid.hex,
            'build_job_name': job.unique_name,
            'build_job_uuid': job.uuid.hex,
            'update_status': False
        })


@receiver(post_delete, sender=BuildJob, dispatch_uid="build_job_post_delete")
@ignore_raw
def build_job_post_delete(sender, **kwargs):
    instance = kwargs['instance']
    auditor.record(event_type=BUILD_JOB_DELETED, instance=instance)
    remove_bookmarks(object_id=instance.id, content_type='buildjob')


@receiver(pre_delete, sender=ExperimentGroup, dispatch_uid="experiment_group_pre_delete")
@ignore_raw
def experiment_group_pre_delete(sender, **kwargs):
    """Delete all group outputs."""
    instance = kwargs['instance']

    if instance.is_selection:
        return

    # Delete outputs and logs
    celery_app.send_task(
        SchedulerCeleryTasks.STORES_SCHEDULE_OUTPUTS_DELETION,
        kwargs={
            'persistence': instance.persistence_outputs,
            'subpath': instance.subpath,
        })
    celery_app.send_task(
        SchedulerCeleryTasks.STORES_SCHEDULE_LOGS_DELETION,
        kwargs={
            'persistence': instance.persistence_logs,
            'subpath': instance.subpath,
        })


@receiver(post_delete, sender=ExperimentGroup, dispatch_uid="experiment_group_post_delete")
@ignore_raw
def experiment_group_post_delete(sender, **kwargs):
    """Delete all group outputs."""
    instance = kwargs['instance']
    auditor.record(event_type=EXPERIMENT_GROUP_DELETED,
                   instance=instance)
    remove_bookmarks(object_id=instance.id, content_type='experimentgroup')


@receiver(pre_delete, sender=Experiment, dispatch_uid="experiment_pre_delete")
@ignore_raw
def experiment_pre_delete(sender, **kwargs):
    instance = kwargs['instance']

    # Delete outputs and logs
    if instance.is_independent:
        celery_app.send_task(
            SchedulerCeleryTasks.STORES_SCHEDULE_OUTPUTS_DELETION,
            kwargs={
                'persistence': instance.persistence_outputs,
                'subpath': instance.subpath,
            })
        celery_app.send_task(
            SchedulerCeleryTasks.STORES_SCHEDULE_LOGS_DELETION,
            kwargs={
                'persistence': instance.persistence_logs,
                'subpath': instance.subpath,
            })

    # Delete clones
    for experiment in instance.clones.filter(cloning_strategy=CloningStrategy.RESUME):
        experiment.delete()


@receiver(post_delete, sender=Experiment, dispatch_uid="experiment_post_delete")
@ignore_raw
def experiment_post_delete(sender, **kwargs):
    instance = kwargs['instance']
    auditor.record(event_type=EXPERIMENT_DELETED, instance=instance)
    remove_bookmarks(object_id=instance.id, content_type='experiment')


@receiver(pre_delete, sender=Experiment, dispatch_uid="stop_running_experiment")
@check_specification
@ignore_raw
def stop_running_experiment(sender, **kwargs):
    instance = kwargs['instance']
    if not instance.is_running or instance.jobs.count() == 0:
        return

    try:
        group = instance.experiment_group
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_STOP,
            kwargs={
                'project_name': instance.project.unique_name,
                'project_uuid': instance.project.uuid.hex,
                'experiment_name': instance.unique_name,
                'experiment_uuid': instance.uuid.hex,
                'experiment_group_name': group.unique_name if group else None,
                'experiment_group_uuid': group.uuid.hex if group else None,
                'specification': instance.config,
                'update_status': False,
                'collect_logs': False,
            },
            countdown=1)
    except ExperimentGroup.DoesNotExist:
        # The experiment was already stopped when the group was deleted
        pass


@receiver(pre_delete, sender=Job, dispatch_uid="job_pre_delete")
@ignore_raw
def job_pre_delete(sender, **kwargs):
    job = kwargs['instance']

    # Delete outputs and logs
    celery_app.send_task(
        SchedulerCeleryTasks.STORES_SCHEDULE_OUTPUTS_DELETION,
        kwargs={
            'persistence': job.persistence_outputs,
            'subpath': job.subpath,
        })
    celery_app.send_task(
        SchedulerCeleryTasks.STORES_SCHEDULE_LOGS_DELETION,
        kwargs={
            'persistence': job.persistence_logs,
            'subpath': job.subpath,
        })

    if not job.is_running:
        return

    celery_app.send_task(
        SchedulerCeleryTasks.JOBS_STOP,
        kwargs={
            'project_name': job.project.unique_name,
            'project_uuid': job.project.uuid.hex,
            'job_name': job.unique_name,
            'job_uuid': job.uuid.hex,
            'update_status': False,
            'collect_logs': False,
        })


@receiver(post_delete, sender=Job, dispatch_uid="job_post_delete")
@ignore_raw
def job_post_delete(sender, **kwargs):
    instance = kwargs['instance']
    auditor.record(event_type=JOB_DELETED, instance=instance)
    remove_bookmarks(object_id=instance.id, content_type='job')


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


@receiver(pre_delete, sender=TensorboardJob, dispatch_uid="tensorboard_job_pre_delete")
@ignore_raw
def tensorboard_job_pre_delete(sender, **kwargs):
    job = kwargs['instance']

    celery_app.send_task(
        SchedulerCeleryTasks.TENSORBOARDS_STOP,
        kwargs={
            'project_name': job.project.unique_name,
            'project_uuid': job.project.uuid.hex,
            'tensorboard_job_name': job.unique_name,
            'tensorboard_job_uuid': job.uuid.hex,
            'update_status': False
        })


@receiver(pre_delete, sender=Project, dispatch_uid="project_pre_delete")
@ignore_raw
def project_pre_delete(sender, **kwargs):
    instance = kwargs['instance']
    # Clean repos
    delete_project_repos(instance.unique_name)
    # Clean outputs and logs
    celery_app.send_task(
        SchedulerCeleryTasks.STORES_SCHEDULE_OUTPUTS_DELETION,
        kwargs={
            'persistence': instance.persistence_outputs,
            'subpath': instance.subpath,
        })
    celery_app.send_task(
        SchedulerCeleryTasks.STORES_SCHEDULE_LOGS_DELETION,
        kwargs={
            'persistence': instance.persistence_logs,
            'subpath': instance.subpath,
        })
