from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from factories.pipelines import (
    OperationFactory,
    PipelineFactory,
    PipelineRunFactory,
    OperationRunFactory,
)
from pipelines.constants import OperationStatuses, TriggerPolicy
from pipelines.models import OperationRunStatus
from tests.utils import BaseTest


class TestPipelineModel(BaseTest):
    def test_dag_property(self):
        pipeline = PipelineFactory()
        operations = [OperationFactory(pipeline=pipeline) for _ in range(4)]
        operations[0].upstream_operations.set(operations[2:])
        operations[1].upstream_operations.set(operations[2:])
        operation_by_ids = {op.id: op for op in operations}
        assert pipeline.dag == (
            {
                operations[0].id: set(),
                operations[1].id: set(),
                operations[2].id: {operations[0].id, operations[1].id},
                operations[3].id: {operations[0].id, operations[1].id},
            },
            operation_by_ids
        )

        # Add operations outside the dag
        operation1 = OperationFactory()
        operation1.downstream_operations.set([operations[1], operations[2], operations[3]])

        operation2 = OperationFactory()
        operation2.upstream_operations.set([operations[0], operations[2]])

        assert pipeline.dag == (
            {
                operations[0].id: {operation2.id, },
                operations[1].id: set(),
                operations[2].id: {operations[0].id, operations[1].id, operation2.id},
                operations[3].id: {operations[0].id, operations[1].id},
            },
            operation_by_ids
        )


class TestOperationModel(BaseTest):
    def test_get_countdown(self):
        operation = OperationFactory(retry_delay=5)
        assert operation.get_countdown(1) == 5
        assert operation.get_countdown(2) == 5

        # Test exponential backoff
        operation.retry_exponential_backoff = True
        operation.max_retry_delay = 24
        operation.save()
        assert operation.get_countdown(1) == 5
        assert operation.get_countdown(2) == 5
        assert operation.get_countdown(3) == 8
        assert operation.get_countdown(4) == 16
        assert operation.get_countdown(5) == 24  # Max retry delay

    def test_get_run_params(self):
        operation = OperationFactory()
        assert operation.get_run_params() == {}

        operation.celery_queue = 'dummy_queue'
        operation.save()
        assert operation.get_run_params() == {'queue': 'dummy_queue'}

        operation.timeout = 10
        operation.save()

        assert operation.get_run_params() == {
            'queue': 'dummy_queue',
            'soft_time_limit': 10,
            'time_limit': settings.CELERY_HARD_TIME_LIMIT_DELAY + 10,
        }

        operation.execute_at = timezone.now() + timedelta(hours=1)
        operation.save()
        assert operation.get_run_params() == {
            'queue': 'dummy_queue',
            'soft_time_limit': 10,
            'time_limit': settings.CELERY_HARD_TIME_LIMIT_DELAY + 10,
            'eta': operation.execute_at
        }


class TestPipelineRunModel(BaseTest):
    def test_dag_property(self):
        pipeline_run = PipelineRunFactory()
        operation_runs = [OperationRunFactory(pipeline_run=pipeline_run) for _ in range(4)]
        operation_runs[0].upstream_runs.set(operation_runs[2:])
        operation_runs[1].upstream_runs.set(operation_runs[2:])
        operation_by_ids = {op.id: op for op in operation_runs}
        assert pipeline_run.dag == (
            {
                operation_runs[0].id: set(),
                operation_runs[1].id: set(),
                operation_runs[2].id: {operation_runs[0].id, operation_runs[1].id},
                operation_runs[3].id: {operation_runs[0].id, operation_runs[1].id},
            },
            operation_by_ids
        )

        # Add operations outside the dag
        operation_run1 = OperationRunFactory()
        operation_run1.downstream_runs.set([operation_runs[1], operation_runs[2], operation_runs[3]])

        operation_run2 = OperationRunFactory()
        operation_run2.upstream_runs.set([operation_runs[0], operation_runs[2]])

        assert pipeline_run.dag == (
            {
                operation_runs[0].id: {operation_run2.id, },
                operation_runs[1].id: set(),
                operation_runs[2].id: {operation_runs[0].id, operation_runs[1].id, operation_run2.id},
                operation_runs[3].id: {operation_runs[0].id, operation_runs[1].id},
            },
            operation_by_ids
        )

    def test_check_concurrency(self):
        # Pipeline without concurrency defaults to infinite concurrency
        pipeline = PipelineFactory()
        pipeline_run = PipelineRunFactory(pipeline=pipeline)
        assert pipeline_run.check_concurrency() is True

        # Pipeline with concurrency and pipeline run with operation runs
        pipeline.concurrency = 2
        pipeline.save()

        # No running operation runs
        assert pipeline_run.check_concurrency() is True

        # One operation run
        operation_run1 = OperationRunFactory(pipeline_run=pipeline_run)
        assert pipeline_run.check_concurrency() is True

        # One operation run with RUNNING status
        OperationRunStatus.objects.create(status=OperationStatuses.RUNNING,
                                          operation_run=operation_run1)
        assert pipeline_run.check_concurrency() is True

        # Second operation run
        operation_run2 = OperationRunFactory(pipeline_run=pipeline_run)
        assert pipeline_run.check_concurrency() is True

        # Second operation run with RUNNING status
        OperationRunStatus.objects.create(status=OperationStatuses.RUNNING,
                                          operation_run=operation_run2)
        assert pipeline_run.check_concurrency() is False


class TestOperationRunModel(BaseTest):
    def test_check_concurrency(self):
        # Operation without concurrency defaults to infinite concurrency
        operation = OperationFactory()
        operation_run = OperationRunFactory(operation=operation)
        assert operation_run.check_concurrency() is True

        # Operation with concurrency and operation run with operation runs
        operation.concurrency = 2
        operation.save()

        # No running operation runs
        assert operation_run.check_concurrency() is True

        # One operation run
        operation_run1 = OperationRunFactory(operation=operation)
        assert operation_run.check_concurrency() is True

        # One operation run with RUNNING status
        OperationRunStatus.objects.create(status=OperationStatuses.RUNNING,
                                          operation_run=operation_run1)
        assert operation_run.check_concurrency() is True

        # Second operation run
        operation_run2 = OperationRunFactory(operation=operation)
        assert operation_run.check_concurrency() is True

        # Second operation run with RUNNING status
        OperationRunStatus.objects.create(status=OperationStatuses.RUNNING,
                                          operation_run=operation_run2)
        assert operation_run.check_concurrency() is False

    def test_trigger_policy_one_done(self):
        operation_run = OperationRunFactory()
        operation = operation_run.operation
        operation.trigger_policy = TriggerPolicy.ONE_DONE
        operation.save()

        # No upstream
        assert operation_run.check_upstream_trigger() is False

        # Add non done upstream
        upstream_run1 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run1])
        assert operation_run.check_upstream_trigger() is False

        # A running upstream
        OperationRunStatus.objects.create(status=OperationStatuses.RUNNING,
                                          operation_run=upstream_run1)
        assert operation_run.check_upstream_trigger() is False

        # A failed upstream
        OperationRunStatus.objects.create(status=OperationStatuses.FAILED,
                                          operation_run=upstream_run1)
        assert operation_run.check_upstream_trigger() is True

        # Add skipped upstream
        upstream_run2 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run2])
        OperationRunStatus.objects.create(status=OperationStatuses.SKIPPED,
                                          operation_run=upstream_run2)
        assert operation_run.check_upstream_trigger() is True

        # Add succeeded upstream
        upstream_run3 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3])
        OperationRunStatus.objects.create(status=OperationStatuses.SUCCEEDED,
                                          operation_run=upstream_run3)
        assert operation_run.check_upstream_trigger() is True

        # Add another upstream still True
        upstream_run4 = OperationRunFactory()
        operation_run.upstream_runs.add(upstream_run4)
        assert operation_run.check_upstream_trigger() is True

    def test_trigger_policy_one_succeeded(self):
        operation_run = OperationRunFactory()
        operation = operation_run.operation
        operation.trigger_policy = TriggerPolicy.ONE_SUCCEEDED
        operation.save()

        # No upstream
        assert operation_run.check_upstream_trigger() is False

        # Add non done upstream
        upstream_run1 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run1])
        assert operation_run.check_upstream_trigger() is False

        # A running upstream
        OperationRunStatus.objects.create(status=OperationStatuses.RUNNING,
                                          operation_run=upstream_run1)
        assert operation_run.check_upstream_trigger() is False

        # A failed upstream
        OperationRunStatus.objects.create(status=OperationStatuses.FAILED,
                                          operation_run=upstream_run1)
        assert operation_run.check_upstream_trigger() is False

        # Add skipped upstream
        upstream_run2 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run2])
        OperationRunStatus.objects.create(status=OperationStatuses.SKIPPED,
                                          operation_run=upstream_run2)
        assert operation_run.check_upstream_trigger() is False

        # Add succeeded upstream
        upstream_run3 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3])
        OperationRunStatus.objects.create(status=OperationStatuses.SUCCEEDED,
                                          operation_run=upstream_run3)
        assert operation_run.check_upstream_trigger() is True

        # Add another upstream still True
        upstream_run4 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run1, upstream_run2, upstream_run3, upstream_run4])
        assert operation_run.check_upstream_trigger() is True

    def test_trigger_policy_one_failed(self):
        operation_run = OperationRunFactory()
        operation = operation_run.operation
        operation.trigger_policy = TriggerPolicy.ONE_FAILED
        operation.save()

        # No upstream
        assert operation_run.check_upstream_trigger() is False

        # Add non done upstream
        upstream_run1 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run1])
        assert operation_run.check_upstream_trigger() is False

        # A running upstream
        OperationRunStatus.objects.create(status=OperationStatuses.RUNNING,
                                          operation_run=upstream_run1)
        assert operation_run.check_upstream_trigger() is False

        # A failed upstream
        OperationRunStatus.objects.create(status=OperationStatuses.FAILED,
                                          operation_run=upstream_run1)
        assert operation_run.check_upstream_trigger() is True

        # Add skipped upstream
        upstream_run2 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run2])
        OperationRunStatus.objects.create(status=OperationStatuses.SKIPPED,
                                          operation_run=upstream_run2)
        assert operation_run.check_upstream_trigger() is False

        # Add succeeded upstream
        upstream_run3 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3])
        OperationRunStatus.objects.create(status=OperationStatuses.SUCCEEDED,
                                          operation_run=upstream_run3)
        assert operation_run.check_upstream_trigger() is False

        # Add another upstream still True
        upstream_run4 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run1, upstream_run2, upstream_run3, upstream_run4])
        assert operation_run.check_upstream_trigger() is True

    def test_trigger_policy_all_done(self):
        operation_run = OperationRunFactory()
        operation = operation_run.operation
        operation.trigger_policy = TriggerPolicy.ALL_DONE
        operation.save()

        # No upstream
        assert operation_run.check_upstream_trigger() is True

        # Add non done upstream
        upstream_run1 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run1])
        assert operation_run.check_upstream_trigger() is False

        # A running upstream
        OperationRunStatus.objects.create(status=OperationStatuses.RUNNING,
                                          operation_run=upstream_run1)
        assert operation_run.check_upstream_trigger() is False

        # A failed upstream
        OperationRunStatus.objects.create(status=OperationStatuses.FAILED,
                                          operation_run=upstream_run1)
        assert operation_run.check_upstream_trigger() is True

        # Add skipped upstream
        upstream_run2 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run2])
        OperationRunStatus.objects.create(status=OperationStatuses.SKIPPED,
                                          operation_run=upstream_run2)
        assert operation_run.check_upstream_trigger() is True

        # Add succeeded upstream
        upstream_run3 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3])
        OperationRunStatus.objects.create(status=OperationStatuses.SUCCEEDED,
                                          operation_run=upstream_run3)
        assert operation_run.check_upstream_trigger() is True

        # Many done upstreams
        operation_run.upstream_runs.set(
            [upstream_run1, upstream_run2, upstream_run3])
        assert operation_run.check_upstream_trigger() is True

        # Add another upstream
        upstream_run4 = OperationRunFactory()
        operation_run.upstream_runs.add(upstream_run4)
        assert operation_run.check_upstream_trigger() is False

    def test_trigger_policy_all_succeeded(self):
        operation_run = OperationRunFactory()
        operation = operation_run.operation
        operation.trigger_policy = TriggerPolicy.ALL_SUCCEEDED
        operation.save()

        # No upstream
        assert operation_run.check_upstream_trigger() is True

        # Add non done upstream
        upstream_run1 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run1])
        assert operation_run.check_upstream_trigger() is False

        # A running upstream
        OperationRunStatus.objects.create(status=OperationStatuses.RUNNING,
                                          operation_run=upstream_run1)
        assert operation_run.check_upstream_trigger() is False

        # A failed upstream
        OperationRunStatus.objects.create(status=OperationStatuses.FAILED,
                                          operation_run=upstream_run1)
        assert operation_run.check_upstream_trigger() is False

        # Add skipped upstream
        upstream_run2 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run2])
        OperationRunStatus.objects.create(status=OperationStatuses.SKIPPED,
                                          operation_run=upstream_run2)
        assert operation_run.check_upstream_trigger() is False

        # Add succeeded upstream
        upstream_run3 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3])
        OperationRunStatus.objects.create(status=OperationStatuses.SUCCEEDED,
                                          operation_run=upstream_run3)
        assert operation_run.check_upstream_trigger() is True

        # Add many succeeded upstream
        upstream_run4 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3, upstream_run4])
        OperationRunStatus.objects.create(status=OperationStatuses.SUCCEEDED,
                                          operation_run=upstream_run4)
        assert operation_run.check_upstream_trigger() is True

        # Many done upstreams
        operation_run.upstream_runs.set(
            [upstream_run1, upstream_run2, upstream_run3])
        assert operation_run.check_upstream_trigger() is False

    def test_trigger_policy_all_failed(self):
        operation_run = OperationRunFactory()
        operation = operation_run.operation
        operation.trigger_policy = TriggerPolicy.ALL_FAILED
        operation.save()

        # No upstream
        assert operation_run.check_upstream_trigger() is True

        # Add non done upstream
        upstream_run1 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run1])
        assert operation_run.check_upstream_trigger() is False

        # A running upstream
        OperationRunStatus.objects.create(status=OperationStatuses.RUNNING,
                                          operation_run=upstream_run1)
        assert operation_run.check_upstream_trigger() is False

        # A failed upstream
        OperationRunStatus.objects.create(status=OperationStatuses.FAILED,
                                          operation_run=upstream_run1)
        assert operation_run.check_upstream_trigger() is True

        # Add skipped upstream
        upstream_run2 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run2])
        OperationRunStatus.objects.create(status=OperationStatuses.SKIPPED,
                                          operation_run=upstream_run2)
        assert operation_run.check_upstream_trigger() is False

        # Add succeeded upstream
        upstream_run3 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3])
        OperationRunStatus.objects.create(status=OperationStatuses.SUCCEEDED,
                                          operation_run=upstream_run3)
        assert operation_run.check_upstream_trigger() is False

        # Add many failed upstream
        upstream_run4 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run1, upstream_run4])
        OperationRunStatus.objects.create(status=OperationStatuses.FAILED,
                                          operation_run=upstream_run4)
        assert operation_run.check_upstream_trigger() is True

        # Many done upstreams
        operation_run.upstream_runs.set(
            [upstream_run1, upstream_run2, upstream_run3])
        assert operation_run.check_upstream_trigger() is False

    def test_is_upstream_done(self):
        operation_run = OperationRunFactory()

        # No upstream
        assert operation_run.is_upstream_done is True

        # Add non done upstream
        upstream_run1 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run1])
        assert operation_run.is_upstream_done is False

        # A running upstream
        OperationRunStatus.objects.create(status=OperationStatuses.RUNNING,
                                          operation_run=upstream_run1)
        assert operation_run.is_upstream_done is False

        # A failed upstream
        OperationRunStatus.objects.create(status=OperationStatuses.FAILED,
                                          operation_run=upstream_run1)
        assert operation_run.is_upstream_done is True

        # Add skipped upstream
        upstream_run2 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run2])
        OperationRunStatus.objects.create(status=OperationStatuses.SKIPPED,
                                          operation_run=upstream_run2)
        assert operation_run.is_upstream_done is True

        # Add succeeded upstream
        upstream_run3 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3])
        OperationRunStatus.objects.create(status=OperationStatuses.SUCCEEDED,
                                          operation_run=upstream_run3)
        assert operation_run.is_upstream_done is True

        # Many done upstreams
        operation_run.upstream_runs.set(
            [upstream_run1, upstream_run2, upstream_run3])
        assert operation_run.is_upstream_done is True

        # Add another upstream
        upstream_run4 = OperationRunFactory()
        operation_run.upstream_runs.add(upstream_run4)
        assert operation_run.is_upstream_done is False
