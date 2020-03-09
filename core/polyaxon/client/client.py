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

from polyaxon import settings
from polyaxon.client.transport import Transport


class PolyaxonClient:
    def __init__(self, config=None, token=None):

        self._config = config or settings.CLIENT_CONFIG
        self._config.token = token or settings.AUTH_CONFIG.token

        self._transport = None
        self.api_client = polyaxon_sdk.ApiClient(
            self.config.sdk_config, **self.config.client_header
        )
        self._projects_v1 = None
        self._runs_v1 = None
        self._auth_v1 = None
        self._users_v1 = None
        self._versions_v1 = None
        self._agents_v1 = None

    def reset(self):
        self._transport = None
        self._projects_v1 = None
        self._runs_v1 = None
        self._auth_v1 = None
        self._users_v1 = None
        self._versions_v1 = None
        self._agents_v1 = None
        self.api_client = polyaxon_sdk.ApiClient(
            self.config.sdk_config, **self.config.client_header
        )

    def set_health_check(self, url):
        self.transport.set_health_check(url)

    def unset_health_check(self, url):
        self.transport.unset_health_check(url)

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

    @property
    def agents_v1(self):
        if not self._agents_v1:
            self._agents_v1 = polyaxon_sdk.AgentsV1Api(self.api_client)
        return self._agents_v1

    def sanitize_for_serialization(self, value):
        return self.api_client.sanitize_for_serialization(value)
