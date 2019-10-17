# -*- coding: utf-8 -*-
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
