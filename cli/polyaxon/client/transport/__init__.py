#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

from polyaxon.client.transport.http_transport import HttpTransportMixin
from polyaxon.client.transport.periodic_transport import (
    PeriodicHttpTransportMixin,
    PeriodicWSTransportMixin,
)
from polyaxon.client.transport.socket_transport import SocketTransportMixin
from polyaxon.client.transport.threaded_transport import ThreadedTransportMixin
from polyaxon.exceptions import AuthenticationError
from polyaxon.logger import logger


class Transport(
    HttpTransportMixin,
    PeriodicHttpTransportMixin,
    PeriodicWSTransportMixin,
    ThreadedTransportMixin,
    SocketTransportMixin,
):
    """Transport for handling http/ws operations."""

    def __init__(self, config=None):
        self.config = config

    def _get_headers(self, headers=None):
        request_headers = headers or {}
        # Auth headers if access_token is present
        if self.config:
            if "Authorization" not in request_headers and self.config.token:
                request_headers.update(
                    {
                        "Authorization": "{} {}".format(
                            self.config.authentication_type, self.config.token
                        )
                    }
                )
            if self.config.client_header:
                request_headers.update(self.config.client_header)
        return request_headers

    def handle_exception(self, e, log_message=None):
        logger.info("%s: %s", log_message, e.message)

        if self.config.reraise:
            raise e

        if isinstance(e, AuthenticationError):
            # exit now since there is nothing we can do without login
            raise e
