from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from constants.pipelines import OperationStatuses, PipelineStatuses
from db.models.pipelines import OperationRun, OperationRunStatus, PipelineRun, PipelineRunStatus
from libs.decorators import ignore_raw, ignore_updates
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import PipelineCeleryTasks


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
        celery_app.send_task(
            PipelineCeleryTasks.PIPELINES_STOP_OPERATIONS,
            kwargs={'pipeline_run_id': pipeline_run.id,
                    'message': 'Pipeline run was stopped'})
    if pipeline_run.skipped:
        celery_app.send_task(
            PipelineCeleryTasks.PIPELINES_SKIP_OPERATIONS,
            kwargs={'pipeline_run_id': pipeline_run.id,
                    'message': 'Pipeline run was skipped'})


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
    celery_app.send_task(
        PipelineCeleryTasks.PIPELINES_CHECK_STATUSES,
        kwargs={'pipeline_run_id': pipeline_run.id,
                'status': instance.status,
                'message': instance.message})
    if operation_run.is_done:
        # Notify downstream that instance is done, and that its dependency can start.
        downstream_runs = operation_run.downstream_runs.filter(
            status__status=OperationStatuses.CREATED)
        for op_run in downstream_runs:
            celery_app.send_task(
                PipelineCeleryTasks.PIPELINES_START_OPERATION,
                kwargs={'operation_run_id': op_run.id})


@receiver(pre_delete, sender=OperationRun, dispatch_uid="operation_run_deleted")
@ignore_raw
def operation_run_deleted(sender, **kwargs):
    instance = kwargs['instance']
    instance.stop()
