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

from polyaxon import settings
from polyaxon.client.transport.retry_transport import RetryTransportMixin
from polyaxon.client.workers.queue_worker import QueueWorker
from polyaxon.logger import logger


class ThreadedTransportMixin(RetryTransportMixin):
    """Threads operations transport."""

    @property
    def threaded_done(self):
        if hasattr(self, "_threaded_done"):
            return self._threaded_done
        return None

    @property
    def threaded_exceptions(self):
        if hasattr(self, "_threaded_exceptions"):
            return self._threaded_exceptions
        return None

    def queue_request(self, request, url, **kwargs):
        try:
            request(url=url, session=self.retry_session, **kwargs)
        except Exception as e:
            self._threaded_exceptions += 1
            logger.debug(
                "Error making request url: %s, params: params %s, exp: %s",
                url,
                kwargs,
                e,
            )
        finally:
            self._threaded_done += 1

    @property
    def worker(self):
        if not hasattr(self, "_worker") or not self._worker.is_alive():
            self._worker = QueueWorker(timeout=settings.CLIENT_CONFIG.timeout)
            self._worker.start()
        return self._worker

    def async_post(
        self,
        url,
        params=None,
        data=None,
        files=None,
        json_data=None,
        timeout=None,
        headers=None,
    ):
        """Async Call request with a post."""
        return self.worker.queue(
            self.queue_request,
            request=self.post,
            url=url,
            params=params,
            data=data,
            files=files,
            json_data=json_data,
            timeout=timeout,
            headers=headers,
        )

    def async_patch(
        self,
        url,
        params=None,
        data=None,
        files=None,
        json_data=None,
        timeout=None,
        headers=None,
    ):
        """Async Call request with a patch."""
        return self.worker.queue(
            self.queue_request,
            request=self.patch,
            url=url,
            params=params,
            data=data,
            files=files,
            json_data=json_data,
            timeout=timeout,
            headers=headers,
        )

    def async_delete(
        self,
        url,
        params=None,
        data=None,
        files=None,
        json_data=None,
        timeout=None,
        headers=None,
    ):
        """Async Call request with a delete."""
        return self.worker.queue(
            self.queue_request,
            request=self.delete,
            url=url,
            params=params,
            data=data,
            files=files,
            json_data=json_data,
            timeout=timeout,
            headers=headers,
        )

    def async_put(
        self,
        url,
        params=None,
        data=None,
        files=None,
        json_data=None,
        timeout=None,
        headers=None,
    ):
        """Async Call request with a put."""
        return self.worker.queue(
            self.queue_request,
            request=self.put,
            url=url,
            params=params,
            data=data,
            files=files,
            json_data=json_data,
            timeout=timeout,
            headers=headers,
        )

    def async_upload(
        self,
        url,
        files,
        files_size,
        params=None,
        json_data=None,
        timeout=3600,
        headers=None,
    ):
        return self.worker.queue(
            self.queue_request,
            request=self.upload,
            url=url,
            files=files,
            files_size=files_size,
            params=params,
            json_data=json_data,
            timeout=timeout,
            headers=headers,
        )
