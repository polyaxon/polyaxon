# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import requests
import time

from flaky import flaky
from tests.test_transports.utils import BaseTestCaseTransport

from polyaxon_client.api_config import ApiConfig
from polyaxon_client.transport.threaded_transport import ThreadedTransportMixin
from polyaxon_client.workers.queue_worker import QueueWorker


class DummyTransport(ThreadedTransportMixin):
    # pylint:disable=protected-access
    def __init__(self, delay=0):
        self.queue = []
        self.delay = delay
        self.config = ApiConfig(is_managed=True, timeout=0.01)
        self._threaded_exceptions = 0
        self._threaded_done = 0

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

    def upload(self, url, **kwargs):
        time.sleep(self.delay)
        self.queue.append(('upload', url))


class ExceptionTransport(ThreadedTransportMixin):
    # pylint:disable=protected-access
    def __init__(self, delay=0):
        self.delay = delay
        self.config = ApiConfig(is_managed=True, timeout=0.01)
        self._threaded_exceptions = 0
        self._threaded_done = 0

    def post(self, **kwargs):
        time.sleep(self.delay)
        raise requests.exceptions.HTTPError('error')

    def patch(self, **kwargs):
        time.sleep(self.delay)
        raise requests.exceptions.HTTPError('error')

    def delete(self, **kwargs):
        time.sleep(self.delay)
        raise requests.exceptions.HTTPError('error')

    def put(self, **kwargs):
        time.sleep(self.delay)
        raise requests.exceptions.HTTPError('error')

    def upload(self, **kwargs):
        time.sleep(self.delay)
        raise requests.exceptions.HTTPError('error')


class TestThreadedTransport(BaseTestCaseTransport):
    # pylint:disable=protected-access
    def setUp(self):
        super(TestThreadedTransport, self).setUp()
        self.transport = DummyTransport()
        self.exception_transport = ExceptionTransport()

    def test_retry_session(self):
        assert hasattr(self.transport, '_retry_session') is False
        assert isinstance(self.transport.retry_session, requests.Session)
        assert isinstance(self.transport._retry_session, requests.Session)

    def test_worker(self):
        assert hasattr(self.transport, '_worker') is False
        assert isinstance(self.transport.worker, QueueWorker)
        assert isinstance(self.transport._worker, QueueWorker)

    def test_async_requests(self):
        assert self.transport.queue == []

        self.transport.async_post(url='url_post')
        time.sleep(0.03)
        assert self.transport.queue == [('post', 'url_post')]
        assert self.transport.threaded_done == 1
        assert self.transport.threaded_exceptions == 0

        self.transport.async_patch(url='url_patch')
        time.sleep(0.03)
        assert self.transport.queue == [('post', 'url_post'), ('patch', 'url_patch')]
        assert self.transport.threaded_done == 2
        assert self.transport.threaded_exceptions == 0

        self.transport.async_put(url='url_put')
        time.sleep(0.03)
        assert self.transport.queue == [('post', 'url_post'),
                                        ('patch', 'url_patch'),
                                        ('put', 'url_put')]
        assert self.transport.threaded_done == 3
        assert self.transport.threaded_exceptions == 0

        self.transport.async_delete(url='url_delete')
        time.sleep(0.03)
        assert self.transport.queue == [('post', 'url_post'),
                                        ('patch', 'url_patch'),
                                        ('put', 'url_put'),
                                        ('delete', 'url_delete')]
        assert self.transport.threaded_done == 4
        assert self.transport.threaded_exceptions == 0

        self.transport.async_upload(url='url_upload', files=['file'], files_size=200)
        time.sleep(0.03)
        assert self.transport.queue == [('post', 'url_post'),
                                        ('patch', 'url_patch'),
                                        ('put', 'url_put'),
                                        ('delete', 'url_delete'),
                                        ('upload', 'url_upload')]
        assert self.transport.threaded_done == 5
        assert self.transport.threaded_exceptions == 0
        assert self.transport.worker.is_alive() is True

    @flaky(max_runs=3)
    def test_async_exceptions(self):
        self.exception_transport.async_post(url='url_post')
        time.sleep(0.03)
        assert self.exception_transport.threaded_done == 1
        assert self.exception_transport.threaded_exceptions == 1

        self.exception_transport.async_patch(url='url_patch')
        time.sleep(0.03)
        assert self.exception_transport.threaded_done == 2
        assert self.exception_transport.threaded_exceptions == 2

        self.exception_transport.async_put(url='url_put')
        time.sleep(0.03)
        assert self.exception_transport.threaded_done == 3
        assert self.exception_transport.threaded_exceptions == 3

        self.exception_transport.async_delete(url='url_delete')
        time.sleep(0.03)
        assert self.exception_transport.threaded_done == 4
        assert self.exception_transport.threaded_exceptions == 4

        self.exception_transport.async_delete(url='url_upload')
        time.sleep(0.03)
        assert self.exception_transport.threaded_done == 5
        assert self.exception_transport.threaded_exceptions == 5

    def test_worker_atexit_handle_queue_before_stopping(self):
        # Transport
        self.transport.config.timeout = 0.5
        self.transport.delay = 0.5
        assert self.transport.queue == []
        self.transport.async_post(url='url_post')
        assert self.transport.queue == []
        time.sleep(0.1)
        assert self.transport.worker.is_alive() is True
        self.transport.worker.atexit()
        assert self.transport.queue == [('post', 'url_post')]
        assert self.transport.threaded_done == 1
        assert self.transport.threaded_exceptions == 0
        assert self.transport._worker.is_alive() is False

        # Exception transport
        self.exception_transport.config.timeout = 0.5
        self.exception_transport.delay = 0.5
        self.exception_transport.async_post(url='url_post')
        assert self.exception_transport.threaded_done == 0
        assert self.exception_transport.threaded_exceptions == 0
        time.sleep(0.1)
        assert self.exception_transport.worker.is_alive() is True
        self.exception_transport.worker.atexit()
        assert self.exception_transport.threaded_done == 1
        assert self.exception_transport.threaded_exceptions == 1
        assert self.exception_transport._worker.is_alive() is False
