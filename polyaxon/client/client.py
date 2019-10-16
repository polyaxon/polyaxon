# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from datetime import datetime

import polyaxon_sdk
from hestia.tz_utils import utc

from polyaxon.client import settings
from polyaxon.client.config import ClientConfig
from polyaxon.client.transport import Transport


class PolyaxonClient(object):
    def __init__(
        self,
        config=None,
        host=None,
        token=None,
        verify_ssl=None,
        is_managed=None,
        authentication_type=None,
        api_version=None,
        reraise=False,
        schema_response=None,
        timeout=None,
    ):

        self._config = config or ClientConfig(
            host=host,
            token=token,
            authentication_type=authentication_type,
            version=api_version,
            verify_ssl=verify_ssl,
            is_managed=is_managed,
            schema_response=schema_response,
            reraise=reraise,
            timeout=timeout,
        )

        self._transport = None
        self.api_client = polyaxon_sdk.ApiClient(self.config.sdk_config)
        self._project_service = None
        self._run_service = None
        self._auth_service = None
        self._version_service = None
        self._user_service = None

    def reset(self):
        self._transport = None
        self._project_service = None
        self._run_service = None
        self._auth_service = None
        self._user_service = None
        self._version_service = None

    @property
    def host(self):
        return self.config.host

    @property
    def http_port(self):
        return self.config.http_port

    @property
    def ws_port(self):
        return self.config.ws_port

    @property
    def use_https(self):
        return self.config.use_https

    @property
    def verify_ssl(self):
        return self.config.verify_ssl

    @property
    def token(self):
        return self.config.token

    @property
    def authentication_type(self):
        return self.config.authentication_type

    @property
    def is_managed(self):
        return self.config.is_managed

    @property
    def api_version(self):
        return self.config.version

    @property
    def reraise(self):
        return self.config.reraise

    @property
    def timeout(self):
        return self.config.timeout

    def set_host(self, host):
        self.config.host = host
        self.reset()

    def set_http_port(self, http_port):
        self.config.http_port = http_port
        self.reset()

    def set_ws_port(self, ws_port):
        self.config.ws_port = ws_port
        self.reset()

    def set_use_https(self, use_https):
        self.config.use_https = use_https
        self.reset()

    def set_verify_ssl(self, verify_ssl):
        self.config.verify_ssl = verify_ssl
        self.reset()

    def set_token(self, token):
        self.config.token = token
        self.reset()

    def set_is_managed(self, is_managed):
        self.config.is_managed = is_managed
        self.reset()

    def set_authentication_type(self, authentication_type):
        self.config.authentication_type = authentication_type
        self.reset()

    def set_version_api(self, version_api):
        self.config.version = version_api
        self.reset()

    def set_reraise(self, reraise):
        self.config.reraise = reraise
        self.reset()

    def set_health_check(self, url):
        self.transport.set_health_check(url)

    def unset_health_check(self, url):
        self.transport.unset_health_check(url)

    def set_internal_health_check(self):
        if settings.HEALTH_CHECK_URL:
            self.set_health_check(
                self.auth.build_url(self.config.base_url, settings.HEALTH_CHECK_URL)
            )

    def reconcile(self, status):
        if settings.RECONCILE_URL:
            self.transport.post(
                url=self.auth.build_url(
                    self.config.base_url, settings.RECONCILE_URL
                ),
                json_data={
                    "status": status,
                    "created_at": str(utc.localize(datetime.utcnow())),
                },
            )

    @property
    def transport(self):
        if not self._transport:
            self._transport = Transport(config=self.config)
        return self._transport

    @property
    def config(self):
        return self._config

    @property
    def project_service(self):
        if not self._project_service:
            self._project_service = polyaxon_sdk.ProjectServiceApi(self.api_client)
        return self._project_service

    @property
    def run_service(self):
        if not self._run_service:
            self._run_service = polyaxon_sdk.RunServiceApi(self.api_client)
        return self._run_service

    @property
    def auth_service(self):
        if not self._auth_service:
            self._auth_service = polyaxon_sdk.AuthServiceApi(self.api_client)
        return self._auth_service

    @property
    def user_service(self):
        if not self._user_service:
            self._user_service = polyaxon_sdk.UserServiceApi(self.api_client)
        return self._user_service

    @property
    def version_service(self):
        if not self._version_service:
            self._version_service = polyaxon_sdk.VersionServiceApi(self.api_client)
        return self._version_service
