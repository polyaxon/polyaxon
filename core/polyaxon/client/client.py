#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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
from polyaxon.constants import NO_AUTH


class PolyaxonClient:
    """Auto-configurable and high-level base client that abstract
    the need to set a configuration for each service.

    PolyaxonClient comes with logic
    to pass config and token to other specific clients.

    If no values are passed to this class,
    Polyaxon will try to resolve the configuration from the environment:
        * If you have a configured CLI, Polyaxon will use the configuration of the cli.
        * If you use this client in the context of a job or a service managed by Polyaxon,
        a configuration will be available.

    > N.B. PolyaxonClient requires python >= 3.5,
    if you want to interact with Polyaxon using a client
    compatible with python 2.7 please check polyaxon-sdk.

    Args:
        config: ClientConfig, optional, Instance of a ClientConfig.
        token: str, optional, the token to use for authenticating the clients,
               if the user is already logged in using the CLI, it will automatically use that token.
               Using the client inside a job/service scheduled with Polyaxon will have access to the
               token of the user who started the run if the `auth` context is enabled.

    You can access specific clients:

    ```python
    >>> client = PolyaxonClient()

    >>> client.projects_v1
    >>> client.runs_v1
    >>> client.auth_v1
    >>> client.users_v1
    >>> client.agents_v1
    >>> client.component_hub_v1
    >>> client.model_registry_v1
    ```
    """

    def __init__(self, config=None, token=None):

        self._config = config or settings.CLIENT_CONFIG
        if not token:
            self._config.token = settings.AUTH_CONFIG.token
        elif token != NO_AUTH:
            self._config.token = token

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
        self._component_hub_v1 = None
        self._model_registry_v1 = None

    def reset(self):
        self._transport = None
        self._projects_v1 = None
        self._runs_v1 = None
        self._auth_v1 = None
        self._users_v1 = None
        self._versions_v1 = None
        self._agents_v1 = None
        self._component_hub_v1 = None
        self._model_registry_v1 = None
        self.api_client = polyaxon_sdk.ApiClient(
            self.config.sdk_config, **self.config.client_header
        )

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

    @property
    def component_hub_v1(self):
        if not self._component_hub_v1:
            self._component_hub_v1 = polyaxon_sdk.ComponentHubV1Api(self.api_client)
        return self._component_hub_v1

    @property
    def model_registry_v1(self):
        if not self._model_registry_v1:
            self._model_registry_v1 = polyaxon_sdk.ModelRegistryV1Api(self.api_client)
        return self._model_registry_v1

    def sanitize_for_serialization(self, value):
        return self.api_client.sanitize_for_serialization(value)
