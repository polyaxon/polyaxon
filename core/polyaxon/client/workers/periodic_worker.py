#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy

from time import sleep, time

from polyaxon import settings
from polyaxon.client.workers.queue_worker import QueueWorker
from polyaxon.logger import logger


class PeriodicWorker(QueueWorker):
    NAME = "polyaxon.PeriodicWorker"

    def __init__(
        self,
        callback,
        worker_interval=None,
        worker_timeout=None,
        queue_size=None,
        kwargs=None,
    ):
        super().__init__(timeout=worker_timeout, queue_size=queue_size)
        self._interval = (
            worker_interval
            if worker_interval is not None
            else settings.CLIENT_CONFIG.interval
        )
        self._callback = callback
        self._kwargs = kwargs
        self._health_urls = []
        self._last_health_check = time()

    def queue_health(self, url):  # pylint:disable=arguments-differ
        self.is_running()
        if url not in self._health_urls:
            self._health_urls.append(url)

    def unqueue_health(self, url):
        if url in self._health_urls:
            self._health_urls.remove(url)

    def queue(self, url, **kwargs):  # pylint:disable=arguments-differ
        self.is_running()
        self._queue.put_nowait({url: kwargs})

    def _call(self, url, queue_kwargs):
        try:
            kwargs = copy.copy(self._kwargs)
            kwargs.update(queue_kwargs)
            self._callback(url=url, **kwargs)
        except Exception:
            logger.error("Failed processing job", exc_info=True)

    def _extend_url_kwargs(self, url_kwargs, kwargs):
        for k, v in kwargs.items():
            if v:
                if k in url_kwargs:
                    url_kwargs[k].append(v)
                else:
                    url_kwargs[k] = [v]

        return url_kwargs

    def _extend_queue_kwargs(self, queue_kwargs, kwargs, messages):
        for url, v in kwargs.items():
            if v:
                if url in queue_kwargs:
                    queue_kwargs[url] = self._extend_url_kwargs(queue_kwargs[url], v)
                    messages[url] += 1
                else:
                    queue_kwargs[url] = self._extend_url_kwargs({}, v)
                    messages[url] = 0
            else:
                queue_kwargs[url] = {}
                messages[url] = 1

        return queue_kwargs, messages

    def health_checks(self):
        if time() - self._last_health_check > settings.HEALTH_CHECK_INTERVAL:
            self._last_health_check = time()
            for url in self._health_urls:
                self._call(url, {})

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
                        queue_kwargs, record, messages
                    )
                finally:
                    self._queue.task_done()

                for url in messages.keys():
                    if messages[url] >= settings.CLIENT_CONFIG.interval:
                        self._call(url, queue_kwargs[url])
                        messages[url] = 0
                        queue_kwargs[url] = {}

            if queue_kwargs:
                for url in queue_kwargs.keys():
                    self._call(url, queue_kwargs[url])

            self.health_checks()
            sleep(self._interval)
