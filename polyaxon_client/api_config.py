# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from hestia.auth import AuthenticationTypes

from polyaxon_client import settings
from polyaxon_client.exceptions import PolyaxonClientException


class ApiConfig(object):
    PAGE_SIZE = 20
    BASE_URL = "{}/api/{}"
    BASE_WS_URL = "{}/ws/{}"

    def __init__(self,
                 host=None,
                 port=None,
                 http_port=None,
                 ws_port=None,
                 token=None,
                 version=None,
                 authentication_type=None,
                 use_https=None,
                 verify_ssl=None,
                 is_managed=None,
                 is_local=None,
                 schema_response=None,
                 reraise=False,
                 timeout=None,
                 interval=None):

        self.token = token or settings.SECRET_USER_TOKEN
        self.host = host or settings.API_HOST
        self.is_managed = self._get_bool(is_managed, settings.IS_MANAGED)
        self.is_local = self._get_bool(is_local, settings.IS_LOCAL)
        self.use_https = self._get_bool(use_https, settings.USE_HTTPS)
        self.verify_ssl = self._get_bool(verify_ssl, settings.VERIFY_SSL)

        if not self.host and not self.is_managed:
            raise PolyaxonClientException(
                'Api config requires at least a host if not running in-cluster.')

        self.port = port
        if port:
            self.http_port = port
            self.ws_port = port
        else:
            self.http_port = http_port or settings.HTTP_PORT or (settings.DEFAULT_HTTPS_PORT
                                                                 if self.use_https
                                                                 else settings.DEFAULT_HTTP_PORT)
            self.ws_port = ws_port or settings.WS_PORT or self.http_port
        self.version = version or settings.API_VERSION
        self.internal_header = None

        if self.is_managed and not self.is_local:
            if not settings.API_HTTP_HOST:
                print('Could get api host info, '
                      'please make sure this is running inside a polyaxon job.')
            self.http_host = settings.API_HTTP_HOST
            self.ws_host = settings.API_WS_HOST
            if all([settings.INTERNAL_HEADER, settings.INTERNAL_HEADER_SERVICE]):
                self.internal_header = {settings.INTERNAL_HEADER: settings.INTERNAL_HEADER_SERVICE}

            internal_token_cond = (
                self.internal_header and
                not self.token and
                settings.SECRET_INTERNAL_TOKEN
            )
            if internal_token_cond:
                self.token = settings.SECRET_INTERNAL_TOKEN
        else:
            http_protocol = 'https' if self.use_https else 'http'
            ws_protocol = 'wss' if self.use_https else 'ws'
            self.http_host = '{}://{}:{}'.format(http_protocol, self.host, self.http_port)
            self.ws_host = '{}://{}:{}'.format(ws_protocol, self.host, self.ws_port)
        self.base_url = self.BASE_URL.format(self.http_host, self.version)
        self.base_ws_url = self.BASE_WS_URL.format(self.ws_host, self.version)
        self.authentication_type = (authentication_type or
                                    settings.AUTHENTICATION_TYPE or
                                    AuthenticationTypes.TOKEN)
        self.schema_response = self._get_bool(schema_response, settings.SCHEMA_RESPONSE)
        self.reraise = reraise
        self.timeout = timeout if timeout is not None else settings.TIMEOUT
        self.interval = interval if timeout is not None else settings.INTERVAL

    @staticmethod
    def _get_bool(value, default_value):
        if isinstance(value, bool):
            return value

        return default_value
