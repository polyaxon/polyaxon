# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from polyaxon_client.workers.queue_worker import QueueWorker


class ThreadedTransportMixin(object):
    """Threads operations transport."""
    @property
    def retry_session(self):
        if not self._retry_session:
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
        return self._retry_session

    @property
    def worker(self):
        if not self._worker or not self._worker.is_alive():
            self._worker = QueueWorker()
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
        """Call request with a post."""
        return self.post(self,
                         url,
                         params=params,
                         data=data,
                         files=files,
                         json_data=json_data,
                         timeout=timeout,
                         headers=headers,
                         session=self.retry_session)

    def async_patch(self,
                    url,
                    params=None,
                    data=None,
                    files=None,
                    json_data=None,
                    timeout=None,
                    headers=None):
        """Call request with a patch."""
        return self.patch(self,
                          url,
                          params=params,
                          data=data,
                          files=files,
                          json_data=json_data,
                          timeout=timeout,
                          headers=headers,
                          session=self.retry_session)

    def async_delete(self,
                     url,
                     params=None,
                     data=None,
                     files=None,
                     json_data=None,
                     timeout=None,
                     headers=None):
        """Call request with a delete."""
        return self.delete(url,
                           params=params,
                           data=data,
                           files=files,
                           json_data=json_data,
                           timeout=timeout,
                           headers=headers,
                           session=self.retry_session)

    def async_put(self,
                  url,
                  params=None,
                  data=None,
                  files=None,
                  json_data=None,
                  timeout=None,
                  headers=None):
        """Call request with a put."""
        return self.put(url,
                        params=params,
                        data=data,
                        files=files,
                        json_data=json_data,
                        timeout=timeout,
                        headers=headers,
                        session=self.retry_session)
