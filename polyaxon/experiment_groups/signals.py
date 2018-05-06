from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from experiment_groups.models import ExperimentGroup, ExperimentGroupStatus
from experiment_groups.paths import delete_experiment_group_logs, delete_experiment_group_outputs
from experiment_groups.statuses import ExperimentGroupLifeCycle
from libs.decorators import ignore_raw, ignore_updates, ignore_updates_pre
from repos.utils import assign_code_reference


@receiver(pre_save, sender=ExperimentGroup, dispatch_uid="experiment_group_pre_save")
@ignore_updates_pre
@ignore_raw
def experiment_group_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    # Add code reference
    assign_code_reference(instance)
    # Check if params need to be set
    if not instance.params and instance.specification:
        instance.params = instance.specification.settings.to_dict()


@receiver(post_save, sender=ExperimentGroup, dispatch_uid="experiment_group_saved")
@ignore_updates
@ignore_raw
def new_experiment_group(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(ExperimentGroupLifeCycle.CREATED)
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


@receiver(post_save, sender=ExperimentGroupStatus, dispatch_uid="experiment_group_status_saved")
@ignore_raw
def new_experiment_status(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)
    experiment_group = instance.experiment_group

    if created:
        # update experiment last_status
        experiment_group.status = instance
        experiment_group.save()
