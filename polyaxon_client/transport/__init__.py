# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.exceptions import AuthenticationError
from polyaxon_client.logger import logger
from polyaxon_client.transport.http_transport import HttpTransportMixin
from polyaxon_client.transport.socket_transport import SocketTransportMixin
from polyaxon_client.transport.threaded_transport import ThreadedTransportMixin


class Transport(HttpTransportMixin, ThreadedTransportMixin, SocketTransportMixin):
    """Transport for handling http/ws operations."""

    def __init__(self, token=None, authentication_type='token', reraise=False):
        self.authentication_type = authentication_type
        self.token = token
        self.reraise = reraise
        # Http transport session
        self._session = None
        # Threaded transport worker and session
        self._worker = None
        self._retry_session = None

    def _get_headers(self, headers=None):
        request_headers = headers or {}
        # Auth headers if access_token is present
        if 'Authorization' not in request_headers and self.token:
            request_headers.update({'Authorization': '{} {}'.format(self.authentication_type,
                                                                    self.token)})
        return request_headers

    def handle_exception(self, e, log_message=None):
        logger.info("%s: %s", log_message, e.message)

        if self.reraise:
            raise e

        if isinstance(e, AuthenticationError):
            # exit now since there is nothing we can do without login
            raise e
