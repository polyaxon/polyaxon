from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from experiment_groups.models import ExperimentGroup
from experiment_groups.paths import delete_experiment_group_logs, delete_experiment_group_outputs
from experiment_groups.tasks import create_group_experiments
from libs.decorators import ignore_raw
from schedulers import experiment_scheduler


@receiver(post_save, sender=ExperimentGroup, dispatch_uid="experiment_group_saved")
@ignore_raw
def new_experiment_group(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    if not created:
        return

    # Clean outputs and logs
    delete_experiment_group_outputs(instance.unique_name)
    delete_experiment_group_logs(instance.unique_name)

    create_group_experiments.apply_async((instance.id,), countdown=1)


@receiver(pre_delete, sender=ExperimentGroup, dispatch_uid="experiment_group_deleted")
@ignore_raw
def experiment_group_deleted(sender, **kwargs):
    """Stop all experiments before deleting the group."""

    instance = kwargs['instance']
    for experiment in instance.running_experiments:
        # Delete all jobs from DB before sending a signal to k8s,
        # this way no statuses will be updated in the meanwhile
        experiment.jobs.all().delete()
        experiment_scheduler.stop_experiment(experiment, update_status=False)

    # Delete outputs and logs
    delete_experiment_group_outputs(instance.unique_name)
    delete_experiment_group_logs(instance.unique_name)
