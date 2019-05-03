from hestia.signal_decorators import ignore_raw, ignore_updates

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from db.models.pipelines import OperationRun, PipelineRun
from lifecycles.pipelines import PipelineLifeCycle


@receiver(post_save, sender=PipelineRun, dispatch_uid="pipeline_run_saved")
@ignore_updates
@ignore_raw
def new_pipeline_run(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(PipelineLifeCycle.CREATED)


@receiver(pre_delete, sender=OperationRun, dispatch_uid="operation_run_deleted")
@ignore_raw
def operation_run_deleted(sender, **kwargs):
    instance = kwargs['instance']
    instance.entity.delete()
