import logging

from db.models.operations import OperationRun

_logger = logging.getLogger('polyaxon.db')


def get_valid_operation_run(operation_run_id: int = None,
                            operation_run_uuid: str = None,
                            include_deleted: bool = False):
    cond = (not any([operation_run_id, operation_run_uuid]) or
            all([operation_run_id, operation_run_uuid]))
    if cond:
        raise ValueError('`get_valid_operation` function expects an operation id or uuid.')

    try:
        qs = OperationRun.all if include_deleted else OperationRun.objects
        if operation_run_uuid:
            op_run = qs.get(uuid=operation_run_uuid)
        else:
            op_run = qs.get(id=operation_run_id)
    except OperationRun.DoesNotExist:
        _logger.info('OperationRun `%s` does not exist', operation_run_id or operation_run_uuid)
        return None

    return op_run


def is_operation_run_still_running(operation_run_id: int = None,
                                   operation_run_uuid: str = None):
    op_run = get_valid_operation_run(operation_run_id=operation_run_id,
                                     operation_run_uuid=operation_run_uuid)

    if not op_run or not op_run.is_running:
        return False

    return True
