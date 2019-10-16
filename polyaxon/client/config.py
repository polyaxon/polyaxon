# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import polyaxon_sdk
from hestia.auth import AuthenticationTypes

from polyaxon.client import settings
from polyaxon.client.exceptions import PolyaxonClientException
from polyaxon.managers.auth import AuthConfigManager
from polyaxon.managers.config import GlobalConfigManager
from polyaxon.utils.formatting import Printer


class ClientConfig(object):
    PAGE_SIZE = 20
    BASE_URL = "{}/api/{}"

    def __init__(
        self,
        host=None,
        token=None,
        version=None,
        authentication_type=None,
        verify_ssl=None,
        ssl_ca_cert=None,
        cert_file=None,
        key_file=None,
        assert_hostname=None,
        connection_pool_maxsize=None,
        is_managed=None,
        is_local=None,
        schema_response=None,
        reraise=False,
        timeout=None,
        interval=None,
        debug=False
    ):

        self.token = token or settings.SECRET_USER_TOKEN
        self.host = host or settings.API_HOST
        self.is_managed = self._get_bool(is_managed, settings.IS_MANAGED)
        self.is_local = self._get_bool(is_local, settings.IS_LOCAL)
        self.verify_ssl = self._get_bool(verify_ssl, settings.VERIFY_SSL)
        self.ssl_ca_cert = ssl_ca_cert or settings.SSL_CA_CERT
        self.cert_file = cert_file or settings.CERT_FILE
        self.key_file = key_file or settings.KEY_FILE
        self.assert_hostname = assert_hostname or settings.ASSERT_HOSTNAME
        self.connection_pool_maxsize = connection_pool_maxsize or settings.CONNECTION_POOL_MAX_SIZE
        self.debug = debug
        if self.debug is None and settings.LOG_LEVEL:
            self.debug = settings.LOG_LEVEL.upper() == "DEBUG"

        if not self.host and not self.is_managed:
            raise PolyaxonClientException(
                "Api config requires at least a host if not running in-cluster."
            )

        self.version = version or settings.API_VERSION
        self.service_header = None

        if self.is_managed and not self.is_local:
            if all([settings.HEADER, settings.HEADER_SERVICE]):
                self.service_header = {settings.HEADER: settings.HEADER_SERVICE}

            internal_token_cond = (
                self.service_header
                and not self.token
                and settings.SECRET_INTERNAL_TOKEN
            )
            if internal_token_cond:
                self.token = settings.SECRET_INTERNAL_TOKEN

        self.base_url = self.BASE_URL.format(self.host, self.version)
        self.authentication_type = (
            authentication_type
            or settings.AUTHENTICATION_TYPE
            or AuthenticationTypes.TOKEN
        )
        self.schema_response = self._get_bool(schema_response, settings.SCHEMA_RESPONSE)
        self.reraise = reraise
        self.timeout = timeout if timeout is not None else settings.TIMEOUT
        self.interval = interval if timeout is not None else settings.INTERVAL

    @classmethod
    def get_config_from_manager(cls):
        host = GlobalConfigManager.get_value("host")
        if not host:
            Printer.print_error(
                "Received an invalid config, you need to provide a valid host."
            )
            sys.exit(1)
        verify_ssl = GlobalConfigManager.get_value("verify_ssl")
        token = AuthConfigManager.get_value("token")
        return cls(
            host=host,
            verify_ssl=verify_ssl,
            token=token
        )

    @property
    def sdk_config(self):
        config = polyaxon_sdk.Configuration()
        config.debug = self.debug
        config.host = self.host
        config.verify_ssl = self.verify_ssl
        config.ssl_ca_cert = self.ssl_ca_cert
        config.cert_file = self.cert_file
        config.key_file = self.key_file
        config.assert_hostname = self.assert_hostname
        if self.connection_pool_maxsize:
            config.connection_pool_maxsize = self.connection_pool_maxsize
        if self.token:
            config.api_key['Authorization'] = self.token
            config.api_key_prefix['Authorization'] = self.authentication_type
        return config

    @staticmethod
    def _get_bool(value, default_value):
        if isinstance(value, bool):
            return value

        return default_value
