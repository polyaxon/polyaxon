import logging

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from experiment_groups.models import ExperimentGroup
from experiments.models import Experiment, ExperimentStatus
from experiments.statuses import ExperimentLifeCycle
from libs.decorators import check_specification, ignore_raw, ignore_updates, runner_signal
from runner.schedulers import experiment_scheduler
from runner.tasks.experiments import build_experiment

logger = logging.getLogger('polyaxon.runner.experiments')


@receiver(post_save, sender=Experiment, dispatch_uid="start_new_experiment")
@runner_signal
@check_specification
@ignore_updates
@ignore_raw
def start_new_experiment(sender, **kwargs):
    instance = kwargs['instance']
    if instance.is_independent:
        # Start building the experiment and then Schedule it to be picked by the spawners
        build_experiment.apply_async((instance.id, ), countdown=1)


@receiver(pre_delete, sender=Experiment, dispatch_uid="stop_running_experiment")
@runner_signal
@check_specification
@ignore_raw
def stop_running_experiment(sender, **kwargs):
    instance = kwargs['instance']
    try:
        _ = instance.experiment_group  # noqa
        # Delete all jobs from DB before sending a signal to k8s,
        # this way no statuses will be updated in the meanwhile
        instance.jobs.all().delete()
        experiment_scheduler.stop_experiment(instance, update_status=False)
    except ExperimentGroup.DoesNotExist:
        # The experiment was already stopped when the group was deleted
        pass


@receiver(post_save, sender=ExperimentStatus, dispatch_uid="handle_new_experiment_status")
@runner_signal
@ignore_raw
def handle_new_experiment_status(sender, **kwargs):
    instance = kwargs['instance']
    experiment = instance.experiment
    if not experiment.specification:
        return

    if instance.status in (ExperimentLifeCycle.FAILED, ExperimentLifeCycle.SUCCEEDED):
        logger.info('One of the workers failed or Master for experiment `%s` is done, '
                    'send signal to other workers to stop.', experiment.unique_name)
        # Schedule stop for this experiment because other jobs may be still running
        experiment_scheduler.stop_experiment(experiment, update_status=False)
