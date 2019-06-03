from hestia.signal_decorators import ignore_raw

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_delete
from django.dispatch import receiver

import workers

from db.models.operations import OperationRun
from lifecycles.operations import OperationStatuses
from polyaxon.settings import PipelinesCeleryTasks


@receiver(pre_delete, sender=OperationRun, dispatch_uid="operation_run_pre_delete")
@ignore_raw
def operation_run_pre_delete(sender, **kwargs):
    instance = kwargs['instance']
    instance.entity.delete()


def new_operation_run_status(entity_type, entity, status):
    # TODO: may be move this to the executor, and think about making it an async task
    # If status is created, then the entity is still not set on the op
    # Set the entity and status to created
    if status == OperationStatuses.CREATED:
        return

    try:
        operation_run = OperationRun.objects.get(entity_content_type__model=entity_type,
                                                 entity_object_id=entity.id)
    except ObjectDoesNotExist:
        return

    pipeline_run = operation_run.pipeline_run
    # Update job last_status
    operation_run.status = status
    operation_run.save(update_fields=['status'])

    # Check if we need to update the pipeline_run's status
    workers.send(
        PipelinesCeleryTasks.PIPELINES_CHECK_STATUSES,
        kwargs={'pipeline_run_id': pipeline_run.id, 'status': status},
        countdown=None)
    if operation_run.is_done:
        # Notify downstream that instance is done, and that its dependency can start.
        downstream_runs = operation_run.downstream_runs.filter(status__isnull=True)
        for op_run in downstream_runs:
            workers.send(
                PipelinesCeleryTasks.PIPELINES_START_OPERATION,
                kwargs={'operation_run_id': op_run.id},
                countdown=None)
