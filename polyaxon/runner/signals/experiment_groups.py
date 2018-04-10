from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from experiment_groups.models import ExperimentGroup
from libs.decorators import ignore_raw, runner_signal
from runner.schedulers import experiment_scheduler
from experiment_groups.tasks import create_group_experiments


@receiver(post_save, sender=ExperimentGroup, dispatch_uid="experiment_group_create_experiments")
@runner_signal
@ignore_raw
def new_experiment_group(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    if not created:
        return

    create_group_experiments.apply_async((instance.id,), countdown=1)


@receiver(pre_delete, sender=ExperimentGroup, dispatch_uid="experiment_group_stop_experiments")
@runner_signal
@ignore_raw
def experiment_group_stop_experiments(sender, **kwargs):
    """Stop all experiments before deleting the group."""

    instance = kwargs['instance']
    for experiment in instance.running_experiments:
        # Delete all jobs from DB before sending a signal to k8s,
        # this way no statuses will be updated in the meanwhile
        experiment.jobs.all().delete()
        experiment_scheduler.stop_experiment(experiment, update_status=False)
