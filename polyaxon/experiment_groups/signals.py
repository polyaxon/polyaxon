from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

import auditor

from event_manager.events.experiment_group import (
    EXPERIMENT_GROUP_CREATED,
    EXPERIMENT_GROUP_DELETED,
    EXPERIMENT_GROUP_FINISHED,
    EXPERIMENT_GROUP_ITERATION,
    EXPERIMENT_GROUP_NEW_STATUS,
    EXPERIMENT_GROUP_STOPPED
)
from experiment_groups.models import (
    ExperimentGroup,
    ExperimentGroupIteration,
    ExperimentGroupStatus
)
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
    auditor.record(event_type=EXPERIMENT_GROUP_CREATED,
                   instance=instance)


@receiver(pre_delete, sender=ExperimentGroup, dispatch_uid="experiment_group_deleted")
@ignore_raw
def experiment_group_pre_deleted(sender, **kwargs):
    """Delete all group outputs."""
    instance = kwargs['instance']

    # Delete outputs and logs
    delete_experiment_group_outputs(instance.unique_name)
    delete_experiment_group_logs(instance.unique_name)


@receiver(post_delete, sender=ExperimentGroup, dispatch_uid="experiment_group_deleted")
@ignore_raw
def experiment_group_post_deleted(sender, **kwargs):
    """Delete all group outputs."""
    instance = kwargs['instance']
    auditor.record(event_type=EXPERIMENT_GROUP_DELETED,
                   instance=instance)


@receiver(post_save, sender=ExperimentGroupStatus, dispatch_uid="experiment_group_status_saved")
@ignore_raw
def new_experiment_status(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)
    experiment_group = instance.experiment_group
    previous_status = experiment_group.last_status

    if created:
        # update experiment last_status
        experiment_group.status = instance
        experiment_group.save()
        auditor.record(event_type=EXPERIMENT_GROUP_NEW_STATUS,
                       instance=experiment_group,
                       previous_status=previous_status)

    if instance.status == ExperimentGroupLifeCycle.STOPPED:
        auditor.record(event_type=EXPERIMENT_GROUP_STOPPED,
                       instance=experiment_group,
                       previous_status=previous_status)

    if ExperimentGroupLifeCycle.is_done(instance.status):
        auditor.record(event_type=EXPERIMENT_GROUP_FINISHED,
                       instance=experiment_group,
                       previous_status=previous_status)


@receiver(post_save,
          sender=ExperimentGroupIteration,
          dispatch_uid="experiment_group_iteration_saved")
@ignore_updates
@ignore_raw
def new_experiment_group_iteration(sender, **kwargs):
    instance = kwargs['instance']
    auditor.record(event_type=EXPERIMENT_GROUP_ITERATION,
                   instance=instance.experiment_group)
