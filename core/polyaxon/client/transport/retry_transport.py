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

import requests

from requests.adapters import HTTPAdapter

from urllib3 import Retry


class RetryTransportMixin:
    """Threads operations transport."""

    @property
    def retry_session(self):
        if not hasattr(self, "_retry_session"):
            self._retry_session = requests.Session()
            retry = Retry(
                total=3,
                read=3,
                connect=3,
                backoff_factor=2,
                status_forcelist=[429, 500, 502, 503, 504],
            )
            adapter = HTTPAdapter(max_retries=retry)
            self._retry_session.mount("http://", adapter)
            self._retry_session.mount("https://", adapter)
            self._threaded_done = 0
            self._threaded_exceptions = 0
            self._periodic_http_done = 0
            self._periodic_http_exceptions = 0
            self._periodic_ws_done = 0
            self._periodic_ws_exceptions = 0
        return self._retry_session
