from django.db.models.signals import post_save
from django.dispatch import receiver

from libs.decorators import ignore_raw
from pipelines.constants import OperationStatuses
from pipelines.models import PipelineRunStatus, OperationRunStatus
from pipelines.tasks import (
    check_pipeline_run_status,
    start_operation_run,
    stop_pipeline_operation_runs,
    skip_pipeline_operation_runs,
)


@receiver(post_save, sender=PipelineRunStatus, dispatch_uid="new_pipeline_run_status_saved")
@ignore_raw
def new_pipeline_run_status(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    if created:
        pipeline_run = instance.pipeline_run
        # Update job last_status
        pipeline_run.status = instance
        pipeline_run.save()
        # Notify operations with status change. This is necessary if we skip or stop the dag run.
        if pipeline_run.stopped():
            stop_pipeline_operation_runs.delay(pipeline_run_id=pipeline_run.id,
                                               message='Pipeline run was stopped')
        if pipeline_run.skipped():
            skip_pipeline_operation_runs.delay(pipeline_run_id=pipeline_run.id,
                                               message='Pipeline run was skipped')


@receiver(post_save, sender=OperationRunStatus, dispatch_uid="new_pipeline_run_status_saved")
@ignore_raw
def new_operation_run_status(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    if not created:
        return

    operation_run = instance.operation_run
    pipeline_run = operation_run.pipeline_run
    # Update job last_status
    operation_run.status = instance
    operation_run.save()

    # Check if we need to update the pipeline_run's status
    check_pipeline_run_status.delay(pipline_run_uuid=pipeline_run.uuid.hex,
                                    status=instance.status,
                                    message=instance.message)
    if operation_run.is_done():
        # Notify downstream that instance is done, and that its dependency can start.
        for op_run in operation_run.downstream_runs.filter(status=OperationStatuses.CREATED):
            start_operation_run.delay(operation_run_id=op_run.id)
