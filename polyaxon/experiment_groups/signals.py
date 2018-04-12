from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from experiment_groups.models import ExperimentGroup
from experiment_groups.paths import delete_experiment_group_logs, delete_experiment_group_outputs
from libs.decorators import ignore_raw, ignore_updates, ignore_updates_pre
from repos.utils import assign_code_reference


@receiver(pre_save, sender=ExperimentGroup, dispatch_uid="experiment_group_saved")
@ignore_updates_pre
@ignore_raw
def add_experiment_group_code_reference(sender, **kwargs):
    assign_code_reference(kwargs['instance'])


@receiver(post_save, sender=ExperimentGroup, dispatch_uid="experiment_group_saved")
@ignore_updates
@ignore_raw
def new_experiment_group(sender, **kwargs):
    instance = kwargs['instance']
    # Clean outputs and logs
    delete_experiment_group_outputs(instance.unique_name)
    delete_experiment_group_logs(instance.unique_name)


@receiver(post_delete, sender=ExperimentGroup, dispatch_uid="experiment_group_deleted")
@ignore_raw
def experiment_group_deleted(sender, **kwargs):
    """Delete all group outputs."""

    instance = kwargs['instance']

    # Delete outputs and logs
    delete_experiment_group_outputs(instance.unique_name)
    delete_experiment_group_logs(instance.unique_name)
