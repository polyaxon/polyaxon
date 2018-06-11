import logging
import os

from celery import Celery, Task, states

from django.apps import apps

_logger = logging.getLogger("polyaxon.tasks")


STATES = states


class CeleryTask(Task):
    """Base custom celery task with basic logging."""
    abstract = True

    def on_success(self, retval, task_id, args, kwargs):
        _logger.info("Celery task succeeded", extra={'task name': self.name})

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        extra = {
            'task name': self.name,
            'task id': task_id,
            'task args': args,
            'task kwargs': kwargs,
        }
        _logger.error("Celery Task Failed", exc_info=einfo, extra=extra)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        _logger.info("Celery task retry", extra={'task name': self.name})


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'polyaxon.settings')

app = Celery('polyaxon')

app.Task = CeleryTask  # Custom base class for logging

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
