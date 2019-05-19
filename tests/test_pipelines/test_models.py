from datetime import timedelta

import pytest

from mock import patch

from django.conf import settings
from django.utils import timezone

from db.models.jobs import JobStatus
from db.models.pipelines import OperationRun, PipelineRunStatus
from factories.factory_pipelines import (
    OperationFactory,
    OperationRunFactory,
    PipelineFactory,
    PipelineRunFactory
)
from lifecycles.operations import OperationStatuses
from lifecycles.pipelines import PipelineLifeCycle, TriggerPolicy
from operations.scheduler import skip_operation_run, start_operation_run, stop_operation_run
from tests.base.case import BaseTest


@pytest.mark.pipelines_mark
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


@pytest.mark.pipelines_mark
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

        operation.queue = 'dummy_queue'
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


@pytest.mark.pipelines_mark
class TestPipelineRunModel(BaseTest):
    DISABLE_EXECUTOR = False
    DISABLE_RUNNER = False

    def test_pipeline_run_creation_sets_created_status(self):
        assert PipelineRunStatus.objects.count() == 0
        # Assert `new_pipeline_run_status` task is also called
        pipeline_run = PipelineRunFactory()
        assert PipelineRunStatus.objects.filter(pipeline_run=pipeline_run).count() == 1
        assert pipeline_run.last_status == PipelineLifeCycle.CREATED

    def test_stopping_pipeline_run_stops_operation_runs(self):
        pipeline_run = PipelineRunFactory()
        for _ in range(2):
            op_run = OperationRunFactory(pipeline_run=pipeline_run)
            assert start_operation_run(op_run) is False
        assert pipeline_run.statuses.count() == 1
        assert pipeline_run.last_status == PipelineLifeCycle.CREATED
        assert JobStatus.objects.filter().count() == 2
        assert set(OperationRun.objects.values_list(
            'status', flat=True)) == {OperationStatuses.CREATED, }
        assert set(JobStatus.objects.values_list(
            'status', flat=True)) == {OperationStatuses.CREATED, }
        # Set pipeline run to stopped
        with patch('scheduler.tasks.jobs.jobs_stop.apply_async') as spawner_mock_stop:
            pipeline_run.on_stop()
        assert pipeline_run.statuses.count() == 2
        assert pipeline_run.last_status == PipelineLifeCycle.STOPPED
        # Operation run are also stopped
        assert JobStatus.objects.all().count() + spawner_mock_stop.call_count == 4

    def test_skipping_pipeline_run_stops_operation_runs(self):
        pipeline_run = PipelineRunFactory()
        for _ in range(2):
            op_run = OperationRunFactory(pipeline_run=pipeline_run)
            assert start_operation_run(op_run) is False
        assert pipeline_run.statuses.count() == 1
        assert pipeline_run.last_status == PipelineLifeCycle.CREATED
        assert JobStatus.objects.filter().count() == 2
        assert set(JobStatus.objects.values_list(
            'status', flat=True)) == {OperationStatuses.CREATED, }
        # Set pipeline run to skipped
        with patch('scheduler.tasks.jobs.jobs_stop.apply_async') as spawner_mock_stop:
            pipeline_run.on_skip()
        assert pipeline_run.statuses.count() == 2
        assert pipeline_run.last_status == PipelineLifeCycle.SKIPPED
        # Operation run are also skipped
        assert JobStatus.objects.filter().count() + spawner_mock_stop.call_count == 6
        assert set(JobStatus.objects.values_list(
            'status', flat=True)) == {OperationStatuses.CREATED,
                                      OperationStatuses.SKIPPED}

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
        operation_run1.downstream_runs.set([operation_runs[1],
                                            operation_runs[2],
                                            operation_runs[3]])

        operation_run2 = OperationRunFactory()
        operation_run2.upstream_runs.set([operation_runs[0], operation_runs[2]])

        assert pipeline_run.dag == (
            {
                operation_runs[0].id: {operation_run2.id, },
                operation_runs[1].id: set(),
                operation_runs[2].id: {operation_runs[0].id,
                                       operation_runs[1].id,
                                       operation_run2.id},
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
        operation_run1.status = OperationStatuses.RUNNING
        operation_run1.save()
        assert pipeline_run.check_concurrency() is True

        # Second operation run
        operation_run2 = OperationRunFactory(pipeline_run=pipeline_run)
        assert pipeline_run.check_concurrency() is True

        # Second operation run with RUNNING status
        operation_run2.status = OperationStatuses.RUNNING
        operation_run2.save()
        assert pipeline_run.check_concurrency() is False


@pytest.mark.pipelines_mark
class TestOperationRunModel(BaseTest):
    DISABLE_EXECUTOR = False

    def test_operation_run_creation_sets_created_status(self):
        assert JobStatus.objects.count() == 0
        # Assert `new_pipeline_run_status` task is also called
        operation_run = OperationRunFactory()
        start_operation_run(operation_run)
        operation_run.refresh_from_db()
        assert JobStatus.objects.count() == 1
        assert operation_run.last_status == OperationStatuses.CREATED
        assert operation_run.entity.last_status == OperationStatuses.CREATED

    def test_scheduling_operation_run_sets_pipeline_run_to_scheduled(self):
        operation_run = OperationRunFactory()
        start_operation_run(operation_run)
        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.CREATED
        pipeline_run = operation_run.pipeline_run
        assert pipeline_run.last_status == PipelineLifeCycle.CREATED
        assert pipeline_run.statuses.count() == 1

        operation_run.set_status(OperationStatuses.SCHEDULED)
        operation_run.refresh_from_db()
        pipeline_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.SCHEDULED
        assert pipeline_run.last_status == PipelineLifeCycle.SCHEDULED
        assert pipeline_run.statuses.count() == 2

    def test_running_operation_run_sets_pipeline_run_to_running(self):
        operation_run = OperationRunFactory()
        start_operation_run(operation_run)
        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.CREATED
        pipeline_run = operation_run.pipeline_run
        assert pipeline_run.last_status == PipelineLifeCycle.CREATED
        assert pipeline_run.statuses.count() == 1

        # Create another operation run for this pipeline_run
        operation_run2 = OperationRunFactory(pipeline_run=pipeline_run)
        start_operation_run(operation_run2)
        operation_run2.refresh_from_db()

        operation_run.set_status(OperationStatuses.SCHEDULED)
        pipeline_run.refresh_from_db()
        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.SCHEDULED
        assert pipeline_run.last_status == PipelineLifeCycle.SCHEDULED
        assert pipeline_run.statuses.count() == 2

        operation_run.set_status(OperationStatuses.RUNNING)
        pipeline_run.refresh_from_db()
        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.RUNNING
        assert pipeline_run.last_status == PipelineLifeCycle.RUNNING
        assert pipeline_run.statuses.count() == 3

        operation_run2.set_status(OperationStatuses.SCHEDULED)
        assert pipeline_run.last_status == PipelineLifeCycle.RUNNING
        assert pipeline_run.statuses.count() == 3

    def test_stopping_all_operation_runs_sets_pipeline_run_to_finished(self):
        operation_run = OperationRunFactory()
        start_operation_run(operation_run)
        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.CREATED
        pipeline_run = operation_run.pipeline_run
        assert pipeline_run.last_status == PipelineLifeCycle.CREATED
        assert pipeline_run.statuses.count() == 1

        # Create another operation run for this pipeline_run
        operation_run2 = OperationRunFactory(pipeline_run=pipeline_run)
        start_operation_run(operation_run2)
        operation_run2.refresh_from_db()
        # Stopping the first operation does not stop the pipeline
        with patch('scheduler.tasks.jobs.jobs_stop.apply_async') as spawner_mock_stop:
            stop_operation_run(operation_run)
        assert spawner_mock_stop.call_count == 1
        # Manual stopping
        operation_run.entity.set_status(OperationStatuses.STOPPED)
        pipeline_run.refresh_from_db()
        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.STOPPED
        assert pipeline_run.last_status == PipelineLifeCycle.CREATED
        assert pipeline_run.statuses.count() == 1

        # Stopping the second operation stops the pipeline
        with patch('scheduler.tasks.jobs.jobs_stop.apply_async') as spawner_mock_stop:
            stop_operation_run(operation_run2)
        assert spawner_mock_stop.call_count == 1
        # Manual stopping
        operation_run2.entity.set_status(OperationStatuses.STOPPED)
        pipeline_run.refresh_from_db()
        assert pipeline_run.last_status == PipelineLifeCycle.DONE
        assert pipeline_run.statuses.count() == 2

    def test_skipping_all_operation_runs_sets_pipeline_run_to_finished(self):
        operation_run = OperationRunFactory()
        start_operation_run(operation_run)
        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.CREATED
        pipeline_run = operation_run.pipeline_run
        assert pipeline_run.last_status == PipelineLifeCycle.CREATED
        assert pipeline_run.statuses.count() == 1

        # Create another operation run for this pipeline_run
        operation_run2 = OperationRunFactory(pipeline_run=pipeline_run)
        start_operation_run(operation_run2)
        operation_run2.refresh_from_db()

        # Stopping the first operation does not stop the pipeline
        with patch('scheduler.tasks.jobs.jobs_stop.apply_async') as spawner_mock_stop:
            skip_operation_run(operation_run)
        assert spawner_mock_stop.call_count == 1
        operation_run.refresh_from_db()
        pipeline_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.SKIPPED
        assert pipeline_run.last_status == PipelineLifeCycle.CREATED
        assert pipeline_run.statuses.count() == 1

        # Stopping the second operation stops the pipeline
        with patch('scheduler.tasks.jobs.jobs_stop.apply_async') as spawner_mock_stop:
            skip_operation_run(operation_run2)
        assert spawner_mock_stop.call_count == 1
        pipeline_run.refresh_from_db()
        assert pipeline_run.last_status == PipelineLifeCycle.DONE
        assert pipeline_run.statuses.count() == 2

    def test_succeeded_operation_runs_sets_pipeline_run_to_finished(self):
        operation_run = OperationRunFactory()
        start_operation_run(operation_run)
        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.CREATED
        pipeline_run = operation_run.pipeline_run
        assert pipeline_run.last_status == PipelineLifeCycle.CREATED
        assert pipeline_run.statuses.count() == 1

        # Stopping the first operation does not stop the pipeline
        operation_run.set_status(OperationStatuses.SCHEDULED)
        operation_run.set_status(OperationStatuses.RUNNING)
        operation_run.on_success()
        operation_run.refresh_from_db()
        pipeline_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.SUCCEEDED
        assert pipeline_run.last_status == PipelineLifeCycle.DONE
        assert pipeline_run.statuses.count() == 4

    def test_failed_operation_runs_sets_pipeline_run_to_finished(self):
        operation_run = OperationRunFactory()
        start_operation_run(operation_run)
        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.CREATED
        pipeline_run = operation_run.pipeline_run
        assert pipeline_run.last_status == PipelineLifeCycle.CREATED
        assert pipeline_run.statuses.count() == 1

        # Stopping the first operation does not stop the pipeline
        operation_run.set_status(OperationStatuses.SCHEDULED)
        operation_run.set_status(OperationStatuses.RUNNING)
        operation_run.on_failure()
        pipeline_run.refresh_from_db()
        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.FAILED
        assert pipeline_run.last_status == PipelineLifeCycle.DONE
        assert pipeline_run.statuses.count() == 4

    def test_failed_upstream_operation_runs_sets_pipeline_run_to_finished(self):
        operation_run = OperationRunFactory()
        start_operation_run(operation_run)
        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.CREATED
        pipeline_run = operation_run.pipeline_run
        assert pipeline_run.last_status == PipelineLifeCycle.CREATED
        assert pipeline_run.statuses.count() == 1

        # Stopping the first operation does not stop the pipeline
        operation_run.on_upstream_failed()
        operation_run.refresh_from_db()
        pipeline_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.UPSTREAM_FAILED
        assert pipeline_run.last_status == PipelineLifeCycle.DONE
        assert pipeline_run.statuses.count() == 2

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
        operation_run1.status = OperationStatuses.RUNNING
        operation_run1.save()

        assert operation_run.check_concurrency() is True

        # Second operation run
        operation_run2 = OperationRunFactory(operation=operation)
        assert operation_run.check_concurrency() is True

        # Second operation run with RUNNING status
        operation_run2.status = OperationStatuses.RUNNING
        operation_run2.save()
        assert operation_run.check_concurrency() is False

    def test_trigger_policy_one_done(self):
        operation_run = OperationRunFactory()
        start_operation_run(operation_run)
        operation_run.refresh_from_db()
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
        upstream_run1.status = OperationStatuses.RUNNING
        upstream_run1.save()
        assert operation_run.check_upstream_trigger() is False

        # A failed upstream
        upstream_run1.status = OperationStatuses.FAILED
        upstream_run1.save()
        assert operation_run.check_upstream_trigger() is True

        # Add skipped upstream
        upstream_run2 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run2])
        upstream_run2.status = OperationStatuses.SKIPPED
        upstream_run2.save()
        assert operation_run.check_upstream_trigger() is True

        # Add succeeded upstream
        upstream_run3 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3])
        upstream_run3.status = OperationStatuses.SUCCEEDED
        upstream_run3.save()
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
        upstream_run1.status = OperationStatuses.RUNNING
        upstream_run1.save()
        assert operation_run.check_upstream_trigger() is False

        # A failed upstream
        upstream_run1.status = OperationStatuses.FAILED
        upstream_run1.save()
        assert operation_run.check_upstream_trigger() is False

        # Add skipped upstream
        upstream_run2 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run2])
        upstream_run2.status = OperationStatuses.SKIPPED
        upstream_run2.save()
        assert operation_run.check_upstream_trigger() is False

        # Add succeeded upstream
        upstream_run3 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3])
        upstream_run3.status = OperationStatuses.SUCCEEDED
        upstream_run3.save()
        assert operation_run.check_upstream_trigger() is True

        # Add another upstream still True
        upstream_run4 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run1,
                                         upstream_run2,
                                         upstream_run3,
                                         upstream_run4])
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
        upstream_run1.status = OperationStatuses.RUNNING
        upstream_run1.save()
        assert operation_run.check_upstream_trigger() is False

        # A failed upstream
        upstream_run1.status = OperationStatuses.FAILED
        upstream_run1.save()
        assert operation_run.check_upstream_trigger() is True

        # Add skipped upstream
        upstream_run2 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run2])
        upstream_run2.status = OperationStatuses.SKIPPED
        upstream_run2.save()
        assert operation_run.check_upstream_trigger() is False

        # Add succeeded upstream
        upstream_run3 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3])
        upstream_run3.status = OperationStatuses.SUCCEEDED
        upstream_run3.save()
        assert operation_run.check_upstream_trigger() is False

        # Add another upstream still True
        upstream_run4 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run1,
                                         upstream_run2,
                                         upstream_run3,
                                         upstream_run4])
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
        upstream_run1.status = OperationStatuses.RUNNING
        upstream_run1.save()
        assert operation_run.check_upstream_trigger() is False

        # A failed upstream
        upstream_run1.status = OperationStatuses.FAILED
        upstream_run1.save()
        assert operation_run.check_upstream_trigger() is True

        # Add skipped upstream
        upstream_run2 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run2])
        upstream_run2.status = OperationStatuses.SKIPPED
        upstream_run2.save()
        assert operation_run.check_upstream_trigger() is True

        # Add succeeded upstream
        upstream_run3 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3])
        upstream_run3.status = OperationStatuses.SUCCEEDED
        upstream_run3.save()
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
        upstream_run1.status = OperationStatuses.RUNNING
        upstream_run1.save()
        assert operation_run.check_upstream_trigger() is False

        # A failed upstream
        upstream_run1.status = OperationStatuses.FAILED
        upstream_run1.save()
        assert operation_run.check_upstream_trigger() is False

        # Add skipped upstream
        upstream_run2 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run2])
        upstream_run2.status = OperationStatuses.SKIPPED
        upstream_run2.save()
        assert operation_run.check_upstream_trigger() is False

        # Add succeeded upstream
        upstream_run3 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3])
        upstream_run3.status = OperationStatuses.SUCCEEDED
        upstream_run3.save()
        assert operation_run.check_upstream_trigger() is True

        # Add many succeeded upstream
        upstream_run4 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3, upstream_run4])
        upstream_run4.status = OperationStatuses.SUCCEEDED
        upstream_run4.save()
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
        upstream_run1.status = OperationStatuses.RUNNING
        upstream_run1.save()
        assert operation_run.check_upstream_trigger() is False

        # A failed upstream
        upstream_run1.status = OperationStatuses.FAILED
        upstream_run1.save()
        assert operation_run.check_upstream_trigger() is True

        # Add skipped upstream
        upstream_run2 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run2])
        upstream_run2.status = OperationStatuses.SKIPPED
        upstream_run2.save()
        assert operation_run.check_upstream_trigger() is False

        # Add succeeded upstream
        upstream_run3 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3])
        upstream_run3.status = OperationStatuses.SUCCEEDED
        upstream_run3.save()
        assert operation_run.check_upstream_trigger() is False

        # Add many failed upstream
        upstream_run4 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run1, upstream_run4])
        upstream_run4.status = OperationStatuses.FAILED
        upstream_run4.save()
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
        upstream_run1.status = OperationStatuses.RUNNING
        upstream_run1.save()
        assert operation_run.is_upstream_done is False

        # A failed upstream
        upstream_run1.status = OperationStatuses.FAILED
        upstream_run1.save()
        assert operation_run.is_upstream_done is True

        # Add skipped upstream
        upstream_run2 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run2])
        upstream_run2.status = OperationStatuses.SKIPPED
        upstream_run2.save()
        assert operation_run.is_upstream_done is True

        # Add succeeded upstream
        upstream_run3 = OperationRunFactory()
        operation_run.upstream_runs.set([upstream_run3])
        upstream_run3.status = OperationStatuses.SUCCEEDED
        upstream_run3.save()
        assert operation_run.is_upstream_done is True

        # Many done upstreams
        operation_run.upstream_runs.set(
            [upstream_run1, upstream_run2, upstream_run3])
        assert operation_run.is_upstream_done is True

        # Add another upstream
        upstream_run4 = OperationRunFactory()
        operation_run.upstream_runs.add(upstream_run4)
        assert operation_run.is_upstream_done is False

    def test_schedule_start_with_operation_run_already_scheduled_operation_run(self):
        operation_run = OperationRunFactory()
        operation_run.status = OperationStatuses.FAILED
        operation_run.save()
        assert start_operation_run(operation_run) is False

        operation_run = OperationRunFactory()
        operation_run.status = OperationStatuses.SCHEDULED
        operation_run.save()
        assert start_operation_run(operation_run) is False

    def test_schedule_start_with_failed_upstream(self):
        operation_run = OperationRunFactory()
        operation_run.operation.trigger_policy = TriggerPolicy.ALL_SUCCEEDED
        operation_run.operation.save()

        # Add a failed upstream
        upstream_run1 = OperationRunFactory()
        assert start_operation_run(upstream_run1) is False
        upstream_run1.refresh_from_db()
        operation_run.upstream_runs.set([upstream_run1])
        with patch('pipelines.tasks.pipelines_start_operation.apply_async') as mock_fct:
            upstream_run1.set_status(OperationStatuses.FAILED)

        assert mock_fct.call_count == 1

        assert start_operation_run(operation_run) is False

        # Check also that the task is marked as UPSTREAM_FAILED
        # Since this operation cannot be started anymore
        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.UPSTREAM_FAILED

    def test_schedule_start_works_when_conditions_are_met_manual(self):
        operation_run = OperationRunFactory()
        operation_run.operation.trigger_policy = TriggerPolicy.ONE_DONE
        operation_run.operation.save()
        pipeline_run = operation_run.pipeline_run

        # Add a failed upstream
        upstream_run1 = OperationRunFactory(pipeline_run=pipeline_run)
        assert start_operation_run(upstream_run1) is False
        upstream_run1.refresh_from_db()
        operation_run.upstream_runs.set([upstream_run1])
        with patch('pipelines.tasks.pipelines_start_operation.apply_async') as mock_fct:
            upstream_run1.set_status(OperationStatuses.FAILED)

        assert mock_fct.call_count == 1
        operation_run.refresh_from_db()
        assert operation_run.last_status is None

        assert start_operation_run(operation_run) is False
        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.CREATED

    def test_schedule_start_works_when_conditions_are_met_auto(self):
        operation_run = OperationRunFactory()
        operation_run.operation.trigger_policy = TriggerPolicy.ONE_DONE
        operation_run.operation.save()
        pipeline_run = operation_run.pipeline_run

        # Add a failed upstream
        upstream_run1 = OperationRunFactory(pipeline_run=pipeline_run)
        assert start_operation_run(upstream_run1) is False
        upstream_run1.refresh_from_db()
        operation_run.upstream_runs.set([upstream_run1])
        upstream_run1.set_status(OperationStatuses.FAILED)

        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.CREATED

    def test_schedule_start_works_with_pipeline_concurrency(self):
        operation_run = OperationRunFactory()
        operation_run.operation.trigger_policy = TriggerPolicy.ONE_DONE
        operation_run.operation.save()
        pipeline_run = operation_run.pipeline_run
        # Set pipeline concurrency to 1
        pipeline_run.pipeline.concurrency = 1
        pipeline_run.pipeline.save()

        # Add a failed upstream
        upstream_run1 = OperationRunFactory(pipeline_run=pipeline_run)
        upstream_run2 = OperationRunFactory(pipeline_run=pipeline_run)
        assert start_operation_run(upstream_run1) is False
        assert start_operation_run(upstream_run2) is True
        upstream_run1.refresh_from_db()
        upstream_run2.refresh_from_db()
        operation_run.upstream_runs.set([upstream_run1, upstream_run2])
        with patch('pipelines.tasks.pipelines_start_operation.apply_async') as mock_fct:
            upstream_run1.set_status(OperationStatuses.FAILED)

        assert mock_fct.call_count == 1
        operation_run.refresh_from_db()
        assert operation_run.last_status is None
        upstream_run2.refresh_from_db()
        assert upstream_run2.last_status is None  # Should be started but e mocked the process

        with patch('pipelines.tasks.pipelines_start_operation.apply_async') as mock_fct:
            assert start_operation_run(upstream_run2) is False
            upstream_run2.refresh_from_db()
            upstream_run2.set_status(OperationStatuses.RUNNING)

        assert mock_fct.call_count == 0

        assert start_operation_run(operation_run) is True

        assert operation_run.last_status is None

        upstream_run2.set_status(OperationStatuses.SUCCEEDED)

        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.CREATED

    def test_schedule_start_works_with_operation_concurrency(self):
        operation_run = OperationRunFactory()
        operation_run.operation.trigger_policy = TriggerPolicy.ONE_DONE
        operation_run.operation.save()
        pipeline_run = operation_run.pipeline_run
        # Set operation concurrency to 1
        operation_run.operation.concurrency = 1
        operation_run.operation.save()

        # Add a failed upstream
        upstream_run1 = OperationRunFactory(pipeline_run=pipeline_run)
        upstream_run2 = OperationRunFactory(pipeline_run=pipeline_run)
        assert start_operation_run(upstream_run1) is False
        assert start_operation_run(upstream_run2) is False
        upstream_run1.refresh_from_db()
        upstream_run2.refresh_from_db()
        operation_run.upstream_runs.set([upstream_run1, upstream_run2])
        with patch('pipelines.tasks.pipelines_start_operation.apply_async') as mock_fct:
            upstream_run1.set_status(OperationStatuses.FAILED)
            upstream_run2.set_status(OperationStatuses.RUNNING)

        assert mock_fct.call_count == 1
        operation_run.refresh_from_db()
        assert operation_run.last_status is None
        assert start_operation_run(operation_run) is False
        operation_run.refresh_from_db()
        assert operation_run.last_status == OperationStatuses.CREATED

        # Add another operation run for this operation with scheduled
        new_operation_run = OperationRunFactory(operation=operation_run.operation)
        new_operation_run.upstream_runs.set([upstream_run1, upstream_run2])
        assert new_operation_run.status is None

        # Check if we can start another instance
        new_operation_run.refresh_from_db()
        assert start_operation_run(new_operation_run) is True
        new_operation_run.refresh_from_db()
        assert new_operation_run.last_status is None
