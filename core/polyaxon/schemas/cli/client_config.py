#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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
import urllib3

from marshmallow import EXCLUDE, fields

import polyaxon_sdk

from polyaxon.api import LOCALHOST, POLYAXON_CLOUD_HOST
from polyaxon.contexts import paths as ctx_paths
from polyaxon.env_vars.keys import (
    EV_KEYS_API_VERSION,
    EV_KEYS_ARCHIVE_ROOT,
    EV_KEYS_ASSERT_HOSTNAME,
    EV_KEYS_AUTHENTICATION_TYPE,
    EV_KEYS_CERT_FILE,
    EV_KEYS_CONNECTION_POOL_MAXSIZE,
    EV_KEYS_DEBUG,
    EV_KEYS_DISABLE_ERRORS_REPORTING,
    EV_KEYS_HEADER,
    EV_KEYS_HEADER_SERVICE,
    EV_KEYS_HOST,
    EV_KEYS_INTERVAL,
    EV_KEYS_INTERVALS_COMPATIBILITY_CHECK,
    EV_KEYS_IS_MANAGED,
    EV_KEYS_IS_OFFLINE,
    EV_KEYS_K8S_IN_CLUSTER,
    EV_KEYS_K8S_NAMESPACE,
    EV_KEYS_KEY_FILE,
    EV_KEYS_LOG_LEVEL,
    EV_KEYS_NO_API,
    EV_KEYS_NO_OP,
    EV_KEYS_SSL_CA_CERT,
    EV_KEYS_TIME_ZONE,
    EV_KEYS_TIMEOUT,
    EV_KEYS_TRACKING_TIMEOUT,
    EV_KEYS_VERIFY_SSL,
    EV_KEYS_WATCH_INTERVAL,
)
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.pkg import VERSION
from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.services.auth import AuthenticationTypes
from polyaxon.services.headers import PolyaxonServiceHeaders
from polyaxon.services.values import PolyaxonServices
from polyaxon.utils.http_utils import clean_host


class ClientSchema(BaseSchema):
    host = fields.Str(allow_none=True, data_key=EV_KEYS_HOST)
    version = fields.Str(allow_none=True, data_key=EV_KEYS_API_VERSION)
    debug = fields.Bool(allow_none=True, data_key=EV_KEYS_DEBUG)
    log_level = fields.Str(allow_none=True, data_key=EV_KEYS_LOG_LEVEL)
    authentication_type = fields.Str(
        allow_none=True, data_key=EV_KEYS_AUTHENTICATION_TYPE
    )
    is_managed = fields.Bool(allow_none=True, data_key=EV_KEYS_IS_MANAGED)
    is_offline = fields.Bool(allow_none=True, data_key=EV_KEYS_IS_OFFLINE)
    in_cluster = fields.Bool(allow_none=True, data_key=EV_KEYS_K8S_IN_CLUSTER)
    no_op = fields.Bool(allow_none=True, data_key=EV_KEYS_NO_OP)
    timeout = fields.Float(allow_none=True, data_key=EV_KEYS_TIMEOUT)
    tracking_timeout = fields.Float(allow_none=True, data_key=EV_KEYS_TRACKING_TIMEOUT)
    timezone = fields.Str(allow_none=True, data_key=EV_KEYS_TIME_ZONE)
    watch_interval = fields.Int(allow_none=True, data_key=EV_KEYS_WATCH_INTERVAL)
    interval = fields.Float(allow_none=True, data_key=EV_KEYS_INTERVAL)
    verify_ssl = fields.Bool(allow_none=True, data_key=EV_KEYS_VERIFY_SSL)
    ssl_ca_cert = fields.Str(allow_none=True, data_key=EV_KEYS_SSL_CA_CERT)
    cert_file = fields.Str(allow_none=True, data_key=EV_KEYS_CERT_FILE)
    key_file = fields.Str(allow_none=True, data_key=EV_KEYS_KEY_FILE)
    assert_hostname = fields.Bool(allow_none=True, data_key=EV_KEYS_ASSERT_HOSTNAME)
    connection_pool_maxsize = fields.Int(
        allow_none=True, data_key=EV_KEYS_CONNECTION_POOL_MAXSIZE
    )
    archive_root = fields.Str(allow_none=True, data_key=EV_KEYS_ARCHIVE_ROOT)

    header = fields.Str(allow_none=True, data_key=EV_KEYS_HEADER)
    header_service = fields.Str(allow_none=True, data_key=EV_KEYS_HEADER_SERVICE)

    namespace = fields.Str(allow_none=True, data_key=EV_KEYS_K8S_NAMESPACE)
    no_api = fields.Bool(allow_none=True, data_key=EV_KEYS_NO_API)
    disable_errors_reporting = fields.Bool(
        allow_none=True, data_key=EV_KEYS_DISABLE_ERRORS_REPORTING
    )
    compatibility_check_interval = fields.Int(
        allow_none=True, data_key=EV_KEYS_INTERVALS_COMPATIBILITY_CHECK
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
        EV_KEYS_HOST,
        EV_KEYS_API_VERSION,
        EV_KEYS_ASSERT_HOSTNAME,
        EV_KEYS_AUTHENTICATION_TYPE,
        EV_KEYS_CERT_FILE,
        EV_KEYS_CONNECTION_POOL_MAXSIZE,
        EV_KEYS_ARCHIVE_ROOT,
        EV_KEYS_DEBUG,
        EV_KEYS_HEADER,
        EV_KEYS_HEADER_SERVICE,
        EV_KEYS_K8S_IN_CLUSTER,
        EV_KEYS_INTERVAL,
        EV_KEYS_IS_MANAGED,
        EV_KEYS_IS_OFFLINE,
        EV_KEYS_K8S_NAMESPACE,
        EV_KEYS_KEY_FILE,
        EV_KEYS_LOG_LEVEL,
        EV_KEYS_NO_API,
        EV_KEYS_NO_OP,
        EV_KEYS_SSL_CA_CERT,
        EV_KEYS_TIMEOUT,
        EV_KEYS_TRACKING_TIMEOUT,
        EV_KEYS_VERIFY_SSL,
        EV_KEYS_WATCH_INTERVAL,
        EV_KEYS_DISABLE_ERRORS_REPORTING,
        EV_KEYS_INTERVALS_COMPATIBILITY_CHECK,
    ]

    def __init__(
        self,
        host=None,
        token=None,
        debug=None,
        log_level=None,
        version=None,
        authentication_type=None,
        is_managed=None,
        is_offline=None,
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
        use_cloud_host: bool = False,
        retries: int = None,
        **kwargs
    ):
        self.host = (
            clean_host(host or LOCALHOST) if not use_cloud_host else POLYAXON_CLOUD_HOST
        )
        self.retries = retries if not use_cloud_host else 0
        self.token = token
        self.debug = self._get_bool(debug, False)
        self.log_level = log_level
        self.version = version or "v1"
        self.is_managed = self._get_bool(is_managed, False)
        self.is_offline = self._get_bool(is_offline, False)
        self.in_cluster = self._get_bool(in_cluster, False)
        self.no_op = self._get_bool(no_op, False)
        self.verify_ssl = verify_ssl
        self.ssl_ca_cert = ssl_ca_cert
        self.cert_file = cert_file
        self.key_file = key_file
        self.assert_hostname = self._get_bool(assert_hostname, None)
        self.connection_pool_maxsize = connection_pool_maxsize
        self.archive_root = archive_root or ctx_paths.CONTEXT_ARCHIVE_ROOT
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

    def get_full_headers(self, headers=None, auth_key="Authorization"):
        request_headers = {}
        request_headers.update(headers or {})
        request_headers.update(self.client_header or {})

        if auth_key not in request_headers and self.token:
            request_headers.update(
                {auth_key: "{} {}".format(self.authentication_type, self.token)}
            )
        if self.header and self.header_service:
            request_headers.update({self.header: self.header_service})
        return request_headers

    @property
    def sdk_config(self):
        if not self.host and not self.in_cluster:
            raise PolyaxonClientException(
                "Api config requires at least a host if not running in-cluster."
            )

        config = polyaxon_sdk.Configuration()
        config.retries = self.retries
        config.debug = self.debug
        config.host = clean_host(self.host)
        config.verify_ssl = self.verify_ssl
        if not config.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        config.ssl_ca_cert = self.ssl_ca_cert
        config.cert_file = self.cert_file
        config.key_file = self.key_file
        config.assert_hostname = self.assert_hostname
        if self.connection_pool_maxsize:
            config.connection_pool_maxsize = self.connection_pool_maxsize
        if self.token:
            config.api_key["ApiKey"] = self.token
            config.api_key_prefix["ApiKey"] = self.authentication_type
        return config

    @property
    def sdk_async_config(self):
        config = self.sdk_config
        config.connection_pool_maxsize = 100
        return config

    @classmethod
    def patch_from(cls, config: "ClientConfig", **kwargs):
        data = {**config.to_dict(), **kwargs}
        return cls.from_dict(data)
