import logging

from db.models.pipelines import PipelineRun

_logger = logging.getLogger('polyaxon.db')


def get_valid_pipeline_run(pipeline_run_id: int = None,
                           pipeline_run_uuid: str = None,
                           include_deleted: bool = False):
    cond = (not any([pipeline_run_id, pipeline_run_uuid]) or
            all([pipeline_run_id, pipeline_run_uuid]))
    if cond:
        raise ValueError('`get_valid_pipeline` function expects an pipeline id or uuid.')

    try:
        qs = PipelineRun.all if include_deleted else PipelineRun.objects
        if pipeline_run_uuid:
            op_run = qs.get(uuid=pipeline_run_uuid)
        else:
            op_run = qs.get(id=pipeline_run_id)
    except PipelineRun.DoesNotExist:
        _logger.info('PipelineRun `%s` does not exist', pipeline_run_id or pipeline_run_uuid)
        return None

    return op_run


def is_pipeline_run_still_running(pipeline_run_id: int = None,
                                  pipeline_run_uuid: str = None):
    op_run = get_valid_pipeline_run(pipeline_run_id=pipeline_run_id,
                                    pipeline_run_uuid=pipeline_run_uuid)

    if not op_run or not op_run.is_running:
        return False

    return True
