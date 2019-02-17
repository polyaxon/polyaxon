import logging

from hestia.signal_decorators import ignore_raw, ignore_updates, ignore_updates_pre

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

import auditor

from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from db.models.experiment_jobs import ExperimentJob
from db.models.experiments import Experiment, ExperimentMetric
from event_manager.events.experiment import EXPERIMENT_NEW_METRIC
from libs.repos.utils import assign_code_reference
from signals.names import set_name
from signals.outputs import set_outputs, set_outputs_refs
from signals.persistence import set_persistence
from signals.tags import set_tags

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
    set_name(instance=instance, query=Experiment.all)
    if not instance.specification or not instance.specification.build:
        return

    if instance.is_independent:
        assign_code_reference(instance)
    else:
        instance.code_reference = instance.experiment_group.code_reference


@receiver(post_save, sender=Experiment, dispatch_uid="experiment_post_save")
@ignore_updates
@ignore_raw
def experiment_post_save(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(ExperimentLifeCycle.CREATED)
    if instance.is_independent:
        # TODO: Clean outputs and logs
        pass


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
