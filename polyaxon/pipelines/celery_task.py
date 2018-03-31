from pipelines.models import OperationRun
from polyaxon.celery_api import CeleryTask


class OperationTask(CeleryTask):
    """Base operation celery task with basic logging."""
    _operation = None

    def __call__(self, *args, **kwargs):
        self._operation_run = OperationRun.objects.get(id=kwargs['operation_run_id'])
        self._operation_run.on_run()
        self.max_retries = self._operation_run.operation.max_retries
        self.countdown = self._operation_run.operation.get_countdown(self.request.retries)

        super(OperationTask, self).__call__(*args, **kwargs)

    def on_failure(self, exc, task_id, args, kwargs, exc_info):
        """Update query status and send email notification to a user"""
        super(OperationTask, self).on_failure(exc, task_id, args, kwargs, exc_info)
        self._operation_run.on_failure()

    def on_retry(self, exc, task_id, args, kwargs, exc_info):
        super(OperationTask, self).on_retry(exc, task_id, args, kwargs, exc_info)
        self._operation_run.on_retry()

    def on_success(self, retval, task_id, args, kwargs):
        """Send email notification and a file, if requested to do so by a user"""
        super(OperationTask, self).on_success(retval, task_id, args, kwargs)
        self._operation_run.on_success()
