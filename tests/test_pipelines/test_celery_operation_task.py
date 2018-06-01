import pytest

from constants.pipelines import OperationStatuses, PipelineStatuses
from factories.factory_pipelines import OperationRunFactory
from pipelines.celery_task import ClassBasedTask, OperationTask
from polyaxon.celery_api import app as celery_app
from tests.utils import BaseTest


@pytest.mark.pipelines_mark
class TestOperationTask(BaseTest):
    def setUp(self):

        self.operation_run = OperationRunFactory()
        self.pipeline_run = self.operation_run.pipeline_run
        # Manually set status to scheduled
        self.operation_run.on_scheduled()
        return super().setUp()

    def test_task_without_operation_run_raises(self):
        @celery_app.task(base=OperationTask, shared=False)
        def dummy_task():
            return

        with self.assertRaises(TypeError):
            dummy_task.apply_async()

    def test_task_with_operation_run_succeeds(self):
        @celery_app.task(base=OperationTask, shared=False)
        def dummy_task(operation_run_id):
            return

        kwargs = {'operation_run_id': self.operation_run.id}
        dummy_task.apply_async(kwargs=kwargs)
        self.operation_run.refresh_from_db()
        assert self.operation_run.succeeded is True
        assert set(self.operation_run.statuses.values_list('status', flat=True)) == {
            OperationStatuses.CREATED,
            OperationStatuses.SCHEDULED,
            OperationStatuses.RUNNING,
            OperationStatuses.SUCCEEDED,
        }
        self.pipeline_run.refresh_from_db()
        assert self.operation_run.pipeline_run.last_status == PipelineStatuses.FINISHED
        assert set(self.operation_run.pipeline_run.statuses.values_list('status', flat=True)) == {
            PipelineStatuses.CREATED,
            PipelineStatuses.SCHEDULED,
            PipelineStatuses.RUNNING,
            PipelineStatuses.FINISHED,
        }

    def test_task_with_error_fails(self):
        @celery_app.task(base=OperationTask, shared=False)
        def raising_task(operation_run_id):
            raise KeyError

        kwargs = {'operation_run_id': self.operation_run.id}
        raising_task.apply_async(kwargs=kwargs)
        self.operation_run.refresh_from_db()
        assert self.operation_run.failed is True
        assert set(self.operation_run.statuses.values_list('status', flat=True)) == {
            OperationStatuses.CREATED,
            OperationStatuses.SCHEDULED,
            OperationStatuses.RUNNING,
            OperationStatuses.FAILED,
        }
        self.pipeline_run.refresh_from_db()
        assert self.operation_run.pipeline_run.last_status == PipelineStatuses.FINISHED
        assert set(self.operation_run.pipeline_run.statuses.values_list('status', flat=True)) == {
            PipelineStatuses.CREATED,
            PipelineStatuses.SCHEDULED,
            PipelineStatuses.RUNNING,
            PipelineStatuses.FINISHED,
        }

    def test_task_retries_for_specified_exception(self):
        class RetryTask(ClassBasedTask):
            retry_for = (KeyError, )

            @staticmethod
            def _run(task_bind, *args, **kwargs):
                raise KeyError

        @celery_app.task(base=OperationTask, bind=True, shared=False)
        def retry_task(task_bind, operation_run_id):
            assert task_bind.max_retries == 2
            assert task_bind.countdown == 0
            RetryTask.run(task_bind=task_bind, operation_run_id=operation_run_id)

        # Add retries and count to the operation
        self.operation_run.operation.max_retries = 2
        self.operation_run.operation.retry_delay = 0
        self.operation_run.operation.save()

        kwargs = {'operation_run_id': self.operation_run.id}
        retry_task.apply_async(kwargs=kwargs)
        self.operation_run.refresh_from_db()
        assert self.operation_run.last_status == OperationStatuses.RETRYING
        assert set(self.operation_run.statuses.values_list('status', flat=True)) == {
            OperationStatuses.CREATED,
            OperationStatuses.SCHEDULED,
            OperationStatuses.RUNNING,
            OperationStatuses.RETRYING,
        }
        self.pipeline_run.refresh_from_db()
        assert self.operation_run.pipeline_run.last_status == PipelineStatuses.RUNNING
        assert set(self.operation_run.pipeline_run.statuses.values_list('status', flat=True)) == {
            PipelineStatuses.CREATED,
            PipelineStatuses.SCHEDULED,
            PipelineStatuses.RUNNING,
        }
