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
import logging

from requests import HTTPError
from typing import Dict, List, Union

import polyaxon_sdk

from polyaxon_sdk.rest import ApiException

from polyaxon.client.client import PolyaxonClient
from polyaxon.client.decorators import client_handler
from polyaxon.constants.globals import DEFAULT
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.lifecycle import V1ProjectVersionKind, V1StageCondition
from polyaxon.utils.fqn_utils import get_entity_full_name, get_entity_info
from polyaxon.utils.query_params import get_query_params
from polyaxon.utils.validation import validate_tags


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

    @client_handler(check_no_op=True)
    def __init__(
        self,
        owner: str = None,
        project: str = None,
        client: PolyaxonClient = None,
    ):
        if not owner and project:
            owner, project = get_entity_info(
                get_entity_full_name(owner=owner, entity=project)
            )

        if not owner:
            raise PolyaxonClientException("Please provide a valid owner.")

        self._client = client
        self._owner = owner or DEFAULT
        self._project = project
        self._project_data = polyaxon_sdk.V1Project()

    @property
    def client(self):
        if self._client:
            return self._client
        self._client = PolyaxonClient()
        return self._client

    @property
    def owner(self):
        return self._owner

    @property
    def project(self):
        return self._project

    @property
    def project_data(self):
        return self._project_data

    @client_handler(check_no_op=True, check_offline=True)
    def refresh_data(self):
        """Fetches the project data from the api."""
        self._project_data = self.client.projects_v1.get_project(
            self.owner, self.project
        )
        if self._project_data.owner is None:
            self._project_data.owner = self.owner

    @client_handler(check_no_op=True, check_offline=True)
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

    @client_handler(check_no_op=True, check_offline=True)
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

    @client_handler(check_no_op=True, check_offline=True)
    def delete(self):
        """Deletes project based on the current owner and project."""
        return self.client.projects_v1.delete_project(self.owner, self.project)

    @client_handler(check_no_op=True, check_offline=True)
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

    @client_handler(check_no_op=True, check_offline=True)
    def list_runs(
        self, query: str = None, sort: str = None, limit: int = None, offset: int = None
    ):
        """Lists runs under the current owner/project.

        [Run API](/docs/api/#operation/ListRuns)

        Args:
            query: str, optional, query filters, please refer to
                 [Run PQL](/docs/core/query-language/runs/#query)
            sort: str, optional, fields to order by, please refer to
                 [Run PQL](/docs/core/query-language/runs/#sort)
            limit: int, optional, limit of runs to return.
            offset: int, optional, offset pages to paginate runs.

        Returns:
            List[V1Run], list of run instances.
        """
        params = get_query_params(
            limit=limit or 20, offset=offset, query=query, sort=sort
        )
        return self.client.runs_v1.list_runs(self.owner, self.project, **params)

    @client_handler(check_no_op=True, check_offline=True)
    def list_versions(
        self,
        kind: V1ProjectVersionKind,
        query: str = None,
        sort: str = None,
        limit: int = None,
        offset: int = None,
    ):
        """Lists project versions under the current owner/project.

        [Project API](/docs/api/#operation/ListProjectVersions)

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            query: str, optional, query filters, please refer to
                 [Run PQL](/docs/core/query-language/runs/#query)
            sort: str, optional, fields to order by, please refer to
                 [Run PQL](/docs/core/query-language/runs/#sort)
            limit: int, optional, limit of runs to return.
            offset: int, optional, offset pages to paginate runs.

        Returns:
            List[V1ProjectVersion], list of versions.
        """
        params = get_query_params(
            limit=limit or 20, offset=offset, query=query, sort=sort
        )
        return self.client.projects_v1.list_versions(
            self.owner, self.project, kind, **params
        )

    @client_handler(check_no_op=True, check_offline=True)
    def get_version(self, kind: V1ProjectVersionKind, version: str):
        """Get a project version under the current owner/project.

        [Project API](/docs/api/#operation/GetVersion)

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            version: str, optional, the version name/tag.

        Returns:
            V1ProjectVersion.
        """
        response = self.client.projects_v1.get_version(
            self.owner, self.project, kind, version
        )
        if response.kind != kind:
            raise PolyaxonClientException("This version is not of kind `%s`." % kind)
        return response

    @client_handler(check_no_op=True, check_offline=True)
    def create_version(
        self,
        kind: V1ProjectVersionKind,
        data: Union[Dict, polyaxon_sdk.V1ProjectVersion],
    ):
        """Create a project version based on the data passed.

        [Project API](/docs/api/#operation/CreateVersion)

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            data: Dict or V1ProjectVersion, required.

        Returns:
            V1ProjectVersion.
        """
        if isinstance(data, polyaxon_sdk.V1ProjectVersion):
            data.kind = kind
        elif isinstance(data, dict):
            data["kind"] = kind
        return self.client.projects_v1.create_version(
            self.owner, self.project, kind, body=data
        )

    @client_handler(check_no_op=True, check_offline=True)
    def patch_version(
        self,
        kind: V1ProjectVersionKind,
        version: str,
        data: Union[Dict, polyaxon_sdk.V1ProjectVersion],
    ):
        """Update a project version based on the data passed.

        [Project API](/docs/api/#operation/PatchVersion)

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            version: str, optional, the version name/tag.
            data: Dict or V1ProjectVersion, required.

        Returns:
            V1ProjectVersion.
        """
        return self.client.projects_v1.patch_version(
            self.owner, self.project, kind, version, body=data
        )

    @client_handler(check_no_op=True, check_offline=True)
    def register_version(
        self,
        kind: V1ProjectVersionKind,
        version: str,
        description: str,
        tags: Union[str, List[str]] = None,
        content: str = None,
        run: str = None,
        connection: str = None,
        artifacts: List[str] = None,
        force: bool = False,
    ):
        """Create or Update a project version based on the data passed.

        [Project API](/docs/api/#operation/PatchVersion)

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            version: str, optional, the version name/tag.
            description: str, optional, the version description.
            tags: str or List[str], optional.
            content: str, optional, content of the version.
            run: str, optional, a uuid reference to the run.
            connection: str, optional, a uuid reference to a connection.
            artifacts: List[str], optional, list of artifacts to highlight(requires passing a run)
            force: bool, optional, to force push, i.e. update if exists.

        Returns:
            V1ProjectVersion.
        """
        try:
            self.get_version(kind, version)
            if not force:
                raise PolyaxonClientException(
                    "A {} version {} already exists. "
                    "Please pass the force (--force for CLI) flag "
                    "if you want to push force this version.".format(kind, version)
                )
            to_update = True
        except (ApiException, HTTPError, AttributeError):
            to_update = False

        if tags is not None:
            tags = validate_tags(tags)
        if artifacts is not None:
            artifacts = validate_tags(artifacts)

        if to_update:
            version_config = polyaxon_sdk.V1ProjectVersion()
            if description is not None:
                version_config.description = description
            if tags:
                version_config.tags = tags
            if content:
                version_config.content = content
            if run:
                version_config.run = run
            if artifacts is not None:
                version_config.artifacts = artifacts
            if connection is not None:
                version_config.connection = connection
            return self.patch_version(
                kind=kind,
                version=version,
                data=version_config,
            )
        else:
            version_config = polyaxon_sdk.V1ProjectVersion(
                name=version,
                description=description,
                tags=tags,
                run=run,
                artifacts=artifacts,
                connection=connection,
                content=content,
            )
            return self.create_version(kind=kind, data=version_config)

    @client_handler(check_no_op=True, check_offline=True)
    def delete_version(self, kind: V1ProjectVersionKind, version: str):
        """Delete a project version under the current owner/project.

        [Project API](/docs/api/#operation/DeleteVersion)

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            version: str, optional, the version name/tag.
        """
        logging.info("Deleting {} version: `{}`".format(kind, version))
        return self.client.projects_v1.delete_version(
            self.owner, self.project, kind, version
        )

    @client_handler(check_no_op=True, check_offline=True)
    def stage_project_version(
        self,
        kind: V1ProjectVersionKind,
        version: str,
        condition: Union[Dict, V1StageCondition],
    ):
        """Create a new a project version stage.

        [Project API](/docs/api/#operation/CreateVersionStage)

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            version: str, optional, the version name/tag.
            condition: Dict or V1StageCondition.
        """
        return self.client.projects_v1.create_version_stage(
            self.owner,
            self.project,
            kind,
            version,
            body={"condition": condition},
        )
