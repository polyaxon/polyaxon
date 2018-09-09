# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import requests

from requests.adapters import HTTPAdapter

from urllib3 import Retry

from polyaxon_client.logger import logger
from polyaxon_client.workers.queue_worker import QueueWorker


class ThreadedTransportMixin(object):
    """Threads operations transport."""

    @property
    def done(self):
        if hasattr(self, '_done'):
            return self._done
        return None

    @property
    def exceptions(self):
        if hasattr(self, '_exceptions'):
            return self._exceptions
        return None

    @property
    def retry_session(self):
        if not hasattr(self, '_retry_session'):
            self._retry_session = requests.Session()
            retry = Retry(
                total=3,
                read=3,
                connect=3,
                backoff_factor=2,
                status_forcelist=[500, 502, 503, 504],
            )
            adapter = HTTPAdapter(max_retries=retry)
            self._retry_session.mount('http://', adapter)
            self._retry_session.mount('https://', adapter)
            self._done = 0
            self._exceptions = 0
        return self._retry_session

    def queue_request(self, request, url, **kwargs):
        try:
            request(url=url, session=self.retry_session, **kwargs)
        except Exception as e:
            self._exceptions += 1
            logger.debug('Error making request url: %s, params: params %s, exp: %s', url, kwargs, e)
        finally:
            self._done += 1

    @property
    def worker(self):
        if not hasattr(self, '_worker') or not self._worker.is_alive():
            self._worker = QueueWorker(timeout=self.config.timeout)
            self._worker.start()
        return self._worker

    def async_post(self,
                   url,
                   params=None,
                   data=None,
                   files=None,
                   json_data=None,
                   timeout=None,
                   headers=None):
        """Async Call request with a post."""
        return self.worker.queue(self.queue_request,
                                 request=self.post,
                                 url=url,
                                 params=params,
                                 data=data,
                                 files=files,
                                 json_data=json_data,
                                 timeout=timeout,
                                 headers=headers)

    def async_patch(self,
                    url,
                    params=None,
                    data=None,
                    files=None,
                    json_data=None,
                    timeout=None,
                    headers=None):
        """Async Call request with a patch."""
        return self.worker.queue(self.queue_request,
                                 request=self.patch,
                                 url=url,
                                 params=params,
                                 data=data,
                                 files=files,
                                 json_data=json_data,
                                 timeout=timeout,
                                 headers=headers)

    def async_delete(self,
                     url,
                     params=None,
                     data=None,
                     files=None,
                     json_data=None,
                     timeout=None,
                     headers=None):
        """Async Call request with a delete."""
        return self.worker.queue(self.queue_request,
                                 request=self.delete,
                                 url=url,
                                 params=params,
                                 data=data,
                                 files=files,
                                 json_data=json_data,
                                 timeout=timeout,
                                 headers=headers)

    def async_put(self,
                  url,
                  params=None,
                  data=None,
                  files=None,
                  json_data=None,
                  timeout=None,
                  headers=None):
        """Async Call request with a put."""
        return self.worker.queue(self.queue_request,
                                 request=self.put,
                                 url=url,
                                 params=params,
                                 data=data,
                                 files=files,
                                 json_data=json_data,
                                 timeout=timeout,
                                 headers=headers)

    def async_upload(self,
                     url,
                     files,
                     files_size,
                     params=None,
                     json_data=None,
                     timeout=3600,
                     headers=None):
        return self.worker.queue(self.queue_request,
                                 request=self.upload,
                                 url=url,
                                 files=files,
                                 files_size=files_size,
                                 params=params,
                                 json_data=json_data,
                                 timeout=timeout,
                                 headers=headers)
