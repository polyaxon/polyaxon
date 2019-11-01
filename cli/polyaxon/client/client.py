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

from datetime import datetime

import polyaxon_sdk

from hestia.tz_utils import utc

from polyaxon import settings
from polyaxon.client.transport import Transport
from polyaxon.schemas.cli.client_configuration import ClientConfig


class PolyaxonClient(object):
    def __init__(self, config=None, token=None):

        self._config = config or ClientConfig.from_dict(
            settings.CLIENT_CONFIG.to_dict()
        )
        self._config.token = token or settings.AUTH_CONFIG.token

        self._transport = None
        self.api_client = polyaxon_sdk.ApiClient(
            self.config.sdk_config, **self.config.client_header
        )
        self._projects_v1 = None
        self._runs_v1 = None
        self._auth_v1 = None
        self._versions_v1 = None
        self._users_v1 = None

    def reset(self):
        self._transport = None
        self._projects_v1 = None
        self._runs_v1 = None
        self._auth_v1 = None
        self._users_v1 = None
        self._versions_v1 = None
        self.api_client = polyaxon_sdk.ApiClient(
            self.config.sdk_config, **self.config.client_header
        )

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
                url=self.auth.build_url(self.config.base_url, settings.RECONCILE_URL),
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
    def projects_v1(self):
        if not self._projects_v1:
            self._projects_v1 = polyaxon_sdk.ProjectsV1Api(self.api_client)
        return self._projects_v1

    @property
    def runs_v1(self):
        if not self._runs_v1:
            self._runs_v1 = polyaxon_sdk.RunsV1Api(self.api_client)
        return self._runs_v1

    @property
    def auth_v1(self):
        if not self._auth_v1:
            self._auth_v1 = polyaxon_sdk.AuthV1Api(self.api_client)
        return self._auth_v1

    @property
    def users_v1(self):
        if not self._users_v1:
            self._users_v1 = polyaxon_sdk.UsersV1Api(self.api_client)
        return self._users_v1

    @property
    def versions_v1(self):
        if not self._versions_v1:
            self._versions_v1 = polyaxon_sdk.VersionsV1Api(self.api_client)
        return self._versions_v1
