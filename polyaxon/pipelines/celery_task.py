from pipelines.models import Operation
from polyaxon.celery_api import CeleryTask


class OperationTask(CeleryTask):
    """Base operation celery task with basic logging."""
    _operation = None

    def run(self, *args, **kwargs):
        self._operation = Operation.objects.get(id=kwargs['query_id'])
        super(OperationTask, self).run(*args, **kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Update query status and send email notification to a user"""
        super(OperationTask, self).on_failure(exc, task_id, args, kwargs, einfo)
        self._operation.on_failure()

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        super(OperationTask, self).on_retry(exc, task_id, args, kwargs, einfo)
        self._operation.on_retry()

    def on_success(self, retval, task_id, args, kwargs):
        """Send email notification and a file, if requested to do so by a user"""
        super(OperationTask, self).on_success(retval, task_id, args, kwargs)
        self._operation.on_success()
