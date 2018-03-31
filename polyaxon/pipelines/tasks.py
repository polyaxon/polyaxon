import logging

from pipelines.utils import (
    get_pipeline_run,
    stop_operation_runs_for_pipeline_run,
    skip_operation_runs_for_pipeline_run,
    get_operation_run,
)
from polyaxon.celery_api import app as celery_app

from pipelines import dags
from pipelines.constants import OperationStatuses, PipelineStatuses
from polyaxon.config_settings import CeleryTasks, Intervals

logger = logging.getLogger('polyaxon.tasks.pipelines')


@celery_app.task(name=CeleryTasks.PIPELINES_START, bind=True, max_retries=None)
def start_pipeline_run(self, pipeline_run_id):
    pipeline_run = get_pipeline_run(pipeline_run_id=pipeline_run_id)
    if not pipeline_run:
        logger.info('Pipeline `{}` does not exist any more.'.format(pipeline_run_id))

    pipeline_run.on_schedule()
    dag, op_runs = pipeline_run.dag
    independent_op_run_ids = dags.get_independent_nodes(dag=dag)
    op_runs_to_start = [op_runs[op_run_id] for op_run_id in independent_op_run_ids
                        if op_runs[op_run_id].last_status == OperationStatuses.CREATED]
    concurrency = pipeline_run.pipeline.concurrency
    concurrency = concurrency or len(op_runs_to_start)
    while op_runs_to_start:
        op_run = op_runs_to_start.pop()
        start_operation_run.delay(operation_run_id=op_run.id)
        concurrency -= 1
        if concurrency == 0:
            break

    if op_runs_to_start:
        # Schedule another task
        self.retry(countdown=Intervals.PIPELINES_SCHEDULER)


@celery_app.task(name=CeleryTasks.PIPELINES_STOP_OPERATIONS)
def start_operation_run(operation_run_id):
    operation_run = get_operation_run(operation_run_id=operation_run_id)
    if not operation_run:
        logger.info('Operation `{}` does not exist any more.'.format(operation_run_id))

    operation_run.schedule_start()


@celery_app.task(name=CeleryTasks.PIPELINES_STOP_OPERATIONS, bind=True, max_retries=None)
def stop_pipeline_operation_runs(pipeline_run_id, message=None):
    pipeline_run = get_pipeline_run(pipeline_run_id=pipeline_run_id)
    if not pipeline_run:
        logger.info('Pipeline `{}` does not exist any more.'.format(pipeline_run_id))

    stop_operation_runs_for_pipeline_run(pipeline_run, message=message)


@celery_app.task(name=CeleryTasks.PIPELINES_SKIP_OPERATIONS, bind=True, max_retries=None)
def skip_pipeline_operation_runs(pipeline_run_id, message=None):
    pipeline_run = get_pipeline_run(pipeline_run_id=pipeline_run_id)
    if not pipeline_run:
        logger.info('Pipeline `{}` does not exist any more.'.format(pipeline_run_id))

    # We stop all op runs first
    stop_operation_runs_for_pipeline_run(pipeline_run, message=message)
    # Then we marked them as skipped
    skip_operation_runs_for_pipeline_run(pipeline_run, message=message)


@celery_app.task(name=CeleryTasks.PIPELINES_CHECK_STATUS, ignore_result=True)
def check_pipeline_run_status(pipeline_run_id, status, message=None):
    pipeline_run = get_pipeline_run(pipeline_run_id=pipeline_run_id)
    if not pipeline_run:
        logger.info('Pipeline `{}` does not exist any more.'.format(pipeline_run_id))

    if status in [OperationStatuses.FAILED, OperationStatuses.SUCCEEDED]:
        status = PipelineStatuses.FINISHED
    pipeline_run.set_status(status=status, message=message)
