from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from libs.decorators import ignore_raw, ignore_updates
from constants.pipelines import OperationStatuses, PipelineStatuses
from models.pipelines import OperationRun, OperationRunStatus, PipelineRun, PipelineRunStatus
from pipelines.tasks import (
    check_pipeline_run_status,
    skip_pipeline_operation_runs,
    start_operation_run,
    stop_pipeline_operation_runs
)


@receiver(post_save, sender=PipelineRun, dispatch_uid="pipeline_run_saved")
@ignore_updates
@ignore_raw
def new_pipeline_run(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(PipelineStatuses.CREATED)


@receiver(post_save, sender=OperationRun, dispatch_uid="operation_run_saved")
@ignore_updates
@ignore_raw
def new_operation_run(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(OperationStatuses.CREATED)


@receiver(post_save, sender=PipelineRunStatus, dispatch_uid="new_pipeline_run_status_saved")
@ignore_updates
@ignore_raw
def new_pipeline_run_status(sender, **kwargs):
    instance = kwargs['instance']
    pipeline_run = instance.pipeline_run
    # Update job last_status
    pipeline_run.status = instance
    pipeline_run.save()
    # Notify operations with status change. This is necessary if we skip or stop the dag run.
    if pipeline_run.stopped:
        stop_pipeline_operation_runs.delay(pipeline_run_id=pipeline_run.id,
                                           message='Pipeline run was stopped')
    if pipeline_run.skipped:
        skip_pipeline_operation_runs.delay(pipeline_run_id=pipeline_run.id,
                                           message='Pipeline run was skipped')


@receiver(post_save, sender=OperationRunStatus, dispatch_uid="new_operation_run_status_saved")
@ignore_updates
@ignore_raw
def new_operation_run_status(sender, **kwargs):
    instance = kwargs['instance']
    operation_run = instance.operation_run
    pipeline_run = operation_run.pipeline_run
    # Update job last_status
    operation_run.status = instance
    operation_run.save()

    # No need to check if it is just created
    if instance.status == OperationStatuses.CREATED:
        return

    # Check if we need to update the pipeline_run's status
    check_pipeline_run_status.delay(pipeline_run_id=pipeline_run.id,
                                    status=instance.status,
                                    message=instance.message)
    if operation_run.is_done:
        # Notify downstream that instance is done, and that its dependency can start.
        downstream_runs = operation_run.downstream_runs.filter(
            status__status=OperationStatuses.CREATED)
        for op_run in downstream_runs:
            start_operation_run.delay(operation_run_id=op_run.id)


@receiver(pre_delete, sender=OperationRun, dispatch_uid="operation_run_deleted")
@ignore_raw
def operation_run_deleted(sender, **kwargs):
    instance = kwargs['instance']
    instance.stop()
