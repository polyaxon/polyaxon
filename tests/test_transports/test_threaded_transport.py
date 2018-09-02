# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import time
from unittest import TestCase

import requests

from polyaxon_client.transport.threaded_transport import ThreadedTransportMixin
from polyaxon_client.workers.queue_worker import QueueWorker


class DummyTransport(ThreadedTransportMixin):
    def __init__(self, delay=0):
        self.queue = []
        self.delay = delay

    def post(self, url, **kwargs):
        time.sleep(self.delay)
        self.queue.append(('post', url))

    def patch(self, url, **kwargs):
        time.sleep(self.delay)
        self.queue.append(('patch', url))

    def delete(self, url, **kwargs):
        time.sleep(self.delay)
        self.queue.append(('delete', url))

    def put(self, url, **kwargs):
        time.sleep(self.delay)
        self.queue.append(('put', url))


class TestThreadedTransport(TestCase):
    def setUp(self):
        self.transport = DummyTransport()

    def test_retry_session(self):
        assert hasattr(self.transport, '_retry_session') is False
        assert isinstance(self.transport.retry_session, requests.Session)
        assert isinstance(self.transport._retry_session, requests.Session)

    def test_worker(self):
        assert hasattr(self.transport, '_worker') is False
        assert isinstance(self.transport.worker, QueueWorker)
        assert isinstance(self.transport._worker, QueueWorker)

    def test_async_post(self):
        assert self.transport.queue == []

        self.transport.async_post(url='url_post')
        time.sleep(0.001)
        assert self.transport.queue == [('post', 'url_post')]

        self.transport.async_patch(url='url_patch')
        time.sleep(0.001)
        assert self.transport.queue == [('post', 'url_post'), ('patch', 'url_patch')]

        self.transport.async_put(url='url_put')
        time.sleep(0.001)
        assert self.transport.queue == [('post', 'url_post'),
                                        ('patch', 'url_patch'),
                                        ('put', 'url_put')]

        self.transport.async_delete(url='url_delete')
        time.sleep(0.001)
        assert self.transport.queue == [('post', 'url_post'),
                                        ('patch', 'url_patch'),
                                        ('put', 'url_put'),
                                        ('delete', 'url_delete')]
        assert self.transport.worker.is_alive() is True

    def test_worker_atexit_handle_queue_before_stopping(self):
        self.transport.delay = 0.5
        assert self.transport.queue == []
        self.transport.async_post(url='url_post')
        assert self.transport.queue == []
        time.sleep(0.1)
        assert self.transport.worker.is_alive() is True
        self.transport.worker.atexit()
        assert self.transport.queue == [('post', 'url_post')]
        assert self.transport._worker.is_alive() is False




