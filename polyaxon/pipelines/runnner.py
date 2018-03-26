from django.db.models import F, Max

from pipelines import dags
from pipelines.models import PipelineRun, OperationRun


def set_op_upstreams(op_run, op):
    # We get a list of all upstream ops or the current op
    upstream_ops = op.upstream_operations.values_list('id', flat=True)
    # We get latest op runs for the upstream_ops
    latest_op_runs = OperationRun.objects.filter(id__in=upstream_ops)
    latest_op_runs = latest_op_runs.annotate(max_date=Max('created_at'))
    latest_op_runs = latest_op_runs.filter(date=F('max_date'))
    # Set the upstream ops
    op_run.set(latest_op_runs)


def set_orphan_ops_upstreams(dag, ops, op_runs, runs_by_ops):
    orphan_ops = dags.get_orphan_operations(dag)
    for op_id in orphan_ops:
        op_run_id = runs_by_ops[op_id]
        op_run = op_runs[op_run_id]
        set_op_upstreams(op_run=op_run, op=ops[op_id])


def set_topological_dag_upstreams(dag, ops, op_runs, runs_by_ops):
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
    # 1. We set first the upstream for orphan operations
    set_orphan_ops_upstreams(dag=dag, ops=ops, op_runs=op_runs, runs_by_ops=runs_by_ops)

    # 2. We set the upstream for topologically sorted dag
    set_topological_dag_upstreams(dag=dag, ops=ops, op_runs=op_runs, runs_by_ops=runs_by_ops)
