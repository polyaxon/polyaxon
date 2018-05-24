from django.db.models.signals import post_save
from django.dispatch import receiver

import auditor

from event_manager.events.experiment_group import EXPERIMENT_GROUP_ITERATION
from db.models.experiment_groups import ExperimentGroupIteration
from libs.decorators import ignore_raw, ignore_updates


@receiver(post_save,
          sender=ExperimentGroupIteration,
          dispatch_uid="experiment_group_iteration_saved")
@ignore_updates
@ignore_raw
def new_experiment_group_iteration(sender, **kwargs):
    instance = kwargs['instance']
    auditor.record(event_type=EXPERIMENT_GROUP_ITERATION,
                   instance=instance.experiment_group)
