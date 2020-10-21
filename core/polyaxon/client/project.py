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
from typing import Dict, Union

import polyaxon_sdk

from polyaxon import settings
from polyaxon.client import PolyaxonClient
from polyaxon.client.decorators import check_no_op, check_offline
from polyaxon.constants import DEFAULT
from polyaxon.env_vars.getters import get_project_full_name, get_project_info
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.utils.query_params import get_query_params


class ProjectClient:
    """ProjectClient is a client to communicate with Polyaxon projects endpoints.

    If no values are passed to this class,
    Polyaxon will try to resolve the owner and project from the environment:
        * If you have a configured CLI, Polyaxon will use the configuration of the cli.
        * If you have a cached project using the CLI,
        the client will default to that cached project unless you override the values.
        * If you use this client in the context of a job or a service managed by Polyaxon,
        a configuration will be available to resolve the values based on that run.

    If you intend to create a new project instance or to list projects,
    only the `owner` parameter is required.

    Properties:
        project: str.
        owner: str.
        project_data: V1Project.

    Args:
        owner: str, optional, the owner is the username or
               the organization name owning this project.
        project: str, optional, project name.
        client: [PolyaxonClient](/docs/core/python-library/polyaxon-client/), optional,
                an instance of a configured client, if not passed,
                a new instance will be created based on the available environment.

    Raises:
        PolyaxonClientException: If no owner is passed and Polyaxon cannot
            resolve an owner from the environment.
    """

    @check_no_op
    def __init__(
        self,
        owner: str = None,
        project: str = None,
        client: PolyaxonClient = None,
    ):
        if not owner and project:
            owner, project = get_project_info(
                get_project_full_name(owner=owner, project=project)
            )

        if not owner:
            raise PolyaxonClientException("Please provide a valid project owner.")

        self.client = client
        if not (self.client or settings.CLIENT_CONFIG.is_offline):
            self.client = PolyaxonClient()

        self._owner = owner or DEFAULT
        self._project = project
        self._project_data = polyaxon_sdk.V1Project()

    @property
    def owner(self):
        return self._owner

    @property
    def project(self):
        return self._project

    @property
    def project_data(self):
        return self._project_data

    @check_no_op
    @check_offline
    def refresh_data(self):
        """Fetches the project data from the api."""
        self._project_data = self.client.projects_v1.get_project(
            self.owner, self.project
        )
        if self._project_data.owner is None:
            self._project_data.owner = self.owner

    @check_no_op
    @check_offline
    def create(self, data: Union[Dict, polyaxon_sdk.V1Project]):
        """Creates a new project based on the data passed.

        [Project API](/docs/api/#operation/CreateProject)

        Args:
            data: dict or V1Project, required.

        Returns:
            V1Project, project instance from the response.
        """
        self._project_data = self.client.projects_v1.create_project(self.owner, data)
        self._project_data.owner = self.owner
        self._project = self._project_data.name
        return self._project_data

    @check_no_op
    @check_offline
    def list(
        self, query: str = None, sort: str = None, limit: int = None, offset: int = None
    ):
        """Lists projects under the current owner.

        [Project API](/docs/api/#operation/ListProjects)

        Args:
            query: str, optional, query filters, please refer to
                    [Project PQL](/docs/core/query-language/projects/#query)
            sort: str, optional, fields to order by, please refer to
                    [Project PQL](/docs/core/query-language/projects/#sort)
            limit: int, optional, limit of projects to return.
            offset: int, optional, offset pages to paginate projects.

        Returns:
            List[V1Project], list of project instances.
        """
        params = get_query_params(limit=limit, offset=offset, query=query, sort=sort)
        return self.client.projects_v1.list_projects(self.owner, **params)

    @check_no_op
    @check_offline
    def delete(self):
        """Deletes project based on the current owner and project."""
        return self.client.projects_v1.delete_project(self.owner, self.project)

    @check_no_op
    @check_offline
    def update(self, data: Union[Dict, polyaxon_sdk.V1Project]):
        """Updates a project based on the data passed.

        [Project API](/docs/api/#operation/PatchProject)

        Args:
            data: Dict or V1Project, required.

        Returns:
            V1Project, project instance from the response.
        """
        self._project_data = self.client.projects_v1.patch_project(
            self.owner, self.project, body=data
        )
        self._project = self._project_data.name
        return self._project_data
