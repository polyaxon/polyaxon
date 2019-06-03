import workers

from operations.manager.skip import skip_entity
from operations.manager.stop import stop_entity
from polyaxon.settings import OperationsCeleryTasks


def start_operation_run(operation_run: 'OperationRun') -> bool:
    """Schedule the task: check first if the task can start:
        1. we check that the task is still in the CREATED state.
        2. we check that the upstream dependency is met.
        3. we check that pipeline can start a new task;
          i.e. we check the concurrency of the pipeline.
        4. we check that operation can start a new instance;
          i.e. we check the concurrency of the operation.

    -> If all checks pass we schedule the task start it.

    -> 1. If the operation is not in created status, nothing to do.
    -> 2. If the upstream dependency check is not met, two use cases need to be validated:
        * The upstream dependency is not met but could be met in the future,
          because some ops are still CREATED/SCHEDULED/RUNNING/...
          in this case nothing need to be done, every time an upstream operation finishes,
          it will notify all the downstream ops including this one.
        * The upstream dependency is not met and could not be met at all.
          In this case we need to mark the task with `UPSTREAM_FAILED`.
    -> 3. If the pipeline has reached it's concurrency limit,
       we just delay schedule based on the interval/time delay defined by the user.
       The pipeline scheduler will keep checking until the task can be scheduled or stopped.
    -> 4. If the operation has reached it's concurrency limit,
       Same as above we keep trying based on an interval defined by the user.

    Returns:
        boolean: Whether to try to schedule this operation run in the future or not.
    """
    if operation_run.entity is not None:
        # This operation has already scheduled an entity
        return False

    upstream_trigger_check = operation_run.check_upstream_trigger()
    if not upstream_trigger_check and operation_run.is_upstream_done:
        # This task cannot be scheduled anymore
        operation_run.on_upstream_failed()
        return False

    if not operation_run.pipeline_run.check_concurrency():
        return True

    if not operation_run.check_concurrency():
        return True

    workers.send(
        OperationsCeleryTasks.START_OPERATION,
        kwargs={'operation_run_id': operation_run.id},
        **operation_run.operation.get_run_params(),
    )
    return False


def stop_operation_run(operation_run: 'OperationRun', message: str = None) -> None:
    stop_entity(operation_run=operation_run, message=message)


def skip_operation_run(operation_run: 'OperationRun', message: str = None) -> None:
    skip_entity(operation_run=operation_run, message=message)
