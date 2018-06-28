from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.utils.timezone import now

import auditor

from constants.experiment_groups import ExperimentGroupLifeCycle
from db.models.experiment_groups import ExperimentGroup, ExperimentGroupStatus
from event_manager.events.experiment_group import (
    EXPERIMENT_GROUP_CREATED,
    EXPERIMENT_GROUP_DELETED,
    EXPERIMENT_GROUP_DONE,
    EXPERIMENT_GROUP_NEW_STATUS,
    EXPERIMENT_GROUP_STOPPED
)
from libs.decorators import check_specification, ignore_raw, ignore_updates, ignore_updates_pre
from libs.paths.experiment_groups import (
    delete_experiment_group_logs,
    delete_experiment_group_outputs
)
from libs.repos.utils import assign_code_reference
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks
from polyaxon_schemas.utils import SearchAlgorithms
from signals.run_time import set_finished_at, set_started_at
from signals.utils import set_persistence, set_tags


@receiver(pre_save, sender=ExperimentGroup, dispatch_uid="experiment_group_pre_save")
@ignore_updates_pre
@ignore_raw
def experiment_group_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    # Add code reference
    assign_code_reference(instance)
    # Check if params need to be set
    if not instance.hptuning and instance.specification:
        hptuning_config = instance.specification.hptuning
        hptuning = hptuning_config.to_dict()
        if hptuning_config.search_algorithm == SearchAlgorithms.GRID:
            hptuning['grid_search'] = hptuning.get('grid_search', {})
        instance.hptuning = hptuning
    set_tags(instance=instance)
    set_persistence(instance=instance)


@receiver(post_save, sender=ExperimentGroup, dispatch_uid="experiment_group_saved")
@ignore_updates
@ignore_raw
def new_experiment_group(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(ExperimentGroupLifeCycle.CREATED)
    # Clean outputs and logs
    delete_experiment_group_outputs(
        persistence_outputs=instance.persistence_outputs,
        experiment_group_name=instance.unique_name)
    delete_experiment_group_logs(instance.unique_name)
    auditor.record(event_type=EXPERIMENT_GROUP_CREATED,
                   instance=instance)


@receiver(post_save, sender=ExperimentGroup, dispatch_uid="experiment_group_create_experiments")
@check_specification
@ignore_updates
@ignore_raw
def experiment_group_create_experiments(sender, **kwargs):
    instance = kwargs['instance']
    celery_app.send_task(
        SchedulerCeleryTasks.EXPERIMENTS_GROUP_CREATE,
        kwargs={'experiment_group_id': instance.id},
        countdown=1)


@receiver(pre_delete, sender=ExperimentGroup, dispatch_uid="experiment_group_pre_delete")
@ignore_raw
def experiment_group_pre_delete(sender, **kwargs):
    """Delete all group outputs."""
    instance = kwargs['instance']

    # Delete outputs and logs
    delete_experiment_group_outputs(
        persistence_outputs=instance.persistence_outputs,
        experiment_group_name=instance.unique_name)
    delete_experiment_group_logs(instance.unique_name)


@receiver(post_delete, sender=ExperimentGroup, dispatch_uid="experiment_group_post_delete")
@ignore_raw
def experiment_group_post_delete(sender, **kwargs):
    """Delete all group outputs."""
    instance = kwargs['instance']
    auditor.record(event_type=EXPERIMENT_GROUP_DELETED,
                   instance=instance)


@receiver(post_save, sender=ExperimentGroupStatus, dispatch_uid="experiment_group_status_post_save")
@ignore_updates
@ignore_raw
def experiment_group_status_post_save(sender, **kwargs):
    instance = kwargs['instance']
    experiment_group = instance.experiment_group
    previous_status = experiment_group.last_status

    # update experiment last_status
    experiment_group.status = instance
    if instance.status == ExperimentGroupLifeCycle.RUNNING:
        experiment_group.started_at = now()

    set_started_at(instance=experiment_group,
                   status=instance.status,
                   starting_statuses=[ExperimentGroupLifeCycle.RUNNING])
    set_finished_at(instance=experiment_group,
                    status=instance.status,
                    is_done=ExperimentGroupLifeCycle.is_done)
    experiment_group.save()
    auditor.record(event_type=EXPERIMENT_GROUP_NEW_STATUS,
                   instance=experiment_group,
                   previous_status=previous_status)

    if instance.status == ExperimentGroupLifeCycle.STOPPED:
        auditor.record(event_type=EXPERIMENT_GROUP_STOPPED,
                       instance=experiment_group,
                       previous_status=previous_status)

    if ExperimentGroupLifeCycle.is_done(instance.status):
        auditor.record(event_type=EXPERIMENT_GROUP_DONE,
                       instance=experiment_group,
                       previous_status=previous_status)
