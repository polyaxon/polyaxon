from django.db.models import F, Max

from pipelines import dags
from pipelines.models import PipelineRun, OperationRun


def set_op_upstreams(op_run, op):
    """Set the upstream operations for operation run."""
    # We get a list of all upstream ops or the current op
    upstream_ops = op.upstream_operations.values_list('id', flat=True)
    # We get latest op runs for the upstream_ops
    latest_op_runs = OperationRun.objects.filter(id__in=upstream_ops)
    latest_op_runs = latest_op_runs.annotate(max_date=Max('created_at'))
    latest_op_runs = latest_op_runs.filter(date=F('max_date'))
    # Set the upstream ops
    op_run.set(latest_op_runs)


def set_topological_dag_upstreams(dag, ops, op_runs, runs_by_ops):
    """Set the upstream runs for the operation runs in the dag following the topological sort."""
    sorted_ops = dags.sort_topologically(dag=dag)
    for op_id in sorted_ops:
        op_run_id = runs_by_ops[op_id]
        op_run = op_runs[op_run_id]
        set_op_upstreams(op_run=op_run, op=ops[op_id])


def create_pipeline_run(pipeline, context_by_op):
    """Create a pipeline run/instance."""
    pipeline_run = PipelineRun.objects.create(pipeline=pipeline)
    dag, ops = pipeline.dag
    # Go trough the operation and create operation runs and the upstreams
    op_runs = {}
    runs_by_ops = {}
    for op_id in dag.keys():
        op_run = OperationRun.objects.create(
            pipeline_run=pipeline_run,
            operation_id=op_id,
            celery_task_context=context_by_op.get(op_id))
        op_run_id = op_run.id
        op_runs[op_run_id] = op_run
        runs_by_ops[op_id] = op_run_id

    # Create operations upstreams
    # We set the upstream for the topologically sorted dag
    set_topological_dag_upstreams(dag=dag, ops=ops, op_runs=op_runs, runs_by_ops=runs_by_ops)


def get_pipeline_run(pipeline_run_id=None, pipeline_run_uuid=None):
    if not any([pipeline_run_id, pipeline_run_uuid]) or all([pipeline_run_id, pipeline_run_uuid]):
        raise ValueError('`get_pipeline_run` function expects a pipeline run id or uuid.')

    try:
        if pipeline_run_uuid:
            return PipelineRun.objects.get(uuid=pipeline_run_uuid)
        else:
            return PipelineRun.objects.get(id=pipeline_run_id)
    except PipelineRun.DoesNotExist:
        return None


def get_operation_run(operation_run_id=None, operation_run_uuid=None):
    args = [operation_run_id, operation_run_uuid]
    if not any(args) or all(args):
        raise ValueError('`get_operation_run` function expects an operation run id or uuid.')

    try:
        if operation_run_uuid:
            return OperationRun.objects.get(uuid=operation_run_uuid)
        else:
            return OperationRun.objects.get(id=operation_run_id)
    except OperationRun.DoesNotExist:
        return None


def stop_operation_runs_for_pipeline_run(pipeline_run, message=None):
    for op_run in pipeline_run.operation_runs.all():
        op_run.stop(message=message)


def skip_operation_runs_for_pipeline_run(pipeline_run, message=None):
    for op_run in pipeline_run.operation_runs.all():
        op_run.skip(message=message)
