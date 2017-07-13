# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import os

from celery import Celery, Task

from django.conf import settings

_logger = logging.getLogger("polyaxon.tasks")


class PolyaxonTask(Task):
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
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

app = Celery('api')

app.Task = PolyaxonTask  # Custom base class for logging

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
