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
from polyaxon.client import PolyaxonClient
from polyaxon.client.decorators import check_no_op, check_offline
from polyaxon.env_vars.getters import get_project_full_name, get_project_info
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.utils.query_params import get_query_params


class ProjectClient:
    @check_no_op
    def __init__(
        self, owner=None, project=None, client=None,
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

        self._owner = owner
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
        self._project_data = self.client.projects_v1.get_project(
            self.owner, self.project
        )

    @check_no_op
    @check_offline
    def create(self, data: polyaxon_sdk.V1Project()):
        self._project_data = self.client.projects_v1.create_project(self.owner, data)
        self._project = self._project_data.name
        return self._project_data

    @check_no_op
    @check_offline
    def list(
        self, query: str = None, sort: str = None, limit: int = None, offset: int = None
    ):
        params = get_query_params(limit=limit, offset=offset, query=query, sort=sort)
        return self.client.projects_v1.list_projects(self.owner, **params)

    @check_no_op
    @check_offline
    def delete(self):
        return self.client.projects_v1.delete_project(self.owner, self.project)

    @check_no_op
    @check_offline
    def update(self, data: polyaxon_sdk.V1Project()):
        return self.client.projects_v1.patch_project(
            self.owner, self.project, body=data
        )
