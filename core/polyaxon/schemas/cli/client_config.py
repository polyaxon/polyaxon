#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

import polyaxon_sdk

from marshmallow import EXCLUDE, fields

from polyaxon.api import get_default_host
from polyaxon.containers.contexts import CONTEXT_ARCHIVE_ROOT
from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_API_VERSION,
    POLYAXON_KEYS_ARCHIVE_ROOT,
    POLYAXON_KEYS_ASSERT_HOSTNAME,
    POLYAXON_KEYS_AUTHENTICATION_TYPE,
    POLYAXON_KEYS_CERT_FILE,
    POLYAXON_KEYS_CONNECTION_POOL_MAXSIZE,
    POLYAXON_KEYS_DEBUG,
    POLYAXON_KEYS_DISABLE_ERRORS_REPORTING,
    POLYAXON_KEYS_HEADER,
    POLYAXON_KEYS_HEADER_SERVICE,
    POLYAXON_KEYS_HOST,
    POLYAXON_KEYS_INTERVAL,
    POLYAXON_KEYS_INTERVALS_COMPATIBILITY_CHECK,
    POLYAXON_KEYS_IS_MANAGED,
    POLYAXON_KEYS_IS_OFFLINE,
    POLYAXON_KEYS_IS_OPS,
    POLYAXON_KEYS_K8S_IN_CLUSTER,
    POLYAXON_KEYS_K8S_NAMESPACE,
    POLYAXON_KEYS_KEY_FILE,
    POLYAXON_KEYS_LOG_LEVEL,
    POLYAXON_KEYS_NO_API,
    POLYAXON_KEYS_NO_OP,
    POLYAXON_KEYS_SERVICE,
    POLYAXON_KEYS_SSL_CA_CERT,
    POLYAXON_KEYS_TIME_ZONE,
    POLYAXON_KEYS_TIMEOUT,
    POLYAXON_KEYS_TRACKING_TIMEOUT,
    POLYAXON_KEYS_VERIFY_SSL,
    POLYAXON_KEYS_WATCH_INTERVAL,
)
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.pkg import VERSION
from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.services.auth import AuthenticationTypes
from polyaxon.services.headers import PolyaxonServiceHeaders, PolyaxonServices
from polyaxon.utils.http_utils import clean_host, clean_verify_ssl


class ClientSchema(BaseSchema):
    service = fields.Str(allow_none=True, data_key=POLYAXON_KEYS_SERVICE)
    host = fields.Str(allow_none=True, data_key=POLYAXON_KEYS_HOST)
    version = fields.Str(allow_none=True, data_key=POLYAXON_KEYS_API_VERSION)
    debug = fields.Bool(allow_none=True, data_key=POLYAXON_KEYS_DEBUG)
    log_level = fields.Str(allow_none=True, data_key=POLYAXON_KEYS_LOG_LEVEL)
    authentication_type = fields.Str(
        allow_none=True, data_key=POLYAXON_KEYS_AUTHENTICATION_TYPE
    )
    is_managed = fields.Bool(allow_none=True, data_key=POLYAXON_KEYS_IS_MANAGED)
    is_offline = fields.Bool(allow_none=True, data_key=POLYAXON_KEYS_IS_OFFLINE)
    is_ops = fields.Bool(allow_none=True, data_key=POLYAXON_KEYS_IS_OPS)
    in_cluster = fields.Bool(allow_none=True, data_key=POLYAXON_KEYS_K8S_IN_CLUSTER)
    no_op = fields.Bool(allow_none=True, data_key=POLYAXON_KEYS_NO_OP)
    timeout = fields.Float(allow_none=True, data_key=POLYAXON_KEYS_TIMEOUT)
    tracking_timeout = fields.Float(
        allow_none=True, data_key=POLYAXON_KEYS_TRACKING_TIMEOUT
    )
    timezone = fields.Str(
        allow_none=True, data_key=POLYAXON_KEYS_TIME_ZONE, default="UTC"
    )
    watch_interval = fields.Int(allow_none=True, data_key=POLYAXON_KEYS_WATCH_INTERVAL)
    interval = fields.Float(allow_none=True, data_key=POLYAXON_KEYS_INTERVAL)
    verify_ssl = fields.Bool(allow_none=True, data_key=POLYAXON_KEYS_VERIFY_SSL)
    ssl_ca_cert = fields.Str(allow_none=True, data_key=POLYAXON_KEYS_SSL_CA_CERT)
    cert_file = fields.Str(allow_none=True, data_key=POLYAXON_KEYS_CERT_FILE)
    key_file = fields.Str(allow_none=True, data_key=POLYAXON_KEYS_KEY_FILE)
    assert_hostname = fields.Bool(
        allow_none=True, data_key=POLYAXON_KEYS_ASSERT_HOSTNAME
    )
    connection_pool_maxsize = fields.Int(
        allow_none=True, data_key=POLYAXON_KEYS_CONNECTION_POOL_MAXSIZE
    )
    archive_root = fields.Str(allow_none=True, data_key=POLYAXON_KEYS_ARCHIVE_ROOT)

    header = fields.Str(allow_none=True, data_key=POLYAXON_KEYS_HEADER)
    header_service = fields.Str(allow_none=True, data_key=POLYAXON_KEYS_HEADER_SERVICE)

    namespace = fields.Str(allow_none=True, data_key=POLYAXON_KEYS_K8S_NAMESPACE)
    no_api = fields.Bool(allow_none=True, data_key=POLYAXON_KEYS_NO_API)
    disable_errors_reporting = fields.Bool(
        allow_none=True, data_key=POLYAXON_KEYS_DISABLE_ERRORS_REPORTING
    )
    compatibility_check_interval = fields.Int(
        allow_none=True, data_key=POLYAXON_KEYS_INTERVALS_COMPATIBILITY_CHECK
    )

    @staticmethod
    def schema_config():
        return ClientConfig


class ClientConfig(BaseConfig):
    SCHEMA = ClientSchema
    IDENTIFIER = "global"

    PAGE_SIZE = 20
    BASE_URL = "{}/api/{}"

    UNKNOWN_BEHAVIOUR = EXCLUDE

    REDUCED_ATTRIBUTES = [
        POLYAXON_KEYS_SERVICE,
        POLYAXON_KEYS_HOST,
        POLYAXON_KEYS_API_VERSION,
        POLYAXON_KEYS_ASSERT_HOSTNAME,
        POLYAXON_KEYS_AUTHENTICATION_TYPE,
        POLYAXON_KEYS_CERT_FILE,
        POLYAXON_KEYS_CONNECTION_POOL_MAXSIZE,
        POLYAXON_KEYS_ARCHIVE_ROOT,
        POLYAXON_KEYS_DEBUG,
        POLYAXON_KEYS_HEADER,
        POLYAXON_KEYS_HEADER_SERVICE,
        POLYAXON_KEYS_K8S_IN_CLUSTER,
        POLYAXON_KEYS_INTERVAL,
        POLYAXON_KEYS_IS_MANAGED,
        POLYAXON_KEYS_IS_OFFLINE,
        POLYAXON_KEYS_IS_OPS,
        POLYAXON_KEYS_K8S_NAMESPACE,
        POLYAXON_KEYS_KEY_FILE,
        POLYAXON_KEYS_LOG_LEVEL,
        POLYAXON_KEYS_NO_API,
        POLYAXON_KEYS_NO_OP,
        POLYAXON_KEYS_SSL_CA_CERT,
        POLYAXON_KEYS_TIMEOUT,
        POLYAXON_KEYS_TRACKING_TIMEOUT,
        POLYAXON_KEYS_VERIFY_SSL,
        POLYAXON_KEYS_WATCH_INTERVAL,
        POLYAXON_KEYS_DISABLE_ERRORS_REPORTING,
        POLYAXON_KEYS_INTERVALS_COMPATIBILITY_CHECK,
    ]

    def __init__(
        self,
        service=None,
        host=None,
        token=None,
        debug=None,
        log_level=None,
        version=None,
        authentication_type=None,
        is_managed=None,
        is_offline=None,
        is_ops=None,
        in_cluster=None,
        no_op=None,
        timeout=None,
        tracking_timeout=None,
        timezone=None,
        watch_interval=None,
        interval=None,
        verify_ssl=None,
        ssl_ca_cert=None,
        cert_file=None,
        key_file=None,
        assert_hostname=None,
        connection_pool_maxsize=None,
        archive_root=None,
        header=None,
        header_service=None,
        namespace=None,
        no_api=None,
        disable_errors_reporting=None,
        compatibility_check_interval=None,
        **kwargs
    ):
        self.service = service
        self.host = clean_host(get_default_host(host, service))
        self.token = token
        self.debug = self._get_bool(debug, False)
        self.log_level = log_level
        self.version = version or "v1"
        self.is_managed = self._get_bool(is_managed, False)
        self.is_offline = self._get_bool(is_offline, False)
        self.is_ops = self._get_bool(is_ops, False)
        self.in_cluster = self._get_bool(in_cluster, False)
        self.no_op = self._get_bool(no_op, False)
        self.verify_ssl = clean_verify_ssl(
            host=self.host, verify_ssl=self._get_bool(verify_ssl, None)
        )
        self.ssl_ca_cert = ssl_ca_cert
        self.cert_file = cert_file
        self.key_file = key_file
        self.assert_hostname = self._get_bool(assert_hostname, None)
        self.connection_pool_maxsize = connection_pool_maxsize
        self.archive_root = archive_root or CONTEXT_ARCHIVE_ROOT
        self.header = header
        self.header_service = header_service
        self.timeout = timeout or 20
        self.tracking_timeout = tracking_timeout or 1
        self.timezone = timezone
        self.interval = interval or 5
        self.watch_interval = watch_interval or 5
        self.namespace = namespace
        self.no_api = self._get_bool(no_api, False)
        self.authentication_type = authentication_type or AuthenticationTypes.TOKEN
        self.disable_errors_reporting = self._get_bool(disable_errors_reporting, False)
        self.compatibility_check_interval = compatibility_check_interval

        self.client_header = {}

        if all([self.header, self.header_service]):
            self.client_header["header_name"] = self.header
            self.client_header["header_value"] = self.header_service

    @property
    def base_url(self):
        return self.BASE_URL.format(clean_host(self.host), self.version)

    def set_cli_header(self):
        self.header = PolyaxonServiceHeaders.get_header(PolyaxonServiceHeaders.SERVICE)
        self.header_service = VERSION
        self.client_header["header_name"] = self.header
        self.client_header["header_value"] = self.header_service

    def set_agent_header(self):
        self.header = PolyaxonServiceHeaders.get_header(PolyaxonServiceHeaders.SERVICE)
        self.header_service = PolyaxonServices.AGENT
        self.client_header["header_name"] = self.header
        self.client_header["header_value"] = self.header_service

    @property
    def sdk_config(self):
        if not self.host and not self.in_cluster:
            raise PolyaxonClientException(
                "Api config requires at least a host if not running in-cluster."
            )

        config = polyaxon_sdk.Configuration()
        config.debug = self.debug
        config.host = clean_host(self.host)
        config.verify_ssl = clean_verify_ssl(
            host=config.host, verify_ssl=self.verify_ssl
        )
        config.ssl_ca_cert = self.ssl_ca_cert
        config.cert_file = self.cert_file
        config.key_file = self.key_file
        config.assert_hostname = self.assert_hostname
        if self.connection_pool_maxsize:
            config.connection_pool_maxsize = self.connection_pool_maxsize
        if self.token:
            config.api_key["Authorization"] = self.token
            config.api_key_prefix["Authorization"] = self.authentication_type
        return config

    @staticmethod
    def _get_bool(value, default_value):
        if isinstance(value, bool):
            return value

        return default_value
