import logging

from pipelines import dags
from pipelines.constants import OperationStatuses, PipelineStatuses
from pipelines.utils import (
    get_operation_run,
    get_pipeline_run,
    skip_operation_runs_for_pipeline_run,
    stop_operation_runs_for_pipeline_run
)
from polyaxon.celery_api import app as celery_app
from polyaxon.config_settings import CeleryTasks, Intervals

logger = logging.getLogger('polyaxon.tasks.pipelines')


@celery_app.task(name=CeleryTasks.PIPELINES_START, bind=True, max_retries=None)
def start_pipeline_run(self, pipeline_run_id):
    pipeline_run = get_pipeline_run(pipeline_run_id=pipeline_run_id)
    if not pipeline_run:
        logger.info('Pipeline `%s` does not exist any more.', pipeline_run_id)

    pipeline_run.on_schedule()
    dag, op_runs = pipeline_run.dag
    sorted_ops = dags.sort_topologically(dag=dag)
    op_runs_to_start = [op_runs[op_run_id] for op_run_id in sorted_ops
                        if op_runs[op_run_id].last_status == OperationStatuses.CREATED]
    concurrency = pipeline_run.pipeline.n_operation_runs_to_start
    future_check = False
    while op_runs_to_start and concurrency > 0:
        op_run = op_runs_to_start.pop()
        if op_run.schedule_start():
            # If we end up here it means that the task
            future_check = True
        else:
            concurrency -= 1

    if op_runs_to_start or future_check:
        # Schedule another task
        self.retry(countdown=Intervals.PIPELINES_SCHEDULER)


@celery_app.task(name=CeleryTasks.PIPELINES_START_OPERATION)
def start_operation_run(operation_run_id):
    operation_run = get_operation_run(operation_run_id=operation_run_id)
    if not operation_run:
        logger.info('Operation `%s` does not exist any more.', operation_run_id)

    operation_run.schedule_start()


@celery_app.task(name=CeleryTasks.PIPELINES_STOP_OPERATIONS, ignore_result=True)
def stop_pipeline_operation_runs(pipeline_run_id, message=None):
    pipeline_run = get_pipeline_run(pipeline_run_id=pipeline_run_id)
    if not pipeline_run:
        logger.info('Pipeline `%s` does not exist any more.', pipeline_run_id)

    stop_operation_runs_for_pipeline_run(pipeline_run, message=message)


@celery_app.task(name=CeleryTasks.PIPELINES_SKIP_OPERATIONS, ignore_result=True)
def skip_pipeline_operation_runs(pipeline_run_id, message=None):
    pipeline_run = get_pipeline_run(pipeline_run_id=pipeline_run_id)
    if not pipeline_run:
        logger.info('Pipeline `%s` does not exist any more.', pipeline_run_id)

    # We stop all op runs first
    stop_operation_runs_for_pipeline_run(pipeline_run, message=message)
    # Then we marked them as skipped
    skip_operation_runs_for_pipeline_run(pipeline_run, message=message)


@celery_app.task(name=CeleryTasks.PIPELINES_CHECK_STATUS, ignore_result=True)
def check_pipeline_run_status(pipeline_run_id, status, message=None):
    pipeline_run = get_pipeline_run(pipeline_run_id=pipeline_run_id)
    if not pipeline_run:
        logger.info('Pipeline `%s` does not exist any more.', pipeline_run_id)

    if status in OperationStatuses.DONE_STATUS:
        status = PipelineStatuses.FINISHED
    pipeline_run.set_status(status=status, message=message)
