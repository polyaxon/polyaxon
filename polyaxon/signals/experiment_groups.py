from hestia.signal_decorators import ignore_raw, ignore_updates, ignore_updates_pre

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from constants.experiment_groups import ExperimentGroupLifeCycle
from db.models.experiment_groups import ExperimentGroup, GroupTypes
from libs.repos.utils import assign_code_reference
from schemas.hptuning import SearchAlgorithms
from signals.names import set_name
from signals.persistence import set_persistence
from signals.tags import set_tags


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
    # Set type
    if not instance.hptuning:
        instance.group_type = GroupTypes.SELECTION
    else:
        instance.group_type = GroupTypes.STUDY
    set_name(instance=instance, query=ExperimentGroup.all)


@receiver(post_save, sender=ExperimentGroup, dispatch_uid="experiment_group_saved")
@ignore_updates
@ignore_raw
def new_experiment_group(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(ExperimentGroupLifeCycle.CREATED)
    # TODO: Clean outputs and logs
