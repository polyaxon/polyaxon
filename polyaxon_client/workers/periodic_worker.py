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

    def queue(self, url, **kwargs):  # pylint:disable=arguments-differ
        self.is_running()
        self._queue.put_nowait({url: kwargs})

    def _call(self, url, queue_kwargs):
        try:
            kwargs = copy.copy(self._kwargs)
            kwargs.update(queue_kwargs)
            self._callback(url=url, **kwargs)
        except Exception:
            logger.error('Failed processing job', exc_info=True)

    def _extend_url_kwargs(self, url_kwargs, kwargs):
        for k, v in six.iteritems(kwargs):
            if v:
                if k in url_kwargs:
                    url_kwargs[k].append(v)
                else:
                    url_kwargs[k] = [v]

        return url_kwargs

    def _extend_queue_kwargs(self, queue_kwargs, kwargs, messages):
        for url, v in six.iteritems(kwargs):
            if v:
                if url in queue_kwargs:
                    queue_kwargs[url] = self._extend_url_kwargs(queue_kwargs[url], v)
                    messages[url] += 1
                else:
                    queue_kwargs[url] = self._extend_url_kwargs({}, v)
                    messages[url] = 0

        return queue_kwargs, messages

    def _target(self):
        while True:
            queue_kwargs = {}
            messages = {}
            while self._queue.qsize() > 0:
                record = self._queue.get()
                try:
                    if record is self.END_EVENT:
                        break
                    queue_kwargs, messages = self._extend_queue_kwargs(
                        queue_kwargs, record, messages)
                finally:
                    self._queue.task_done()

                for url in six.iterkeys(messages):
                    if messages[url] >= settings.QUEUE_CALL:
                        self._call(url, queue_kwargs[url])
                        messages[url] = 0
                        queue_kwargs[url] = {}

            if queue_kwargs:
                for url in six.iterkeys(queue_kwargs):
                    self._call(url, queue_kwargs[url])
            sleep(self._interval)
