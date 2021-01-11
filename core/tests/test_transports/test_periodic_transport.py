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

# # coding: utf-8
#
#
# import requests
# import time
#
# from polyaxon import settings
# from tests.test_transports.utils import BaseTestCaseTransport
#
# from polyaxon.client.transport.periodic_transport import PeriodicHttpTransportMixin
# from polyaxon.client.workers.periodic_worker import PeriodicWorker
#
#
# class DummyTransport(PeriodicHttpTransportMixin):
#     # pylint:disable=protected-access
#     def __init__(self, delay=0):
#         self.queue = []
#         self.delay = delay
#         self._periodic_http_exceptions = 0
#         self._periodic_http_done = 0
#
#     def post(self, url, **kwargs):
#         time.sleep(self.delay)
#         self.queue.append(("post", url, kwargs))
#
#
# class ExceptionTransport(PeriodicHttpTransportMixin):
#     # pylint:disable=protected-access
#     def __init__(self, delay=0):
#         self.delay = delay
#         self._periodic_http_exceptions = 0
#         self._periodic_http_done = 0
#
#     def post(self, **kwargs):
#         time.sleep(self.delay)
#         raise requests.exceptions.HTTPError("error")
#
#
# class TestPeriodicTransport(BaseTestCaseTransport):
#     # pylint:disable=protected-access
#     def setUp(self):
#         super().setUp()
#         self.transport = DummyTransport()
#         self.exception_transport = ExceptionTransport()
#         settings.CLIENT_CONFIG.timeout = 0.01
#         settings.CLIENT_CONFIG.interval = 0
#
#     def test_retry_session(self):
#         assert hasattr(self.transport, "_retry_session") is False
#         assert isinstance(self.transport.retry_session, requests.Session)
#         assert isinstance(self.transport._retry_session, requests.Session)
#
#     def test_worker(self):
#         assert hasattr(self.transport, "_periodic_http_worker") is False
#         self.assertEqual(self.transport.periodic_http_worker, None)
#         worker = self.transport.get_periodic_http_worker(request=self.transport.post)
#         assert isinstance(self.transport.periodic_http_worker, PeriodicWorker)
#         assert isinstance(self.transport._periodic_http_worker, PeriodicWorker)
#         assert isinstance(worker, PeriodicWorker)
#
#     def test_periodic_requests_with_data(self):
#         assert self.transport.queue == []
#
#         self.transport.periodic_post(url="url_post", data={"d1": "v1"})
#         time.sleep(0.03)
#         queue = self.transport.queue
#         assert len(queue) == 1
#         assert queue[0][0] == "post"
#         assert queue[0][1] == "url_post"
#         assert queue[0][2]["data"] == [{"d1": "v1"}]
#         assert self.transport.periodic_http_done == 1
#         assert self.transport.periodic_http_exceptions == 0
#         assert self.transport.get_periodic_http_worker().is_alive() is True
#
#         self.transport.periodic_post(url="url_post", data={"d1": "v1"})
#         self.transport.periodic_post(url="url_post", data={"d2": "v2"})
#         time.sleep(0.03)
#         queue = self.transport.queue
#         assert len(queue) == 2
#         assert queue[1][0] == "post"
#         assert queue[1][1] == "url_post"
#         assert queue[1][2]["data"] == [{"d1": "v1"}, {"d2": "v2"}]
#         assert self.transport.periodic_http_done == 2
#         assert self.transport.periodic_http_exceptions == 0
#         assert self.transport.get_periodic_http_worker().is_alive() is True
#
#     def test_periodic_requests_with_json_data(self):
#         assert self.transport.queue == []
#
#         self.transport.periodic_post(url="url_post", json_data={"d1": "v1"})
#         time.sleep(0.03)
#         queue = self.transport.queue
#         assert len(queue) == 1
#         assert queue[0][0] == "post"
#         assert queue[0][1] == "url_post"
#         assert queue[0][2]["json_data"] == [{"d1": "v1"}]
#         assert self.transport.periodic_http_done == 1
#         assert self.transport.periodic_http_exceptions == 0
#         assert self.transport.get_periodic_http_worker().is_alive() is True
#
#         self.transport.periodic_post(url="url_post", json_data={"d1": "v1"})
#         self.transport.periodic_post(url="url_post", json_data={"d2": "v2"})
#         time.sleep(0.03)
#         queue = self.transport.queue
#         assert len(queue) == 2
#         assert queue[1][0] == "post"
#         assert queue[1][1] == "url_post"
#         assert queue[1][2]["json_data"] == [{"d1": "v1"}, {"d2": "v2"}]
#         assert self.transport.periodic_http_done == 2
#         assert self.transport.periodic_http_exceptions == 0
#         assert self.transport.get_periodic_http_worker().is_alive() is True
#
#     def test_periodic_requests_with_different_urls(self):
#         self.transport.periodic_post(url="url_post1", json_data={"d11": "v11"})
#         self.transport.periodic_post(url="url_post1", json_data={"d12": "v12"})
#         time.sleep(0.0001)
#         self.transport.periodic_post(url="url_post2", data={"d21": "v21"})
#         self.transport.periodic_post(url="url_post2", data={"d22": "v22"})
#         time.sleep(0.05)
#         queue = self.transport.queue
#         assert len(queue) == 2
#         assert queue[0][0] == "post"
#         assert queue[1][0] == "post"
#         assert queue[0][1] == "url_post1"
#         assert queue[1][1] == "url_post2"
#         assert queue[0][2]["json_data"] == [{"d11": "v11"}, {"d12": "v12"}]
#         assert queue[1][2]["data"] == [{"d21": "v21"}, {"d22": "v22"}]
#         assert self.transport.periodic_http_done == 2
#         assert self.transport.periodic_http_exceptions == 0
#         assert self.transport.periodic_http_worker.is_alive() is True
#
#     def test_async_exceptions(self):
#         self.exception_transport.periodic_post(url="url_post", data={"d1": "v1"})
#         time.sleep(0.03)
#         assert self.exception_transport.periodic_http_done == 1
#         assert self.exception_transport.periodic_http_exceptions == 1
#
#     def test_worker_atexit_handle_queue_before_stopping(self):
#         # Transport
#         settings.CLIENT_CONFIG.timeout = 0.5
#         self.transport.delay = 0.5
#         assert self.transport.queue == []
#         self.transport.periodic_post(url="url_post", data={"d1": "v1"})
#         assert self.transport.queue == []
#         time.sleep(0.03)
#         assert self.transport.get_periodic_http_worker().is_alive() is True
#         self.transport.get_periodic_http_worker().atexit()
#         queue = self.transport.queue
#         assert len(queue) == 1
#         assert queue[0][0] == "post"
#         assert queue[0][1] == "url_post"
#         assert queue[0][2]["data"] == [{"d1": "v1"}]
#         assert self.transport.periodic_http_done == 1
#         assert self.transport.periodic_http_exceptions == 0
#         assert self.transport.periodic_http_worker.is_alive() is False
#
#         # Exception transport
#         self.exception_transport.delay = 0.5
#         self.exception_transport.periodic_post(url="url_post", data={"d1": "v1"})
#         assert self.exception_transport.periodic_http_done == 0
#         assert self.exception_transport.periodic_http_exceptions == 0
#         time.sleep(0.1)
#         assert self.exception_transport.periodic_http_worker.is_alive() is True
#         self.exception_transport.periodic_http_worker.atexit()
#         assert self.exception_transport.periodic_http_done == 1
#         assert self.exception_transport.periodic_http_exceptions == 1
#         assert self.exception_transport.periodic_http_worker.is_alive() is False
