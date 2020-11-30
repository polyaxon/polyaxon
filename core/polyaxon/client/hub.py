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
from polyaxon.client.client import PolyaxonClient
from polyaxon.client.decorators import check_no_op, check_offline
from polyaxon.constants import DEFAULT
from polyaxon.env_vars.getters import get_entity_info, get_entity_full_name
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.utils.query_params import get_query_params


class HubClient:
    """HubClient is a client to communicate with Polyaxon component hub endpoints.

    If no values are passed to this class,
    Polyaxon will try to resolve the owner and hub from the environment:
        * If you have a configured CLI, Polyaxon will use the configuration of the cli.
        * If you have a cached owner using the CLI,
        the client will default to that cached owner unless you override the values.

    If you intend to create a new component hub instance or to list components,
    only the `owner` parameter is required.

    Properties:
        hub: str.
        owner: str.
        hub_data: V1ComponentHub.
        hub_version: V1ComponentVersion.

    Args:
        owner: str, optional, the owner is the username or
               the organization name owning this hub.
        hub: str, optional, hub name.
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
        hub: str = None,
        client: PolyaxonClient = None,
    ):
        if not owner and hub:
            owner, hub = get_entity_info(
                get_entity_full_name(owner=owner, entity=hub)
            )

        if not owner:
            raise PolyaxonClientException("Please provide a valid owner.")

        self.client = client
        if not (self.client or settings.CLIENT_CONFIG.is_offline):
            self.client = PolyaxonClient()

        self._owner = owner or DEFAULT
        self._hub = hub
        self._hub_data = polyaxon_sdk.V1ComponentHub()

    @property
    def owner(self):
        return self._owner

    @property
    def hub(self):
        return self._hub

    @property
    def hub_data(self):
        return self._hub_data

    @check_no_op
    @check_offline
    def refresh_data(self):
        """Fetches the hub data from the api."""
        self._hub_data = self.client.component_hub_v1.get_component_hub(
            self.owner, self.hub
        )
        if self._hub_data.owner is None:
            self._hub_data.owner = self.owner

    @check_no_op
    @check_offline
    def create(self, data: Union[Dict, polyaxon_sdk.V1ComponentHub]):
        """Creates a new component hub based on the data passed.

        Args:
            data: dict or V1ComponentHub, required.

        Returns:
            V1ComponentHub, entity instance from the response.
        """
        self._hub_data = self.client.component_hub_v1.create_component_hub(self.owner, data)
        self._hub_data.owner = self.owner
        self._hub = self._hub_data.name
        return self._hub_data

    @check_no_op
    @check_offline
    def list(
        self, query: str = None, sort: str = None, limit: int = None, offset: int = None
    ):
        """Lists components under the current owner.

        Args:
            query: str, optional, query filters, please refer to
                    [Hub PQL](/docs/core/query-language/hub/#query)
            sort: str, optional, fields to order by, please refer to
                    [Hub PQL](/docs/core/query-language/hub/#sort)
            limit: int, optional, limit of components to return.
            offset: int, optional, offset pages to paginate hub.

        Returns:
            List[V1ComponentHub], list of component hub instances.
        """
        params = get_query_params(limit=limit, offset=offset, query=query, sort=sort)
        return self.client.component_hub_v1.list_component_hubs(self.owner, **params)

    @check_no_op
    @check_offline
    def delete(self):
        """Deletes hub based on the current owner and component hub name."""
        return self.client.component_hub_v1.delete_component_hub(self.owner, self.hub)

    @check_no_op
    @check_offline
    def update(self, data: Union[Dict, polyaxon_sdk.V1ComponentHub]):
        """Updates a hub based on the data passed.

        Args:
            data: Dict or V1ComponentHub, required.

        Returns:
            V1ComponentHub, hub instance from the response.
        """
        self._hub_data = self.client.component_hub_v1.patch_component_hub(
            self.owner, self.hub, body=data
        )
        self._hub = self._hub_data.name
        return self._hub_data
