# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy
import six

from time import sleep

from polyaxon_client import settings
from polyaxon_client.logger import logger
from polyaxon_client.workers.queue_worker import QueueWorker


class PeriodicWorker(QueueWorker):
    NAME = 'polyaxon.PeriodicWorker'

    def __init__(self,
                 callback,
                 worker_interval=None,
                 worker_timeout=None,
                 queue_size=None,
                 kwargs=None):
        super(PeriodicWorker, self).__init__(timeout=worker_timeout, queue_size=queue_size)
        self._interval = worker_interval if worker_interval is not None else settings.INTERVAL
        self._callback = callback
        self._kwargs = kwargs

    def queue(self, **kwargs):  # pylint:disable=arguments-differ
        self.is_running()
        self._queue.put_nowait(kwargs)

    def _call(self, queue_kwargs):
        try:
            kwargs = copy.copy(self._kwargs)
            kwargs.update(queue_kwargs)
            self._callback(**kwargs)
        except Exception:
            logger.error('Failed processing job', exc_info=True)

    def _extend_queue_kwargs(self, queue_kwargs, kwargs):
        for k, v in six.iteritems(kwargs):
            if v:
                if k in queue_kwargs:
                    queue_kwargs[k].append(v)
                else:
                    queue_kwargs[k] = [v]

        return queue_kwargs

    def _target(self):
        while True:
            queue_kwargs = {}
            message = 0
            while self._queue.qsize() > 0:
                record = self._queue.get()
                try:
                    if record is self.END_EVENT:
                        break
                    queue_kwargs = self._extend_queue_kwargs(queue_kwargs, record)
                    message += 1
                finally:
                    self._queue.task_done()

                if queue_kwargs and message >= settings.QUEUE_CALL:
                    self._call(queue_kwargs)
                    message = 0
                    queue_kwargs = {}

            if queue_kwargs:
                self._call(queue_kwargs)
            sleep(self._interval)
