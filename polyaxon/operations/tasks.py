from db.getters.operations import get_valid_operation_run
from lifecycles.operations import OperationStatuses
from operations.manager import create_entity
from polyaxon.celery_api import celery_app
from polyaxon.settings import OperationsCeleryTasks


@celery_app.task(name=OperationsCeleryTasks.START_OPERATION, ignore_result=True)
def start_operation(operation_run_id):
    op_run = get_valid_operation_run(operation_run_id=operation_run_id)
    operation = op_run.operation
    pipeline = operation.pipeline
    op_run.entity = create_entity(user_id=pipeline.user_id,
                                  project_id=pipeline.project_id,
                                  entity_type=operation.entity_type,
                                  content=operation.content)
    op_run.status = OperationStatuses.CREATED
    op_run.save()
