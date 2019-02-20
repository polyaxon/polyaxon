from hestia.signal_decorators import ignore_raw

from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver

import auditor
import conf

from db.models.build_jobs import BuildJob
from db.models.cloning_strategies import CloningStrategy
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.notebooks import NotebookJob
from db.models.projects import Project
from db.models.tensorboards import TensorboardJob
from event_manager.events.build_job import BUILD_JOB_CLEANED_TRIGGERED, BUILD_JOB_DELETED
from event_manager.events.experiment import EXPERIMENT_CLEANED_TRIGGERED, EXPERIMENT_DELETED
from event_manager.events.experiment_group import EXPERIMENT_GROUP_DELETED
from event_manager.events.job import JOB_CLEANED_TRIGGERED, JOB_DELETED
from event_manager.events.notebook import NOTEBOOK_CLEANED_TRIGGERED
from event_manager.events.tensorboard import TENSORBOARD_CLEANED_TRIGGERED
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
        },
        countdown=conf.get('GLOBAL_COUNTDOWN'))

    auditor.record(event_type=BUILD_JOB_CLEANED_TRIGGERED, instance=job)


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
        },
        countdown=conf.get('GLOBAL_COUNTDOWN'))
    celery_app.send_task(
        SchedulerCeleryTasks.STORES_SCHEDULE_LOGS_DELETION,
        kwargs={
            'persistence': instance.persistence_logs,
            'subpath': instance.subpath,
        },
        countdown=conf.get('GLOBAL_COUNTDOWN'))


@receiver(post_delete, sender=ExperimentGroup, dispatch_uid="experiment_group_post_delete")
@ignore_raw
def experiment_group_post_delete(sender, **kwargs):
    """Delete all group outputs."""
    instance = kwargs['instance']
    auditor.record(event_type=EXPERIMENT_GROUP_DELETED, instance=instance)
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
            },
            countdown=conf.get('GLOBAL_COUNTDOWN'))
        celery_app.send_task(
            SchedulerCeleryTasks.STORES_SCHEDULE_LOGS_DELETION,
            kwargs={
                'persistence': instance.persistence_logs,
                'subpath': instance.subpath,
            },
            countdown=conf.get('GLOBAL_COUNTDOWN'))

    # Delete clones
    for experiment in instance.clones.filter(cloning_strategy=CloningStrategy.RESUME):
        experiment.delete()

    auditor.record(event_type=EXPERIMENT_CLEANED_TRIGGERED, instance=instance)


@receiver(post_delete, sender=Experiment, dispatch_uid="experiment_post_delete")
@ignore_raw
def experiment_post_delete(sender, **kwargs):
    instance = kwargs['instance']
    auditor.record(event_type=EXPERIMENT_DELETED, instance=instance)
    remove_bookmarks(object_id=instance.id, content_type='experiment')


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
        },
        countdown=conf.get('GLOBAL_COUNTDOWN'))
    celery_app.send_task(
        SchedulerCeleryTasks.STORES_SCHEDULE_LOGS_DELETION,
        kwargs={
            'persistence': job.persistence_logs,
            'subpath': job.subpath,
        },
        countdown=conf.get('GLOBAL_COUNTDOWN'))

    auditor.record(event_type=JOB_CLEANED_TRIGGERED, instance=job)


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
    auditor.record(event_type=NOTEBOOK_CLEANED_TRIGGERED, instance=job)


@receiver(pre_delete, sender=TensorboardJob, dispatch_uid="tensorboard_job_pre_delete")
@ignore_raw
def tensorboard_job_pre_delete(sender, **kwargs):
    job = kwargs['instance']
    auditor.record(event_type=TENSORBOARD_CLEANED_TRIGGERED, instance=job)


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
        },
        countdown=conf.get('GLOBAL_COUNTDOWN'))
    celery_app.send_task(
        SchedulerCeleryTasks.STORES_SCHEDULE_LOGS_DELETION,
        kwargs={
            'persistence': instance.persistence_logs,
            'subpath': instance.subpath,
        },
        countdown=conf.get('GLOBAL_COUNTDOWN'))
