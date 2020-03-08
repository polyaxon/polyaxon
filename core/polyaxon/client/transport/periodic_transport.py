#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

from polyaxon import settings
from polyaxon.client.transport.retry_transport import RetryTransportMixin
from polyaxon.client.workers.periodic_worker import PeriodicWorker
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.logger import logger


class PeriodicHttpTransportMixin(RetryTransportMixin):
    """Periodic http operations transport."""

    @property
    def periodic_http_done(self):
        if hasattr(self, "_periodic_http_done"):
            return self._periodic_http_done
        return None

    @property
    def periodic_http_exceptions(self):
        if hasattr(self, "_periodic_http_exceptions"):
            return self._periodic_http_exceptions
        return None

    def queue_periodic_request(self, request, url, **kwargs):
        try:
            request(url=url, session=self.retry_session, **kwargs)
        except Exception as e:
            self._periodic_http_exceptions += 1
            logger.debug(
                "Error making request url: %s, params: params %s, exp: %s",
                url,
                kwargs,
                e,
            )
        finally:
            self._periodic_http_done += 1

    @property
    def periodic_http_worker(self):
        if hasattr(self, "_periodic_http_worker"):
            return self._periodic_http_worker
        return None

    def get_periodic_http_worker(self, **kwargs):
        worker = self.periodic_http_worker
        if not worker or not worker.is_alive():
            if "request" not in kwargs:
                raise PolyaxonClientException(
                    "Periodic worker expects a request argument."
                )
            self._periodic_http_worker = PeriodicWorker(
                callback=self.queue_periodic_request,
                worker_interval=settings.CLIENT_CONFIG.interval,
                worker_timeout=settings.CLIENT_CONFIG.timeout,
                kwargs=kwargs,
            )
            self._periodic_http_worker.start()
        return self.periodic_http_worker

    def set_health_check(self, url):
        worker = self.get_periodic_http_worker(request=self.post)
        worker.queue_health(url)

    def unset_health_check(self, url):
        worker = self.get_periodic_http_worker(request=self.post)
        worker.unqueue_health(url)

    def periodic_post(
        self,
        url,
        params=None,
        data=None,
        files=None,
        json_data=None,
        timeout=None,
        headers=None,
    ):
        """Periodic Async Call request with a post."""
        worker = self.get_periodic_http_worker(
            request=self.post,
            params=params,
            files=files,
            timeout=timeout,
            headers=headers,
        )
        return worker.queue(url=url, data=data, json_data=json_data)


class PeriodicWSTransportMixin(RetryTransportMixin):
    """Periodic websocket operations transport."""

    @property
    def periodic_ws_done(self):
        if hasattr(self, "_periodic_ws_done"):
            return self._periodic_ws_done
        return None

    @property
    def periodic_ws_exceptions(self):
        if hasattr(self, "_periodic_ws_exceptions"):
            return self._periodic_ws_exceptions
        return None

    def queue_ws_request(self, request, url, **kwargs):
        try:
            request(url=url, **kwargs)
        except Exception as e:
            self._periodic_ws_exceptions += 1
            logger.debug(
                "Error making request url: %s, params: params %s, exp: %s",
                url,
                kwargs,
                e,
            )
        finally:
            self._periodic_ws_done += 1

    @property
    def periodic_ws_workers(self):
        if not hasattr(self, "_periodic_ws_workers"):
            self._periodic_ws_workers = {}

        return self._periodic_ws_workers

    def get_periodic_http_worker(self, url, **kwargs):
        worker = self.periodic_ws_workers.get(url)
        if not worker or not worker.is_alive():
            kwargs["url"] = url
            kwargs["request"] = self.socket(url, message_handler=None, **kwargs)
            worker = PeriodicWorker(
                callback=self.queue_ws_request,
                worker_interval=settings.CLIENT_CONFIG.interval,
                worker_timeout=settings.CLIENT_CONFIG.timeout,
                kwargs=kwargs,
            )
            worker.start()
            self.periodic_ws_workers[url] = worker
        return self.periodic_ws_workers[url]

    def periodic_send(self, url, data=None, headers=None):
        """Periodic Async Call request with a post."""
        worker = self.get_periodic_http_worker(url=url, headers=headers)
        return worker.queue(data=data)
