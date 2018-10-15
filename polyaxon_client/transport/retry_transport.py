# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import requests

from requests.adapters import HTTPAdapter

from urllib3 import Retry


class RetryTransportMixin(object):
    """Threads operations transport."""

    @property
    def retry_session(self):
        if not hasattr(self, '_retry_session'):
            self._retry_session = requests.Session()
            retry = Retry(
                total=3,
                read=3,
                connect=3,
                backoff_factor=2,
                status_forcelist=[429, 500, 502, 503, 504],
            )
            adapter = HTTPAdapter(max_retries=retry)
            self._retry_session.mount('http://', adapter)
            self._retry_session.mount('https://', adapter)
            self._threaded_done = 0
            self._threaded_exceptions = 0
            self._periodic_http_done = 0
            self._periodic_http_exceptions = 0
            self._periodic_ws_done = 0
            self._periodic_ws_exceptions = 0
        return self._retry_session
