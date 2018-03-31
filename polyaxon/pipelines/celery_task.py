from billiard.exceptions import SoftTimeLimitExceeded
from polyaxon_schemas.utils import to_list

from pipelines.models import OperationRun
from polyaxon.celery_api import CeleryTask


class OperationRunTaskException(Exception):
    pass


class OperationTask(CeleryTask):
    """Base operation celery task with basic logging."""
    _operation_run = None

    def __call__(self, *args, **kwargs):
        try:
            self._operation_run = OperationRun.objects.get(id=kwargs['operation_run_id'])
        except (KeyError, OperationRun.DoesNotExist):
            raise OperationRunTaskException
        self._operation_run.on_run()
        self.max_retries = self._operation_run.operation.max_retries
        self.countdown = self._operation_run.operation.get_countdown(self.request.retries)

        super(OperationTask, self).__call__(*args, **kwargs)

    def on_failure(self, exc, task_id, args, kwargs, exc_info):
        """Update query status and send email notification to a user"""
        super(OperationTask, self).on_failure(exc, task_id, args, kwargs, exc_info)
        if isinstance(exc, OperationRunTaskException):
            return
        self._operation_run.on_failure()

    def on_retry(self, exc, task_id, args, kwargs, exc_info):
        super(OperationTask, self).on_retry(exc, task_id, args, kwargs, exc_info)
        self._operation_run.on_retry()

    def on_success(self, retval, task_id, args, kwargs):
        """Send email notification and a file, if requested to do so by a user"""
        super(OperationTask, self).on_success(retval, task_id, args, kwargs)
        self._operation_run.on_success()


class ClassBasedTask(object):
    """A class based task to use for operation tasks."""
    retry_for = None

    @classmethod
    def run(cls, task_bind, *args, **kwargs):
        retry_for = cls.retry_for or []
        retry_for = to_list(retry_for)
        if SoftTimeLimitExceeded not in retry_for:
            retry_for.append(SoftTimeLimitExceeded)
        try:
            return cls._run(task_bind, *args, **kwargs)
        except tuple(retry_for) as exc:
            if task_bind.request.retries < task_bind.max_retries:
                raise task_bind.retry(countdown=task_bind.countdown)
            else:
                raise exc

    @staticmethod
    def _run(task_bind, *args, **kwargs):
        raise NotImplemented
