from hestia.signal_decorators import ignore_raw, ignore_updates, ignore_updates_pre

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from constants.jobs import JobLifeCycle
from db.models.tensorboards import TensorboardJob
from libs.repos.utils import assign_code_reference
from signals.names import set_name
from signals.outputs import set_outputs, set_outputs_refs
from signals.persistence import set_persistence
from signals.tags import set_tags


@receiver(pre_save, sender=TensorboardJob, dispatch_uid="tensorboard_job_pre_save")
@ignore_updates_pre
@ignore_raw
def tensorboard_job_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    set_tags(instance=instance)
    default_persistence_outputs = None
    if instance.experiment:
        default_persistence_outputs = instance.experiment.persistence_outputs
    if instance.experiment_group:
        default_persistence_outputs = instance.experiment_group.persistence_outputs
    set_persistence(instance=instance, default_persistence_outputs=default_persistence_outputs)
    set_outputs(instance=instance)
    set_outputs_refs(instance=instance)
    assign_code_reference(instance)
    set_name(instance=instance, query=TensorboardJob.all)


@receiver(post_save, sender=TensorboardJob, dispatch_uid="tensorboard_job_post_save")
@ignore_updates
@ignore_raw
def tensorboard_job_post_save(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(status=JobLifeCycle.CREATED)
