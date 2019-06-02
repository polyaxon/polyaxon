from hestia.signal_decorators import ignore_raw, ignore_updates, ignore_updates_pre

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from constants.backends import NATIVE_BACKEND
from db.models.pipelines import Pipeline, PipelineRun
from lifecycles.pipelines import PipelineLifeCycle
from signals.backend import set_backend


@receiver(pre_save, sender=Pipeline, dispatch_uid="pipeline_pre_save")
@ignore_updates_pre
@ignore_raw
def pipeline_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    set_backend(instance=instance, default_backend=NATIVE_BACKEND)


@receiver(post_save, sender=PipelineRun, dispatch_uid="pipeline_run_post_save")
@ignore_updates
@ignore_raw
def pipeline_run_post_save(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(PipelineLifeCycle.CREATED)
