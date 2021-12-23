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
from polyaxon.constants.globals import NO_AUTH


class ApiClient(polyaxon_sdk.ApiClient):
    def call_api(
        self,
        resource_path,
        method,
        path_params=None,
        query_params=None,
        header_params=None,
        body=None,
        post_params=None,
        files=None,
        response_types_map=None,
        auth_settings=None,
        async_req=None,
        _return_http_data_only=None,
        collection_formats=None,
        _preload_content=True,
        _request_timeout=None,
        _host=None,
        _request_auth=None,
    ):
        if response_types_map and 200 in response_types_map:
            response_types_map[201] = response_types_map[200]
        return super().call_api(
            resource_path,
            method,
            path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
            post_params=post_params,
            files=files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            collection_formats=collection_formats,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            _host=_host,
            _request_auth=_request_auth,
        )


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
    ```
    """

    def __init__(self, config=None, token=None):

        self._config = config or settings.CLIENT_CONFIG
        token = token or self._config.token
        if not token:
            self._config.token = settings.AUTH_CONFIG.token
        elif token == NO_AUTH:
            self._config.token = None
        else:
            self._config.token = token

        self._transport = None
        self.api_client = ApiClient(self.config.sdk_config, **self.config.client_header)
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
        self.api_client = ApiClient(self.config.sdk_config, **self.config.client_header)

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
