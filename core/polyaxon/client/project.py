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
import os

from requests import HTTPError
from typing import Dict, List, Union

import ujson

import polyaxon_sdk

from polyaxon.client.client import PolyaxonClient
from polyaxon.client.decorators import client_handler
from polyaxon.constants.globals import DEFAULT
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.lifecycle import V1ProjectVersionKind, V1StageCondition
from polyaxon.logger import logger
from polyaxon.utils.fqn_utils import get_entity_full_name, get_entity_info
from polyaxon.utils.path_utils import check_or_create_path, delete_path
from polyaxon.utils.query_params import get_query_params
from polyaxon.utils.validation import validate_tags
from polyaxon_sdk.rest import ApiException


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
    def create(
        self, data: Union[Dict, polyaxon_sdk.V1Project]
    ) -> polyaxon_sdk.V1Project:
        """Creates a new project based on the data passed.

        [Project API](/docs/api/#operation/CreateProject)

        Args:
            data: dict or V1Project, required.

        Returns:
            V1Project, project instance from the response.
        """
        self._project_data = self.client.projects_v1.create_project(
            self.owner,
            data,
            async_req=False,
        )
        self._project_data.owner = self.owner
        self._project = self._project_data.name
        return self._project_data

    @client_handler(check_no_op=True, check_offline=True)
    def list(
        self, query: str = None, sort: str = None, limit: int = None, offset: int = None
    ) -> List[polyaxon_sdk.V1Project]:
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
    def update(
        self, data: Union[Dict, polyaxon_sdk.V1Project]
    ) -> polyaxon_sdk.V1Project:
        """Updates a project based on the data passed.

        [Project API](/docs/api/#operation/PatchProject)

        Args:
            data: Dict or V1Project, required.

        Returns:
            V1Project, project instance from the response.
        """
        self._project_data = self.client.projects_v1.patch_project(
            self.owner,
            self.project,
            body=data,
            async_req=False,
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

    def _validate_kind(self, kind: V1ProjectVersionKind):
        if kind not in V1ProjectVersionKind.allowable_values:
            raise ValueError(
                "The kind `{}` is not supported, it must be one of the values `{}`".format(
                    kind, V1ProjectVersionKind.allowable_values
                )
            )

    @client_handler(check_no_op=True, check_offline=True)
    def list_versions(
        self,
        kind: V1ProjectVersionKind,
        query: str = None,
        sort: str = None,
        limit: int = None,
        offset: int = None,
    ) -> polyaxon_sdk.V1ListProjectVersionsResponse:
        """Lists project versions under the current owner/project based on version kind.

        This is a generic function that maps to list:
            * component versions
            * model versions
            * artifact versions

        [Project API](/docs/api/#operation/ListProjectVersions)

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            query: str, optional, query filters, please refer to
                 [Run PQL](/docs/core/query-language/project-versions/#query)
            sort: str, optional, fields to order by, please refer to
                 [Run PQL](/docs/core/query-language/project-versions/#sort)
            limit: int, optional, limit of project versions to return.
            offset: int, optional, offset pages to paginate project versions.

        Returns:
            List[V1ProjectVersion], list of versions.
        """
        self._validate_kind(kind)
        params = get_query_params(
            limit=limit or 20, offset=offset, query=query, sort=sort
        )
        return self.client.projects_v1.list_versions(
            self.owner, self.project, kind, **params
        )

    @client_handler(check_no_op=True, check_offline=True)
    def list_component_versions(
        self,
        query: str = None,
        sort: str = None,
        limit: int = None,
        offset: int = None,
    ) -> polyaxon_sdk.V1ListProjectVersionsResponse:
        """Lists component versions under the current owner/project.

        [Project API](/docs/api/#operation/ListProjectVersions)

        Args:
            query: str, optional, query filters, please refer to
                 [Run PQL](/docs/core/query-language/project-versions/#query)
            sort: str, optional, fields to order by, please refer to
                 [Run PQL](/docs/core/query-language/project-versions/#sort)
            limit: int, optional, limit of project versions to return.
            offset: int, optional, offset pages to paginate project versions.

        Returns:
            List[V1ProjectVersion], list of component versions.
        """
        return self.list_versions(
            kind=V1ProjectVersionKind.COMPONENT,
            query=query,
            sort=sort,
            limit=limit,
            offset=offset,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def list_model_versions(
        self,
        query: str = None,
        sort: str = None,
        limit: int = None,
        offset: int = None,
    ) -> polyaxon_sdk.V1ListProjectVersionsResponse:
        """Lists model versions under the current owner/project.

        [Project API](/docs/api/#operation/ListProjectVersions)

        Args:
            query: str, optional, query filters, please refer to
                 [Run PQL](/docs/core/query-language/project-versions/#query)
            sort: str, optional, fields to order by, please refer to
                 [Run PQL](/docs/core/query-language/project-versions/#sort)
            limit: int, optional, limit of project versions to return.
            offset: int, optional, offset pages to paginate project versions.

        Returns:
            List[V1ProjectVersion], list of model versions.
        """
        return self.list_versions(
            kind=V1ProjectVersionKind.MODEL,
            query=query,
            sort=sort,
            limit=limit,
            offset=offset,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def list_artifact_versions(
        self,
        query: str = None,
        sort: str = None,
        limit: int = None,
        offset: int = None,
    ) -> polyaxon_sdk.V1ListProjectVersionsResponse:
        """Lists artifact versions under the current owner/project.

        [Project API](/docs/api/#operation/ListProjectVersions)

        Args:
            query: str, optional, query filters, please refer to
                 [Run PQL](/docs/core/query-language/project-versions/#query)
            sort: str, optional, fields to order by, please refer to
                 [Run PQL](/docs/core/query-language/project-versions/#sort)
            limit: int, optional, limit of project versions to return.
            offset: int, optional, offset pages to paginate project versions.

        Returns:
            List[V1ProjectVersion], list of artifact versions.
        """
        return self.list_versions(
            kind=V1ProjectVersionKind.ARTIFACT,
            query=query,
            sort=sort,
            limit=limit,
            offset=offset,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def get_version(
        self, kind: V1ProjectVersionKind, version: str
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Gets a project version under the current owner/project based on version kind.

        This is a generic function that maps to get:
            * component version
            * model version
            * artifact version

        [Project API](/docs/api/#operation/GetVersion)

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            version: str, required, the version name/tag.

        Returns:
            V1ProjectVersion.
        """
        self._validate_kind(kind)
        response = self.client.projects_v1.get_version(
            self.owner, self.project, kind, version
        )
        if response.kind != kind:
            raise PolyaxonClientException("This version is not of kind `%s`." % kind)
        return response

    @client_handler(check_no_op=True, check_offline=True)
    def get_component_version(self, version: str) -> polyaxon_sdk.V1ProjectVersion:
        """Gets a component version under the current owner/project.

        [Project API](/docs/api/#operation/GetVersion)

        Args:
            version: str, required, the version name/tag.

        Returns:
            V1ProjectVersion, component version.
        """
        return self.get_version(kind=V1ProjectVersionKind.COMPONENT, version=version)

    @client_handler(check_no_op=True, check_offline=True)
    def get_model_version(self, version: str) -> polyaxon_sdk.V1ProjectVersion:
        """Gets a model version under the current owner/project.

        [Project API](/docs/api/#operation/GetVersion)

        Args:
            version: str, required, the version name/tag.

        Returns:
            V1ProjectVersion, model version.
        """
        return self.get_version(kind=V1ProjectVersionKind.MODEL, version=version)

    @client_handler(check_no_op=True, check_offline=True)
    def get_artifact_version(self, version: str) -> polyaxon_sdk.V1ProjectVersion:
        """Gets an artifact version under the current owner/project.

        [Project API](/docs/api/#operation/GetVersion)

        Args:
            version: str, required, the version name/tag.

        Returns:
            V1ProjectVersion, artifact version.
        """
        return self.get_version(kind=V1ProjectVersionKind.ARTIFACT, version=version)

    @client_handler(check_no_op=True, check_offline=True)
    def create_version(
        self,
        kind: V1ProjectVersionKind,
        data: Union[Dict, polyaxon_sdk.V1ProjectVersion],
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Creates a project version based on the data passed based on version kind.

        This is a generic function based on the kind passed and creates a:
            * component version
            * model version
            * artifact version

        [Project API](/docs/api/#operation/CreateVersion)

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            data: Dict or V1ProjectVersion, required.

        Returns:
            V1ProjectVersion.
        """
        self._validate_kind(kind)
        if isinstance(data, polyaxon_sdk.V1ProjectVersion):
            data.kind = kind
        elif isinstance(data, dict):
            data["kind"] = kind
        return self.client.projects_v1.create_version(
            self.owner,
            self.project,
            kind,
            body=data,
            async_req=False,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def create_component_version(
        self,
        data: Union[Dict, polyaxon_sdk.V1ProjectVersion],
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Creates a component version based on the data passed.

        [Project API](/docs/api/#operation/CreateVersion)

        Args:
            data: Dict or V1ProjectVersion, required.

        Returns:
            V1ProjectVersion, component version.
        """
        return self.create_version(
            kind=V1ProjectVersionKind.COMPONENT,
            data=data,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def create_model_version(
        self,
        data: Union[Dict, polyaxon_sdk.V1ProjectVersion],
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Creates a model version based on the data passed.

        [Project API](/docs/api/#operation/CreateVersion)

        Args:
            data: Dict or V1ProjectVersion, required.

        Returns:
            V1ProjectVersion, model version.
        """
        return self.create_version(
            kind=V1ProjectVersionKind.MODEL,
            data=data,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def create_artifact_version(
        self,
        data: Union[Dict, polyaxon_sdk.V1ProjectVersion],
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Creates an artifact version based on the data passed.

        [Project API](/docs/api/#operation/CreateVersion)

        Args:
            data: Dict or V1ProjectVersion, required.

        Returns:
            V1ProjectVersion, artifact version.
        """
        return self.create_version(
            kind=V1ProjectVersionKind.ARTIFACT,
            data=data,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def patch_version(
        self,
        kind: V1ProjectVersionKind,
        version: str,
        data: Union[Dict, polyaxon_sdk.V1ProjectVersion],
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Updates a project version based on the data passed and version kind.

        This is a generic function based on the kind passed and patches a:
            * component version
            * model version
            * artifact version

        [Project API](/docs/api/#operation/PatchVersion)

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            version: str, required, the version name/tag.
            data: Dict or V1ProjectVersion, required.

        Returns:
            V1ProjectVersion.
        """
        self._validate_kind(kind)
        return self.client.projects_v1.patch_version(
            self.owner,
            self.project,
            kind,
            version,
            body=data,
            async_req=False,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def patch_component_version(
        self,
        version: str,
        data: Union[Dict, polyaxon_sdk.V1ProjectVersion],
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Updates a component version based on the data passed.

        [Project API](/docs/api/#operation/PatchVersion)

        Args:
            version: str, required, the version name/tag.
            data: Dict or V1ProjectVersion, required.

        Returns:
            V1ProjectVersion, component version.
        """
        return self.patch_version(
            kind=V1ProjectVersionKind.COMPONENT,
            version=version,
            data=data,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def patch_model_version(
        self,
        version: str,
        data: Union[Dict, polyaxon_sdk.V1ProjectVersion],
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Updates a model version based on the data passed.

        [Project API](/docs/api/#operation/PatchVersion)

        Args:
            version: str, required, the version name/tag.
            data: Dict or V1ProjectVersion, required.

        Returns:
            V1ProjectVersion, model version.
        """
        return self.patch_version(
            kind=V1ProjectVersionKind.MODEL,
            version=version,
            data=data,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def patch_artifact_version(
        self,
        version: str,
        data: Union[Dict, polyaxon_sdk.V1ProjectVersion],
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Updates an artifact version based on the data passed.

        [Project API](/docs/api/#operation/PatchVersion)

        Args:
            version: str, required, the version name/tag.
            data: Dict or V1ProjectVersion, required.

        Returns:
            V1ProjectVersion, artifact version.
        """
        return self.patch_version(
            kind=V1ProjectVersionKind.ARTIFACT,
            version=version,
            data=data,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def register_version(
        self,
        kind: V1ProjectVersionKind,
        version: str,
        description: str = None,
        tags: Union[str, List[str]] = None,
        content: str = None,
        run: str = None,
        connection: str = None,
        artifacts: List[str] = None,
        force: bool = False,
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Creates or Updates a project version based on the data passed.

        This is a generic function based on the kind passed and registers a:
            * component version
            * model version
            * artifact version

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            version: str, optional, the version name/tag.
            description: str, optional, the version description.
            tags: str or List[str], optional.
            content: str, optional, content/metadata (JSON object) of the version.
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
            tags = validate_tags(tags, validate_yaml=True)
        if artifacts is not None:
            artifacts = validate_tags(artifacts, validate_yaml=True)

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
    def register_component_version(
        self,
        version: str,
        description: str = None,
        tags: Union[str, List[str]] = None,
        content: str = None,
        run: str = None,
        force: bool = False,
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Creates or Updates a component version based on the data passed.

        Args:
            version: str, optional, the version name/tag.
            description: str, optional, the version description.
            tags: str or List[str], optional.
            content: str, optional, content/metadata (JSON object) of the version.
            run: str, optional, a uuid reference to the run.
            force: bool, optional, to force push, i.e. update if exists.

        Returns:
            V1ProjectVersion, component verison.
        """
        return self.register_version(
            kind=V1ProjectVersionKind.COMPONENT,
            version=version,
            description=description,
            tags=tags,
            content=content,
            run=run,
            force=force,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def register_model_version(
        self,
        version: str,
        description: str = None,
        tags: Union[str, List[str]] = None,
        content: str = None,
        run: str = None,
        connection: str = None,
        artifacts: List[str] = None,
        force: bool = False,
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Create or Update a model version based on the data passed.

        Args:
            version: str, optional, the version name/tag.
            description: str, optional, the version description.
            tags: str or List[str], optional.
            content: str, optional, content/metadata (JSON object) of the version.
            run: str, optional, a uuid reference to the run.
            connection: str, optional, a uuid reference to a connection.
            artifacts: List[str], optional, list of artifacts to highlight(requires passing a run)
            force: bool, optional, to force push, i.e. update if exists.

        Returns:
            V1ProjectVersion, model version.
        """
        return self.register_version(
            kind=V1ProjectVersionKind.MODEL,
            version=version,
            description=description,
            tags=tags,
            content=content,
            run=run,
            connection=connection,
            artifacts=artifacts,
            force=force,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def register_artifact_version(
        self,
        version: str,
        description: str = None,
        tags: Union[str, List[str]] = None,
        content: str = None,
        run: str = None,
        connection: str = None,
        artifacts: List[str] = None,
        force: bool = False,
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Create or Update an artifact version based on the data passed.

        Args:
            version: str, optional, the version name/tag.
            description: str, optional, the version description.
            tags: str or List[str], optional.
            content: str, optional, content/metadata (JSON object) of the version.
            run: str, optional, a uuid reference to the run.
            connection: str, optional, a uuid reference to a connection.
            artifacts: List[str], optional, list of artifacts to highlight(requires passing a run)
            force: bool, optional, to force push, i.e. update if exists.

        Returns:
            V1ProjectVersion, artifact version.
        """
        return self.register_version(
            kind=V1ProjectVersionKind.ARTIFACT,
            version=version,
            description=description,
            tags=tags,
            content=content,
            run=run,
            connection=connection,
            artifacts=artifacts,
            force=force,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def delete_version(self, kind: V1ProjectVersionKind, version: str):
        """Deletes a project version under the current owner/project.

        This is a generic function based on the kind passed and deletes a:
            * component version
            * model version
            * artifact version

        [Project API](/docs/api/#operation/DeleteVersion)

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            version: str, required, the version name/tag.
        """
        self._validate_kind(kind)
        logger.info("Deleting {} version: `{}`".format(kind, version))
        return self.client.projects_v1.delete_version(
            self.owner,
            self.project,
            kind,
            version,
            async_req=False,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def delete_component_version(self, version: str):
        """Deletes a component version under the current owner/project.

        [Project API](/docs/api/#operation/DeleteVersion)

        Args:
            version: str, required, the version name/tag.
        """
        return self.delete_version(
            kind=V1ProjectVersionKind.COMPONENT,
            version=version,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def delete_model_version(self, version: str):
        """Deletes a model version under the current owner/project.

        [Project API](/docs/api/#operation/DeleteVersion)

        Args:
            version: str, required, the version name/tag.
        """
        return self.delete_version(
            kind=V1ProjectVersionKind.MODEL,
            version=version,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def delete_artifact_version(self, version: str):
        """Deletes an artifact version under the current owner/project.

        [Project API](/docs/api/#operation/DeleteVersion)

        Args:
            version: str, required, the version name/tag.
        """
        return self.delete_version(
            kind=V1ProjectVersionKind.ARTIFACT,
            version=version,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def stage_version(
        self,
        kind: V1ProjectVersionKind,
        version: str,
        condition: Union[Dict, V1StageCondition],
    ):
        """Creates a new a project version stage.


        This is a generic function based on the kind passed and stages a:
            * component version
            * model version
            * artifact version

        [Project API](/docs/api/#operation/CreateVersionStage)

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            version: str, required, the version name/tag.
            condition: Dict or V1StageCondition.
        """
        self._validate_kind(kind)
        return self.client.projects_v1.create_version_stage(
            self.owner,
            self.project,
            kind,
            version,
            body={"condition": condition},
            async_req=False,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def stage_component_version(
        self,
        version: str,
        condition: Union[Dict, V1StageCondition],
    ):
        """Creates a new a component version stage.

        [Project API](/docs/api/#operation/CreateVersionStage)

        Args:
            version: str, required, the version name/tag.
            condition: Dict or V1StageCondition.
        """
        return self.stage_version(
            kind=V1ProjectVersionKind.COMPONENT,
            version=version,
            condition=condition,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def stage_model_version(
        self,
        version: str,
        condition: Union[Dict, V1StageCondition],
    ):
        """Creates a new a model version stage.

        [Project API](/docs/api/#operation/CreateVersionStage)

        Args:
            version: str, required, the version name/tag.
            condition: Dict or V1StageCondition.
        """
        return self.stage_version(
            kind=V1ProjectVersionKind.MODEL,
            version=version,
            condition=condition,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def stage_artifact_version(
        self,
        version: str,
        condition: Union[Dict, V1StageCondition],
    ):
        """Creates a new an artifact version stage.

        [Project API](/docs/api/#operation/CreateVersionStage)

        Args:
            version: str, required, the version name/tag.
            condition: Dict or V1StageCondition.
        """
        return self.stage_version(
            kind=V1ProjectVersionKind.ARTIFACT,
            version=version,
            condition=condition,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def transfer_version(
        self, kind: V1ProjectVersionKind, version: str, to_project: str
    ):
        """Transfers the version to a project under the same owner/organization.

        This is a generic function based on the kind passed and transfers a:
            * component version
            * model version
            * artifact version

        [Run API](/docs/api/#operation/TransferVersion)

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            version: str, required, the version name/tag.
            to_project: str, required, the destination project to transfer the version to.
        """

        self._validate_kind(kind)
        return self.client.projects_v1.transfer_version(
            self.owner,
            self.project,
            kind,
            version,
            body={"project": to_project},
            async_req=False,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def transfer_component_version(self, version: str, to_project: str):
        """Transfers the component version to a project under the same owner/organization.

        [Run API](/docs/api/#operation/TransferVersion)

        Args:
            version: str, required, the version name/tag.
            to_project: str, required, the destination project to transfer the version to.
        """
        return self.transfer_version(
            kind=V1ProjectVersionKind.COMPONENT,
            version=version,
            to_project=to_project,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def transfer_model_version(self, version: str, to_project: str):
        """Transfers the model version to a project under the same owner/organization.

        [Run API](/docs/api/#operation/TransferVersion)

        Args:
            version: str, required, the version name/tag.
            to_project: str, required, the destination project to transfer the version to.
        """
        return self.transfer_version(
            kind=V1ProjectVersionKind.MODEL,
            version=version,
            to_project=to_project,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def transfer_artifact_version(self, version: str, to_project: str):
        """Transfers the artifact version to a project under the same owner/organization.

        [Run API](/docs/api/#operation/TransferVersion)

        Args:
            version: str, required, the version name/tag.
            to_project: str, required, the destination project to transfer the version to.
        """
        return self.transfer_version(
            kind=V1ProjectVersionKind.ARTIFACT,
            version=version,
            to_project=to_project,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def copy_version(
        self,
        kind: V1ProjectVersionKind,
        version: str,
        to_project: str = None,
        name: str = None,
        description: str = None,
        tags: Union[str, List[str]] = None,
        content: str = None,
        force: bool = False,
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Copies the version to the same project or to a destination project.

        If `to_project` is provided,
        the version will be copied to the destination project under the same owner/organization.

        If `name` is provided the version will be copied with the new name,
        otherwise the copied version will be have a suffix `-copy`.

        This is a generic function based on the kind passed and copies a:
            * component version
            * model version
            * artifact version

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            version: str, required, the version name/tag.
            to_project: str, optional, the destination project to copy the version to.
            name: str, optional, the name to use for registering the copied version,
                 default value is the original version's name with `-copy` prefix.
            description: str, optional, the version description,
                 default value is the original version's description.
            tags: str or List[str], optional, the version description,
                 default value is the original version's description.
            content: str, optional, content/metadata (JSON object) of the version,
                 default value is the original version's content.
            force: bool, optional, to force push, i.e. update if exists.
        """
        original_version = self.get_version(kind, version)
        version = name if name else "{}-copy".format(version)
        return ProjectClient(
            owner=self.owner,
            project=to_project or self.project,
            client=self.client,
        ).register_version(
            kind=kind,
            version=version,
            description=description or original_version.description,
            tags=tags or original_version.tags,
            content=content or original_version.content,
            run=original_version.run,
            connection=original_version.connection,
            artifacts=original_version.artifacts,
            force=force,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def copy_component_version(
        self,
        version: str,
        to_project: str = None,
        name: str = None,
        description: str = None,
        tags: Union[str, List[str]] = None,
        content: str = None,
        force: bool = False,
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Copies the component version to the same project or to a destination project.

        If `to_project` is provided,
        the version will be copied to the destination project under the same owner/organization.

        If `name` is provided the version will be copied with the new name,
        otherwise the copied version will be have a suffix `-copy`.

        Args:
            version: str, required, the version name/tag.
            to_project: str, optional, the destination project to copy the version to.
            name: str, optional, the name to use for registering the copied version,
                 default value is the original version's name with `-copy` prefix.
            description: str, optional, the version description,
                 default value is the original version's description.
            tags: str or List[str], optional, the version description,
                 default value is the original version's description.
            content: str, optional, content/metadata (JSON object) of the version,
                 default value is the original version's content.
            force: bool, optional, to force push, i.e. update if exists.
        """
        return self.copy_version(
            kind=V1ProjectVersionKind.COMPONENT,
            version=version,
            to_project=to_project,
            name=name,
            description=description,
            tags=tags,
            content=content,
            force=force,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def copy_model_version(
        self,
        version: str,
        to_project: str = None,
        name: str = None,
        description: str = None,
        tags: Union[str, List[str]] = None,
        content: str = None,
        force: bool = False,
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Copies the model version to the same project or to a destination project.

        If `to_project` is provided,
        the version will be copied to the destination project under the same owner/organization.

        If `name` is provided the version will be copied with the new name,
        otherwise the copied version will be have a suffix `-copy`.

        Args:
            version: str, required, the version name/tag.
            to_project: str, optional, the destination project to copy the version to.
            name: str, optional, the name to use for registering the copied version,
                 default value is the original version's name with `-copy` prefix.
            description: str, optional, the version description,
                 default value is the original version's description.
            tags: str or List[str], optional, the version description,
                 default value is the original version's description.
            content: str, optional, content/metadata (JSON object) of the version,
                 default value is the original version's content.
            force: bool, optional, to force push, i.e. update if exists.
        """
        return self.copy_version(
            kind=V1ProjectVersionKind.MODEL,
            version=version,
            to_project=to_project,
            name=name,
            description=description,
            tags=tags,
            content=content,
            force=force,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def copy_artifact_version(
        self,
        version: str,
        to_project: str = None,
        name: str = None,
        description: str = None,
        tags: Union[str, List[str]] = None,
        content: str = None,
        force: bool = False,
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Copies the artifact version to the same project or to a destination project.

        If `to_project` is provided,
        the version will be copied to the destination project under the same owner/organization.

        If `name` is provided the version will be copied with the new name,
        otherwise the copied version will be have a suffix `-copy`.

        Args:
            version: str, required, the version name/tag.
            to_project: str, optional, the destination project to copy the version to.
            name: str, optional, the name to use for registering the copied version,
                 default value is the original version's name with `-copy` prefix.
            description: str, optional, the version description,
                 default value is the original version's description.
            tags: str or List[str], optional, the version description,
                 default value is the original version's description.
            content: str, optional, content/metadata (JSON object) of the version,
                 default value is the original version's content.
            force: bool, optional, to force push, i.e. update if exists.
        """
        return self.copy_version(
            kind=V1ProjectVersionKind.ARTIFACT,
            version=version,
            to_project=to_project,
            name=name,
            description=description,
            tags=tags,
            content=content,
            force=force,
        )

    @client_handler(check_no_op=True)
    def persist_version(self, config: polyaxon_sdk.V1ProjectVersion, path: str):
        """Persists a version to a local path.

        Args:
            config: V1ProjectVersion, the version config to persist.
            path: str, the path where to persist the version config.
        """
        if not config:
            logger.debug(
                "Persist offline run call failed. "
                "Make sure that the offline mode is enabled and that run_data is provided."
            )
            return
        if not path or not os.path.exists(path):
            check_or_create_path(path, is_dir=True)
        version_path = "{}/version_data.json".format(path)
        with open(version_path, "w") as config_file:
            config_file.write(
                ujson.dumps(self.client.sanitize_for_serialization(config))
            )
        if not config.content:
            return
        if config.kind == V1ProjectVersionKind.COMPONENT:
            version_path = "{}/polyaxonfile.json".format(path)
        else:
            # Persist content metadata as content.json file
            version_path = "{}/content.json".format(path)
        with open(version_path, "w") as config_file:
            config_file.write(config.content)

    @client_handler(check_no_op=True, check_offline=True)
    def download_artifacts_for_version(
        self, config: polyaxon_sdk.V1ProjectVersion, path: str
    ):
        """Collects and downloads all artifacts and assets linked to a version.

        Args:
            config: V1ProjectVersion, the version config to download the artifacts for.
            path: str, the path where to persist the artifacts and assets.
        """
        if config.kind not in {
            V1ProjectVersionKind.MODEL,
            V1ProjectVersionKind.ARTIFACT,
        }:
            logger.info(
                "Skip artifacts download for version {} with kind {}.".format(
                    config.name, config.kind
                )
            )
            return

        meta_info = config.meta_info or {}
        run_info = meta_info.get("run", {})
        if not run_info:
            logger.info(
                "Skip artifacts download for version {} with kind {}. "
                "The version is not linked to any run.".format(config.name, config.kind)
            )
            return

        run_artifacts = [
            polyaxon_sdk.V1RunArtifact(**a) for a in meta_info.get("artifacts", [])
        ]
        if not run_artifacts:
            logger.info(
                "Skip artifacts download for version {} with kind {}. "
                "The version is not linked to any artifacts.".format(
                    config.name, config.kind
                )
            )
            return

        run_project = run_info.get("project", self.project)
        run_uuid = run_info.get("uuid", config.run)

        from polyaxon.client.run import RunClient

        # Creating run client to download artifacts
        run_client = RunClient(owner=self.owner, project=run_project, run_uuid=run_uuid)
        for artifact_lineage in run_artifacts:
            logger.info(
                "Downloading artifact {} with kind {} and remote path {} to {}.".format(
                    artifact_lineage.name,
                    artifact_lineage.kind,
                    artifact_lineage.path,
                    path,
                )
            )
            run_client.download_artifact_for_lineage(
                lineage=artifact_lineage, path_to=path
            )

    @client_handler(check_no_op=True, check_offline=True)
    def pull_version(
        self,
        kind: V1ProjectVersionKind,
        version: str,
        path: str,
        download_artifacts: bool = True,
    ):
        """Packages and downloads the version to a local path.

        This is a generic function based on the kind passed and pulls a:
            * component version
            * model version
            * artifact version

        Args:
            kind: V1ProjectVersionKind, kind of the project version.
            version: str, required, the version name/tag.
            path: str, local path where to persist the metadata and artifacts.
            download_artifacts: bool, optional, to download the artifacts based on linked lineage.
        """
        delete_path(path)
        config = self.get_version(kind=kind, version=version)
        self.persist_version(config=config, path=path)
        if download_artifacts:
            self.download_artifacts_for_version(config=config, path=path)

    @client_handler(check_no_op=True, check_offline=True)
    def pull_component_version(
        self,
        version: str,
        path: str,
    ):
        """Packages and downloads the component version to a local path.

        Args:
            version: str, required, the version name/tag.
            path: str, local path where to persist the metadata and artifacts.
        """
        return self.pull_version(
            kind=V1ProjectVersionKind.COMPONENT,
            version=version,
            path=path,
            download_artifacts=False,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def pull_model_version(
        self,
        version: str,
        path: str,
        download_artifacts: bool = True,
    ):
        """Packages and downloads the model version to a local path.

        Args:
            version: str, required, the version name/tag.
            path: str, local path where to persist the metadata and artifacts.
            download_artifacts: bool, optional, to download the artifacts based on linked lineage.
        """
        return self.pull_version(
            kind=V1ProjectVersionKind.MODEL,
            version=version,
            path=path,
            download_artifacts=download_artifacts,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def pull_artifact_version(
        self,
        version: str,
        path: str,
        download_artifacts: bool = True,
    ):
        """Packages and downloads the artifact version to a local path.

        Args:
            version: str, required, the version name/tag.
            path: str, local path where to persist the metadata and artifacts.
            download_artifacts: bool, optional, to download the artifacts based on linked lineage.
        """
        return self.pull_version(
            kind=V1ProjectVersionKind.ARTIFACT,
            version=version,
            path=path,
            download_artifacts=download_artifacts,
        )
