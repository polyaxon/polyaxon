import logging

from hestia.signal_decorators import (
    check_specification,
    ignore_raw,
    ignore_updates,
    ignore_updates_pre
)

from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

import auditor

from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from db.models.cloning_strategies import CloningStrategy
from db.models.experiment_groups import ExperimentGroup
from db.models.experiment_jobs import ExperimentJob
from db.models.experiments import Experiment, ExperimentMetric
from event_manager.events.experiment import EXPERIMENT_DELETED, EXPERIMENT_NEW_METRIC
from libs.repos.utils import assign_code_reference
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks
from signals.outputs import set_outputs, set_outputs_refs
from signals.utils import remove_bookmarks, set_persistence, set_tags

_logger = logging.getLogger('polyaxon.signals.experiments')


@receiver(pre_save, sender=Experiment, dispatch_uid="experiment_pre_save")
@ignore_updates_pre
@ignore_raw
def experiment_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    # Check if declarations need to be set
    if not instance.declarations and instance.specification:
        instance.declarations = instance.specification.declarations
    set_tags(instance=instance)
    set_persistence(instance=instance)
    set_outputs(instance=instance)
    set_outputs_refs(instance=instance)
    if not instance.specification or not instance.specification.build:
        return

    assign_code_reference(instance)


@receiver(post_save, sender=Experiment, dispatch_uid="experiment_post_save")
@ignore_updates
@ignore_raw
def experiment_post_save(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(ExperimentLifeCycle.CREATED)

    if instance.is_independent:
        # TODO: Clean outputs and logs
        pass


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


@receiver(post_save, sender=ExperimentJob, dispatch_uid="experiment_job_post_save")
@ignore_updates
@ignore_raw
def experiment_job_post_save(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(status=JobLifeCycle.CREATED)

@receiver(post_save, sender=ExperimentMetric, dispatch_uid="experiment_metric_post_save")
@ignore_updates
@ignore_raw
def experiment_metric_post_save(sender, **kwargs):
    instance = kwargs['instance']
    experiment = instance.experiment

    # update experiment last_metric
    def update_metric(last_metrics, metrics):
        last_metrics.update(metrics)
        return last_metrics

    experiment.last_metric = update_metric(last_metrics=experiment.last_metric,
                                           metrics=instance.values)
    experiment.save(update_fields=['last_metric'])
    auditor.record(event_type=EXPERIMENT_NEW_METRIC,
                   instance=experiment)


@receiver(post_save, sender=Experiment, dispatch_uid="start_new_experiment")
@check_specification
@ignore_updates
@ignore_raw
def start_new_experiment(sender, **kwargs):
    instance = kwargs['instance']
    if instance.is_independent or instance.is_clone:
        # Start building the experiment and then Schedule it to be picked by the spawners
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_BUILD,
            kwargs={'experiment_id': instance.id},
            countdown=1)


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
