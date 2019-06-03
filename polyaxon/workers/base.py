import logging

from celery import Task

_logger = logging.getLogger("polyaxon.tasks")


class PolyaxonTask(Task):
    """Base custom celery task with basic logging."""
    abstract = True

    def on_success(self, retval, task_id, args, kwargs):
        _logger.info("Async task succeeded", extra={'task name': self.name})

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        extra = {
            'task name': self.name,
            'task id': task_id,
            'task args': args,
            'task kwargs': kwargs,
        }
        _logger.error("Async Task Failed", exc_info=einfo, extra=extra)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        _logger.info("Async task retry", extra={'task name': self.name})
