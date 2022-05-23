#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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
import sys
import time
import uuid

from collections.abc import Mapping
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
from urllib.parse import urlparse

import ujson

from marshmallow import EXCLUDE
from urllib3.exceptions import HTTPError

import polyaxon_sdk

from polyaxon import settings
from polyaxon.api import K8S_V1_LOCATION, STREAMS_V1_LOCATION
from polyaxon.cli.errors import handle_cli_error
from polyaxon.client.client import PolyaxonClient
from polyaxon.client.decorators import client_handler, get_global_or_inline_config
from polyaxon.constants.metadata import META_COPY_ARTIFACTS
from polyaxon.containers.names import MAIN_CONTAINER_NAMES
from polyaxon.contexts import paths as ctx_paths
from polyaxon.env_vars.getters import (
    get_artifacts_store_name,
    get_project_error_message,
    get_project_or_local,
    get_run_info,
    get_run_or_local,
)
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.lifecycle import (
    LifeCycle,
    V1ProjectFeature,
    V1StatusCondition,
    V1Statuses,
)
from polyaxon.logger import logger
from polyaxon.managers.ignore import IgnoreConfigManager
from polyaxon.polyaxonfile import check_polyaxonfile
from polyaxon.polyflow import V1Matrix, V1Operation, V1RunKind
from polyaxon.schemas.types import V1ArtifactsType
from polyaxon.stores.polyaxon_store import PolyaxonStore
from polyaxon.utils.code_reference import get_code_reference
from polyaxon.utils.date_utils import file_modified_since
from polyaxon.utils.formatting import Printer
from polyaxon.utils.fqn_utils import get_entity_full_name, to_fqn_name
from polyaxon.utils.hashing import hash_dir, hash_file, hash_value
from polyaxon.utils.http_utils import absolute_uri
from polyaxon.utils.list_utils import to_list
from polyaxon.utils.path_utils import (
    check_or_create_path,
    delete_path,
    get_base_filename,
    get_dirs_under_path,
    get_files_in_path_context,
)
from polyaxon.utils.query_params import get_logs_params, get_query_params
from polyaxon.utils.tz_utils import now
from polyaxon.utils.urls_utils import get_proxy_run_url
from polyaxon.utils.validation import validate_tags
from polyaxon_sdk.rest import ApiException
from traceml.artifacts import V1ArtifactKind, V1RunArtifact
from traceml.events import V1Events
from traceml.logging.streamer import get_logs_streamer


class RunClient:
    """RunClient is a client to communicate with Polyaxon runs endpoints.

    If no values are passed to this class,
    Polyaxon will try to resolve the owner, project, and run uuid from the environment:
     * If you have a configured CLI, Polyaxon will use the configuration of the cli.
     * If you have a cached run using the CLI,
       the client will default to that cached run unless you override the values.
     * If you use this client in the context of a job or a service managed by Polyaxon,
       a configuration will be available to resolve the values based on that run.

    If you intend to create a new run instance or to list runs,
    only the `owner` and `project` parameters are required.

    You can always access the `self.client` to execute more APIs.

    Properties:
        project: str.
        owner: str.
        run_uuid: str.
        run_data: V1Run.
        status: str.
        namespace: str.
        client: [PolyaxonClient](/docs/core/python-library/polyaxon-client/)

    Args:
        owner: str, optional, the owner is the username or
             the organization name owning this project.
        project: str, optional, project name owning the run(s).
        run_uuid: str, optional, run uuid.
        client: [PolyaxonClient](/docs/core/python-library/polyaxon-client/), optional,
             an instance of a configured client, if not passed,
             a new instance will be created based on the available environment.
        is_offline: bool, optional,
             To trigger the offline mode manually instead of depending on `POLYAXON_IS_OFFLINE`.
        no_op: bool, optional,
             To set the NO_OP mode manually instead of depending on `POLYAXON_NO_OP`.

    Raises:
        PolyaxonClientException: If no owner and/or project are passed and Polyaxon cannot
             resolve the values from the environment.
    """

    @client_handler(check_no_op=True)
    def __init__(
        self,
        owner: str = None,
        project: str = None,
        run_uuid: str = None,
        client: PolyaxonClient = None,
        is_offline: bool = None,
        no_op: bool = None,
    ):
        self._is_offline = get_global_or_inline_config(
            config_key="is_offline", config_value=is_offline, client=client
        )
        self._no_op = get_global_or_inline_config(
            config_key="no_op", config_value=no_op, client=client
        )

        if self._no_op:
            return

        try:
            owner, project = get_project_or_local(
                get_entity_full_name(owner=owner, entity=project)
            )
        except PolyaxonClientException:
            pass

        if project is None:
            if settings.CLIENT_CONFIG.is_managed:
                owner, project, _run_uuid = get_run_info()
                run_uuid = run_uuid or _run_uuid
            elif not self._is_offline:
                raise PolyaxonClientException(
                    "Please provide a valid project, "
                    "or make sure this operation is managed by Polyaxon."
                )

        error_message = get_project_error_message(owner, project)
        if error_message and not self._is_offline:
            raise PolyaxonClientException(error_message)

        self._client = client
        self._owner = owner
        self._project = project
        self._run_uuid = (
            get_run_or_local(run_uuid)
            if not self._is_offline
            else run_uuid or uuid.uuid4().hex
        )
        default_runtime = (
            V1RunKind.JOB
            if self._is_offline or not settings.CLIENT_CONFIG.is_managed
            else None
        )
        self._run_data = polyaxon_sdk.V1Run(
            owner=self._owner,
            project=self._project,
            uuid=self._run_uuid,
            kind=default_runtime,
            runtime=default_runtime,
            is_managed=False if self._is_offline else None,
        )
        self._namespace = None
        self._results = {}
        self._artifacts_lineage = {}
        self._default_filename_sanitize_paths = []
        self._last_update = None
        self._store = None

    def _set_is_offline(
        self,
        client: PolyaxonClient = None,
        is_offline: bool = None,
    ):
        if is_offline is not None:
            return is_offline
        if client and client.config and client.config.is_offline is not None:
            return client.config.is_offline
        return settings.CLIENT_CONFIG.is_offline

    def _set_no_op(
        self,
        client: PolyaxonClient = None,
        no_op: bool = None,
    ):
        if no_op is not None:
            return no_op
        if client and client.config and client.config.no_op is not None:
            return client.config.no_op
        return settings.CLIENT_CONFIG.no_op

    @property
    def client(self):
        if self._client:
            return self._client
        self._client = PolyaxonClient()
        return self._client

    @property
    def store(self):
        if self._store:
            return self._store
        self._store = PolyaxonStore(client=self)
        return self._store

    @property
    def status(self) -> str:
        return self._run_data.status

    @property
    def settings(self) -> Optional[polyaxon_sdk.V1RunSettings]:
        if not self.run_data:
            return None
        if self.run_data.settings and isinstance(self.run_data.settings, Mapping):
            self._run_data.settings = polyaxon_sdk.V1RunSettings(
                **self.run_data.settings
            )
        return self.run_data.settings

    @property
    def namespace(self) -> str:
        if self._namespace:
            return self._namespace
        if self.settings and self.settings.namespace:
            self._namespace = self.settings.namespace
        else:
            self._namespace = self.get_namespace()
        return self._namespace

    @property
    def owner(self) -> str:
        return self._owner

    def set_owner(self, owner: str):
        self._owner = owner

    @property
    def project(self) -> str:
        return self._project

    def set_project(self, project: str):
        self._project = project

    @property
    def run_uuid(self) -> str:
        return self._run_uuid

    def set_run_uuid(self, run_uuid):
        self._run_uuid = run_uuid

    @property
    def run_data(self):
        return self._run_data

    @property
    def artifacts_lineage(self):
        return self._artifacts_lineage

    @client_handler(check_no_op=True)
    def get_inputs(self) -> Dict:
        """Gets the run's inputs.
        Returns:
            dict, all the run inputs/params.
        """
        if not self._run_data.inputs:
            self.refresh_data()
        return self._run_data.inputs

    @client_handler(check_no_op=True)
    def get_outputs(self) -> Dict:
        """Gets the run's outputs.
        Returns:
             dict, all the run outputs/metrics.
        """
        if not self._run_data.inputs:
            self.refresh_data()
        return self._run_data.outputs

    @client_handler(check_no_op=True, check_offline=True)
    def refresh_data(
        self, load_artifacts_lineage: bool = False, load_conditions: bool = False
    ):
        """Fetches the run data from the api."""
        self._run_data = self.client.runs_v1.get_run(
            self.owner, self.project, self.run_uuid
        )
        if load_conditions:
            _, conditions = self.get_statuses()
            self._run_data.status_conditions = conditions
        if load_artifacts_lineage:
            lineages = self.get_artifacts_lineage(limit=1000).results
            self._artifacts_lineage = {l.name: l for l in lineages}

    def _throttle_updates(self) -> bool:
        current_time = now().replace(microsecond=0)
        last_time, updates = self._last_update or (current_time, 0)
        if current_time == last_time and updates > 2:
            return True
        self._last_update = (current_time, updates + 1)
        return False

    def _update(
        self, data: Union[Dict, polyaxon_sdk.V1Run], async_req: bool = True
    ) -> polyaxon_sdk.V1Run:
        if self._is_offline:
            return self.run_data
        response = self.client.runs_v1.patch_run(
            owner=self.owner,
            project=self.project,
            run_uuid=self.run_uuid,
            body=data,
            async_req=async_req,
        )
        if not async_req:
            self._run_data = response
        return response

    @client_handler(check_no_op=True)
    def update(
        self, data: Union[Dict, polyaxon_sdk.V1Run], async_req: bool = False
    ) -> polyaxon_sdk.V1Run:
        """Updates a run based on the data passed.

        [Run API](/docs/api/#operation/PatchRun)

        Args:
            data: Dict or V1Run, required.
            async_req: bool, optional, default: False, execute request asynchronously.

        Returns:
            V1Run, run instance from the response.
        """
        if self._is_offline:
            for k in data:
                setattr(self._run_data, k, getattr(data, k, None))
        return self._update(data=data, async_req=async_req)

    @client_handler(check_no_op=True)
    def transfer(self, to_project: str, async_req: bool = False):
        """Transfers the run to a project under the same owner/organization.

        [Run API](/docs/api/#operation/TransferRun)

        Args:
            to_project: str, required, the destination project to transfer the run to.
            async_req: bool, optional, default: False, execute request asynchronously.
        """

        def _update_run():
            self._project = to_project
            self._run_data._project = to_project

        if self._is_offline:
            _update_run()
            return

        self.client.runs_v1.transfer_run(
            owner=self.owner,
            project=self.project,
            run_uuid=self.run_uuid,
            body={"project": to_project},
            async_req=async_req,
        )
        _update_run()

    def _create(
        self, data: Union[Dict, polyaxon_sdk.V1OperationBody], async_req: bool = False
    ) -> polyaxon_sdk.V1Run:
        response = self.client.runs_v1.create_run(
            owner=self.owner,
            project=self.project,
            body=data,
            async_req=async_req,
        )
        if not async_req:
            self._run_data = response
            self._run_uuid = self._run_data.uuid
            self._run_data.status = V1Statuses.CREATED
            self._namespace = None
            self._results = {}
            self._artifacts_lineage = {}
        return response

    @client_handler(check_no_op=True)
    def create(
        self,
        name: str = None,
        description: str = None,
        tags: Union[str, Sequence[str]] = None,
        content: Union[str, Dict, V1Operation] = None,
        is_managed: bool = True,
        pending: Optional[str] = None,
        meta_info: Optional[Dict] = None,
    ) -> polyaxon_sdk.V1Run:
        """Creates a new run based on the data passed.

        N.B. Create methods are only useful if you want to create a run programmatically,
        if you run a component/operation from the CLI/UI an instance will be created automatically.

        This is a generic create function, you can check other methods for creating runs:
          * from yaml: `create_from_polyaxonfile`
          * from url: `create_from_url`
          * from hub: `create_from_hub`

        > **Note**: If the `content` param is not passed, the run will be marked as non-managed.

        [Run API](/docs/api/#operation/CreateRun)

        Args:
            name: str, optional, it will override the name in the operation if provided.
            description: str, optional,
                 it will override the description in the operation if provided.
            tags: str or List[str], optional, list of tags,
                 it will override the tags in the operation if provided.
            content: str or Dict or V1Operation, optional.
            is_managed: bool, flag to create a managed run.
            pending: str, to specify if the run is pending approval (requires human validation) or pending upload.  # noqa
            meta_info: dict, meta info to create the run with.

        Returns:
            V1Run, run instance from the response.
        """
        tags = validate_tags(tags, validate_yaml=True)
        if self._is_offline:
            self._run_data.name = name
            self._run_data.description = description
            self._run_data.tags = tags
            self._run_data.owner = self._owner
            self._run_data.project = self._project
            if not self._run_uuid:
                self._run_uuid = uuid.uuid4().hex
            self.run_data.uuid = self._run_uuid
            return self.run_data
        if not content:
            is_managed = False
        elif not isinstance(content, (str, Mapping, V1Operation)):
            raise PolyaxonClientException(
                "Received an invalid content: {}".format(content)
            )
        if content:
            if isinstance(content, Mapping):
                content = V1Operation.from_dict(content)
            content = (
                content if isinstance(content, str) else content.to_dict(dump=True)
            )
        data = polyaxon_sdk.V1OperationBody(
            name=name,
            description=description,
            tags=tags,
            content=content,
            is_managed=is_managed,
            pending=pending,
            meta_info=meta_info,
        )
        self._create(data=data, async_req=False)
        return self.run_data

    @client_handler(check_no_op=True, check_offline=True)
    def create_from_polyaxonfile(
        self,
        polyaxonfile: str,
        name: str = None,
        description: str = None,
        tags: Union[str, Sequence[str]] = None,
        params: Dict = None,
        matrix: Union[Dict, V1Matrix] = None,
        presets: List[str] = None,
        queue: str = None,
        nocache: bool = None,
        cache: Union[int, str, bool] = None,
        approved: Union[int, str, bool] = None,
    ) -> polyaxon_sdk.V1Run:
        """Creates a new run based on a polyaxonfile.

        N.B. Create methods are only useful if you want to create a run programmatically,
        if you run a component/operation from the CLI/UI an instance will be created automatically.

        [Run API](/docs/api/#operation/CreateRun)

        Args:
            polyaxonfile: str, path to the polyaxonfile containing a YAML/Json specification.
                 The polyaxonfile should contain a
                 [V1Component](/docs/core/specification/component/) or an
                 [V1Operation](/docs/core/specification/operation/).
            name: str, optional,
                 it will override the name in the operation if provided.
            description: str, optional,
                 it will override the description in the operation if provided.
            tags: str or List[str], optional, list of tags,
                 it will override the tags in the operation if provided.
            params: dict, optional, a dictionary of parameters that will be
                 used to resolve the component's inputs/outputs.
            matrix: dict or V1Matrix, a matrix definition.
            presets: List[str], optional, the name of the
                 [presets](/docs/core/scheduling-presets/).
            queue: str, optional, the name of the
                 [queue](/docs/core/scheduling-strategies/queues/) to assign the run to.
            nocache: bool, optional, DEPRECATED Please use `cache='f'`
                 simple flag to disable
                 [cache check](/docs/automation/helpers/cache/).
                 If passed and the Polyaxonfile has cache section,
                 it will be patched with `disabled: true`.
            cache: Union[int, str, bool], optional, simple flag to enable/disable
                 [cache check](/docs/automation/helpers/cache/).
                 If passed and the Polyaxonfile will be patched with `disabled: true/false`.
                 e.g. `cache=1`, `cache='yes'`, `cache=False`, `cache='t'`, ...
            approved: Union[int, str, bool], optional, simple flag to enable/disable
                 human in the loop validation without changing the polyaxonfile,
                 similar to `isApproved: true/false`,
                 [manual approval](/docs/core/scheduling-strategies/manual-approval/).
                 Can be used with yes/no, y/n, false/true, f/t, 1/0. "
                 "e.g. `approved=1`, `approved='yes'`, `approved=False`, `approved='t'`, ..."

        Returns:
            V1Run, run instance from the response.
        """
        op_spec = check_polyaxonfile(
            polyaxonfile=polyaxonfile,
            params=params,
            matrix=matrix,
            presets=presets,
            queue=queue,
            nocache=nocache,
            cache=cache,
            approved=approved,
            verbose=False,
            is_cli=False,
        )
        return self.create(
            name=name, description=description, tags=tags, content=op_spec
        )

    @client_handler(check_no_op=True, check_offline=True)
    def create_from_url(
        self,
        url: str,
        name: str = None,
        description: str = None,
        tags: Union[str, Sequence[str]] = None,
        params: Dict = None,
        matrix: Union[Dict, V1Matrix] = None,
        presets: List[str] = None,
        queue: str = None,
        nocache: bool = None,
        cache: Union[int, str, bool] = None,
        approved: Union[int, str, bool] = None,
    ) -> polyaxon_sdk.V1Run:
        """Creates a new run from a url containing a Polyaxonfile specification.

        N.B. Create methods are only useful if you want to create a run programmatically,
        if you run a component/operation from the CLI/UI an instance will be created automatically.

        [Run API](/docs/api/#operation/CreateRun)

        Args:
            url: str, url containing a YAML/Json specification.
                 The url's polyaxonfile should contain a
                 [V1Component](/docs/core/specification/component/) or an
                 [V1Operation](/docs/core/specification/operation/).
            name: str, optional, it will override the name in the operation if provided.
            description: str, optional,
                 it will override the description in the operation if provided.
            tags: str or List[str], optional, list of tags,
                 it will override the tags in the operation if provided.
            params: dict, optional, a dictionary of parameters that will be
                 used to resolve the component's inputs/outputs.
            matrix: dict or V1Matrix, a matrix definition.
            presets: List[str], optional, the name of the
                 [presets](/docs/core/scheduling-presets/).
            queue: str, optional, the name of the
                 [queue](/docs/core/scheduling-strategies/queues/) to assign the run to.
            nocache: bool, optional, DEPRECATED Please use `cache='f'`
                 simple flag to disable
                 [cache check](/docs/automation/helpers/cache/).
                 If passed and the Polyaxonfile has cache section,
                 it will be patched with `disabled: true`.
            cache: Union[int, str, bool], optional, simple flag to enable/disable
                 [cache check](/docs/automation/helpers/cache/).
                 If passed and the Polyaxonfile will be patched with `disabled: true/false`.
                 e.g. `cache=1`, `cache='yes'`, `cache=False`, `cache='t'`, ...
            approved: Union[int, str, bool], optional, simple flag to enable/disable
                 human in the loop validation without changing the polyaxonfile,
                 similar to `isApproved: true/false`,
                 [manual approval](/docs/core/scheduling-strategies/manual-approval/).
                 Can be used with yes/no, y/n, false/true, f/t, 1/0. "
                 "e.g. `approved=1`, `approved='yes'`, `approved=False`, `approved='t'`, ..."

        Returns:
            V1Run, run instance from the response.
        """
        op_spec = check_polyaxonfile(
            url=url,
            params=params,
            matrix=matrix,
            presets=presets,
            queue=queue,
            nocache=nocache,
            cache=cache,
            approved=approved,
            verbose=False,
            is_cli=False,
        )
        return self.create(
            name=name, description=description, tags=tags, content=op_spec
        )

    @client_handler(check_no_op=True, check_offline=True)
    def create_from_hub(
        self,
        component: str,
        name: str = None,
        description: str = None,
        tags: Union[str, Sequence[str]] = None,
        params: Dict = None,
        matrix: Union[Dict, V1Matrix] = None,
        presets: str = None,
        queue: str = None,
        nocache: bool = None,
        cache: Union[int, str, bool] = None,
        approved: Union[int, str, bool] = None,
    ) -> polyaxon_sdk.V1Run:
        """Creates a new run from the hub based on the component name.

        N.B. Create methods are only useful if you want to create a run programmatically,
        if you run a component/operation from the CLI/UI an instance will be created automatically.

        If the component has required inputs, you should pass the params.

        [Run API](/docs/api/#operation/CreateRun)

        Args:
            component: str, name of the hub component.
            name: str, optional, it will override the name in the component if provided.
            description: str, optional,
                 it will override the description in the component if provided.
            tags: str or List[str], optional, list of tags,
                 it will override the tags in the component if provided.
            params: dict, optional, a dictionary of parameters that will be
                 used to resolve the component's inputs/outputs.
            matrix: dict or V1Matrix, a matrix definition.
            presets: List[str], optional, the name of the
                 [presets](/docs/core/scheduling-presets/).
            queue: str, optional, the name of the
                 [queue](/docs/core/scheduling-strategies/queues/) to assign the run to.
            nocache: bool, optional, DEPRECATED Please use `cache='f'`
                 simple flag to disable
                 [cache check](/docs/automation/helpers/cache/).
                 If passed and the Polyaxonfile has cache section,
                 it will be patched with `disabled: true`.
            cache: Union[int, str, bool], optional, simple flag to enable/disable
                 [cache check](/docs/automation/helpers/cache/).
                 If passed and the Polyaxonfile will be patched with `disabled: true/false`.
                 e.g. `cache=1`, `cache='yes'`, `cache=False`, `cache='t'`, ...
            approved: Union[int, str, bool], optional, simple flag to enable/disable
                 human in the loop validation without changing the polyaxonfile,
                 similar to `isApproved: true/false`,
                 [manual approval](/docs/core/scheduling-strategies/manual-approval/).
                 Can be used with yes/no, y/n, false/true, f/t, 1/0. "
                 "e.g. `approved=1`, `approved='yes'`, `approved=False`, `approved='t'`, ..."

        Returns:
            V1Run, run instance from the response.
        """
        op_spec = check_polyaxonfile(
            hub=component,
            params=params,
            matrix=matrix,
            presets=presets,
            queue=queue,
            nocache=nocache,
            cache=cache,
            approved=approved,
            verbose=False,
            is_cli=False,
        )
        return self.create(
            name=name, description=description, tags=tags, content=op_spec
        )

    @client_handler(check_no_op=True)
    def log_status(
        self,
        status: str,
        reason: str = None,
        message: str = None,
        last_transition_time: datetime = None,
        last_update_time: datetime = None,
    ):
        """Logs a new run status.

        <blockquote class="info">
        <strong>Note</strong>: If you are executing a managed run, you don't need to call this method manually.
        This method is only useful for manual runs outside of Polyaxon.
        </blockquote>

        N.B you will probably use one of the simpler methods:
            * log_succeeded
            * log_stopped
            * log_failed
            * start
            * end

        [Run API](/docs/api/#operation/CreateRunStatus)

        Args:
            status: str, a valid [Statuses](/docs/core/specification/lifecycle/) value.
            reason: str, optional, reason or service issuing the status change.
            message: str, optional, message to log with this status.
            last_transition_time: datetime, default `now`.
            last_update_time: datetime, default `now`.
        """
        reason = reason or "PolyaxonClient"
        self._run_data.status = status
        current_date = now()
        status_condition = V1StatusCondition(
            type=status,
            status=True,
            reason=reason,
            message=message,
            last_transition_time=last_transition_time or current_date,
            last_update_time=last_update_time or current_date,
        )
        if self._is_offline:
            self._run_data.status_conditions = self._run_data.status_conditions or []
            self._run_data.status_conditions.append(status_condition)
            if status == V1Statuses.CREATED:
                self._run_data.created_at = current_date
            LifeCycle.set_started_at(self._run_data)
            LifeCycle.set_finished_at(self._run_data)
            return
        self.client.runs_v1.create_run_status(
            owner=self.owner,
            project=self.project,
            uuid=self.run_uuid,
            body={"condition": status_condition},
            async_req=True,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def get_statuses(
        self, last_status: str = None
    ) -> Tuple[str, List[V1StatusCondition]]:
        """Gets the run's statuses.

        [Run API](/docs/api/#operation/GetRunStatus)

        Args:
            last_status: str, a valid [Statuses](/docs/core/specification/lifecycle/) value.

        Returns:
            Tuple[str, List[Conditions]], last status and ordered status conditions.
        """
        try:
            response = self.client.runs_v1.get_run_statuses(
                self.owner, self.project, self.run_uuid
            )
            if not last_status:
                return response.status, response.status_conditions
            if last_status == response.status:
                return last_status, []

            _conditions = []
            for c in reversed(response.status_conditions):
                if c.type == last_status:
                    break
                _conditions.append(c)

            return response.status, reversed(_conditions)

        except (ApiException, HTTPError) as e:
            raise PolyaxonClientException("Api error: %s" % e) from e

    def _wait_for_condition(self, statuses: List[str] = None):
        statuses = to_list(statuses, check_none=True)

        def condition():
            if statuses:
                return last_status in statuses
            return LifeCycle.is_done(last_status)

        last_status = None
        while not condition():
            if last_status:
                time.sleep(settings.CLIENT_CONFIG.watch_interval)
            try:
                last_status, _conditions = self.get_statuses(last_status)
                yield last_status, _conditions
            except ApiException as e:
                if e.status in {500, 502, 503, 504}:
                    yield last_status, []
                else:
                    raise e

    @client_handler(check_no_op=True, check_offline=True)
    def wait_for_condition(
        self,
        statuses: List[str] = None,
        print_status: bool = False,
        live_update: any = None,
    ):
        """Waits for the run's last status to meet a condition.

        If a list of statuses is passed, it will wait for the condition:
         * last status is one of the statuses passed.

        Otherwise, it will wait until the user interrupts the function or
        when the run reaches a final status.

        N.B. if you want to watch the statuses and receive the status/conditions,
        please use `watch_statuses` instead which yields the results.
        """
        for status, conditions in self._wait_for_condition(statuses):
            self._run_data.status = status
            if print_status:
                print("Last received status: {}\n".format(status))
            if live_update:
                latest_status = Printer.add_status_color(
                    {"status": status}, status_key="status"
                )
                live_update.update(status="{}\n".format(latest_status["status"]))

    @client_handler(check_no_op=True, check_offline=True)
    def watch_statuses(self, statuses: List[str] = None):
        """Watches run statuses.

        If statuses is passed the watch will wait for a condition:
         * last status is one of the statuses passed.

        Otherwise, it will watch until the user interrupts it or
        when the run reaches a final status.

        N.B. if you just want to wait for a status condition without expecting a yield,
        please use `wait_for_condition` instead

        Yields:
            Tuple[status, List[conditions]]:
                This function will yield the last status and condition for every check.
        """
        for status, conditions in self._wait_for_condition(statuses):
            self._run_data.status = status
            yield status, conditions

    @client_handler(check_no_op=True, check_offline=True)
    def get_logs(self, last_file=None, last_time=None) -> "V1Logs":
        """Gets the run's logs.

        This method return up-to 2000 line logs per request.

        Returns:
            V1Logs
        """
        params = get_logs_params(last_file=last_file, last_time=last_time)
        return self.client.runs_v1.get_run_logs(
            self.namespace, self.owner, self.project, self.run_uuid, **params
        )

    @client_handler(check_no_op=True, check_offline=True)
    def watch_logs(self, hide_time: bool = False, all_info: bool = False):
        """Watches run logs.

        Args:
            hide_time: bool, optional, default: False, remove time information from log lines.
            all_info: bool, optional, default: False, show all information about log lines.
        """
        return get_run_logs(
            client=self, hide_time=hide_time, all_info=all_info, follow=True
        )

    @client_handler(check_no_op=True, check_offline=True)
    def inspect(self):
        return self.client.runs_v1.inspect_run(
            self.namespace, self.owner, self.project, self.run_uuid
        )

    @client_handler(check_no_op=True, check_offline=True)
    def shell(
        self,
        command: str = None,
        pod: str = None,
        container: str = None,
        stderr: bool = True,
        stdin: bool = True,
        stdout: bool = True,
        tty: bool = True,
    ):
        """Executes a command in a container.

        Streams allows to switch to raw terminal mode by sending stdin to 'bash'
        and receives stdout/stderr from 'bash' back to the client.

        Args:
            command: str, optional, a command to execute.
            pod: str, optional, the pod to use for executing the command.
            container: str, optional, the container to use for executing the command.
            stderr: bool, optional
            stdin: bool, optional
            stdout: bool, optional
            tty: bool, optional
        """
        from polyaxon.client.transport import ws_client

        if not pod or not container:
            inspection = self.inspect()
            if not inspection:
                raise PolyaxonClientException(
                    "The shell command is only usable for operations managed by Polyaxon "
                    "and actively running."
                )
            if not pod:
                pod = next(iter(inspection.keys()))
            pod_content = inspection.get(pod, {})
            if not pod_content:
                raise PolyaxonClientException(
                    "The shell command is only usable for operations managed by Polyaxon "
                    "and actively running. Error: the pod `{}` was not found.".format(
                        pod
                    )
                )
            pod_content = pod_content.get("spec", {})
            pod_containers = [c.get("name") for c in pod_content.get("containers", [])]
            if not pod_containers:
                raise PolyaxonClientException(
                    "The shell command is only usable for operations managed by Polyaxon "
                    "and actively running. Error: the operation does not have containers."
                )
            if container:
                if container not in pod_containers:
                    raise PolyaxonClientException(
                        "The shell command is only usable for operations managed by Polyaxon "
                        "and actively running. "
                        "Error: the container `{}` was not found under the pod `{}`.".format(
                            container, pod
                        )
                    )
            else:
                for c in MAIN_CONTAINER_NAMES:
                    if c in pod_containers:
                        container = c
                        break
                if not container:
                    container = pod_containers[0]

        url = get_proxy_run_url(
            service=K8S_V1_LOCATION,
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            run_uuid=self.run_uuid,
            subpath="k8s_exec/{pod}/{container}".format(
                pod=pod,
                container=container,
            ),
        )
        url = absolute_uri(url=url, host=self.client.config.host)

        command = command or "/bin/bash"
        return ws_client.websocket_call(
            self.client.config.sdk_config,
            url,
            query_params=[
                ("command", command.split()),
                ("stderr", stderr),
                ("stdin", stdin),
                ("stdout", stdout),
                ("tty", tty),
            ],
            headers=self.client.config.get_full_headers(auth_key="authorization"),
        )

    @client_handler(check_no_op=True, check_offline=True)
    def get_events(
        self,
        kind: V1ArtifactKind,
        names: List[str],
        orient: str = None,
        force: bool = False,
    ):
        """Gets the run's events

        Args:
            kind: str, a valid `V1ArtifactKind`.
            names: List[str], list of events to return.
            orient: str, csv or dict.
            force: bool, force reload the events.
        """
        return self.client.runs_v1.get_run_events(
            self.namespace,
            self.owner,
            self.project,
            self.run_uuid,
            kind=kind,
            names=names,
            orient=orient,
            force=force,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def get_multi_run_events(
        self,
        kind: V1ArtifactKind,
        runs: List[str],
        names: List[str],
        orient: str = None,
        force: bool = False,
    ):
        """Gets events for multiple runs.

        Args:
            kind: str, a valid `V1ArtifactKind`.
            runs: List[str], list of run uuids to return events for.
            names: List[str], list of events to return.
            orient: str, csv or dict.
            force: bool, force reload the events.
        Returns:
            V1EventsResponse
        """
        return self.client.runs_v1.get_multi_run_events(
            self.namespace,
            self.owner,
            self.project,
            kind=kind,
            names=names,
            runs=runs,
            orient=orient,
            force=force,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def get_artifacts_lineage(
        self, query: str = None, sort: str = None, limit: int = None, offset: int = None
    ):
        """Gets the run's artifacts lineage.

        [Run API](/docs/api/#operation/GetRunArtifactsLineage)

        Args:
            query: str, optional, query filters, please refer to
                 [Run PQL](/docs/core/query-language/artifacts-lineage/#query)
            sort: str, optional, fields to order by, please refer to
                 [Run PQL](/docs/core/query-language/artifacts-lineage/#sort)
            limit: int, optional, limit of runs to return.
            offset: int, optional, offset pages to paginate runs.

        Returns:
            V1ListRunArtifactsResponse.
        """
        params = get_query_params(
            limit=limit or 20, offset=offset, query=query, sort=sort
        )
        return self.client.runs_v1.get_run_artifacts_lineage(
            self.owner, self.project, self.run_uuid, **params
        )

    @client_handler(check_no_op=True, check_offline=True)
    def get_runs_artifacts_lineage(
        self, query: str = None, sort: str = None, limit: int = None, offset: int = None
    ):
        """Gets the artifacts lineage for multiple runs under project based on query.

        [Run API](/docs/api/#operation/GetRunsArtifactsLineage)

        **Available from v1.18**

        Args:
            query: str, optional, query filters, please refer to
                 [Run PQL](/docs/core/query-language/artifacts-lineage/#query)
            sort: str, optional, fields to order by, please refer to
                 [Run PQL](/docs/core/query-language/artifacts-lineage/#sort)
            limit: int, optional, limit of runs to return.
            offset: int, optional, offset pages to paginate runs.

        Returns:
            V1ListRunArtifactsResponse.
        """
        params = get_query_params(
            limit=limit or 20, offset=offset, query=query, sort=sort
        )
        return self.client.runs_v1.get_runs_artifacts_lineage(
            self.owner, self.project, **params
        )

    @client_handler(check_no_op=True, check_offline=True)
    def get_artifact(self, path: str, stream: bool = True, force: bool = False):
        """Gets the run's artifact.

        Args:
            path: str, the relative path of the artifact to return.
            stream: bool, optional, default: True, whether to stream the artifact content.
            force: bool, force reload the artifact.

        Returns:
            str.
        """
        return self.client.runs_v1.get_run_artifact(
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            uuid=self.run_uuid,
            path=path,
            stream=stream,
            force=force,
            _preload_content=True,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def download_artifact_for_lineage(
        self,
        lineage: polyaxon_sdk.V1RunArtifact,
        force: bool = False,
        path_to: str = None,
    ):
        """Downloads an run artifact given a lineage reference.

        Args:
            lineage: V1RunArtifact, the artifact lineage.
            path_to: str, optional, path to download to.
            force: bool, force reload the artifact.

        Returns:
            str
        """
        if not self.run_uuid:
            return

        lineage_path = lineage.path
        summary = lineage.summary or {}
        is_event = summary.get("is_event")
        has_step = summary.get("step")

        if self.run_uuid in lineage_path:
            lineage_path = os.path.relpath(lineage_path, self.run_uuid)

        if V1ArtifactKind.is_single_file_event(lineage.kind):
            return self.download_artifact(
                path=lineage_path, force=force, path_to=path_to
            )

        if V1ArtifactKind.is_single_or_multi_file_event(lineage.kind):
            if is_event or has_step:
                url = get_proxy_run_url(
                    service=STREAMS_V1_LOCATION,
                    namespace=self.namespace,
                    owner=self.owner,
                    project=self.project,
                    run_uuid=self.run_uuid,
                    subpath="events/{}".format(lineage.kind),
                )
                url = absolute_uri(url=url, host=self.client.config.host)
                params = {"names": lineage.name, "pkg_assets": True}
                if force:
                    params["force"] = True

                return self.store.download_file(
                    url=url,
                    path=self.run_uuid,
                    use_filepath=False,
                    extract_path=path_to,
                    path_to=path_to,
                    params=params,
                    untar=True,
                )
            elif V1ArtifactKind.is_file_or_dir(lineage.kind):
                return self.download_artifacts(
                    path=lineage_path, path_to=path_to, check_path=True
                )
            else:
                return self.download_artifact(
                    path=lineage_path, force=force, path_to=path_to
                )

        if V1ArtifactKind.is_file(lineage.kind):
            return self.download_artifact(
                path=lineage_path, force=force, path_to=path_to
            )

        if V1ArtifactKind.is_dir(lineage.kind):
            return self.download_artifacts(path=lineage_path, path_to=path_to)

        if V1ArtifactKind.is_file_or_dir(lineage.kind):
            return self.download_artifacts(
                path=lineage_path, path_to=path_to, check_path=True
            )

    @client_handler(check_no_op=True, check_offline=True)
    def download_artifact(self, path: str, force: bool = False, path_to: str = None):
        """Downloads a single run artifact.

        Args:
            path: str, the relative path of the artifact to return.
            path_to: str, optional, path to download to.
            force: bool, force reload the artifact.

        Returns:
            str
        """
        url = get_proxy_run_url(
            service=STREAMS_V1_LOCATION,
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            run_uuid=self.run_uuid,
            subpath="artifact",
        )
        url = absolute_uri(url=url, host=self.client.config.host)
        params = {}
        if force:
            params["force"] = True

        return self.store.download_file(
            url=url, path=path, path_to=path_to, params=params
        )

    @client_handler(check_no_op=True, check_offline=True)
    def download_artifacts(
        self,
        path: str = "",
        path_to: str = None,
        untar: bool = True,
        delete_tar: bool = True,
        extract_path: str = None,
        check_path: bool = False,
    ):
        """Downloads a subpath containing multiple run artifacts.

        Args:
            path: str, the relative path of the artifact to return.
            path_to: str, optional, path to download to.
            untar: bool, optional, default: true.
            delete_tar: bool, optional, default: true.
            extract_path: str, optional.
            check_path: bool, optional, default: false.
                 To force the API to check if the path is file or dir.
        Returns:
            str.
        """
        url = get_proxy_run_url(
            service=STREAMS_V1_LOCATION,
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            run_uuid=self.run_uuid,
            subpath="artifacts",
        )
        url = absolute_uri(url=url, host=self.client.config.host)
        params = {}
        if check_path:
            params["check_path"] = True

        return self.store.download_file(
            url=url,
            path=path,
            untar=untar,
            path_to=path_to,
            delete_tar=delete_tar and untar,
            extract_path=extract_path,
            params=params,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def upload_artifact(
        self,
        filepath: str,
        path: str = None,
        untar: bool = False,
        overwrite: bool = True,
        show_progress: bool = True,
    ):
        """Uploads a single artifact to the run's artifacts store path.

        Args:
            filepath: str, the filepath to upload.
            path: str, optional, path to upload to, otherwise it will be on the run's root path.
            untar: bool, optional, if the file uploaded is tar.gz and
                 it should be decompressed on the artifacts store.
            overwrite: bool, optional, if the file uploaded should overwrite any previous content.
            show_progress: bool, to show a progress bar.

        Returns:
            str
        """
        url = get_proxy_run_url(
            service=STREAMS_V1_LOCATION,
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            run_uuid=self.run_uuid,
            subpath="artifact",
        )
        url = absolute_uri(url=url, host=self.client.config.host)

        return self.store.upload_file(
            url=url,
            filepath=filepath,
            path=path or "",
            untar=untar,
            overwrite=overwrite,
            show_progress=show_progress,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def upload_artifacts_dir(
        self,
        dirpath: str,
        path: str = "",
        overwrite: bool = True,
        relative_to: str = None,
    ):
        """Uploads a full directory to the run's artifacts store path.

        > This function crawls all files to upload and uses `upload_artifacts`,
        > it also respects `.polyaxonignore` file if it exists or the default ignore pattern.

        Args:
            dirpath: str, the dirpath to upload.
            path: str, the relative path of the artifact to return.
            overwrite: bool, optional, if the file uploaded should overwrite any previous content.
            relative_to: str, optional, if the path uploaded is not the current dir,
                 and you want to cancel the relative path.

        Returns:
            str.
        """
        files = IgnoreConfigManager.get_unignored_filepaths(
            path=dirpath, addtional_patterns=IgnoreConfigManager.get_push_patterns()
        )
        if not files:
            logger.warning(
                "No files detected under the path %s.\n"
                "This could happen if the path is empty or "
                "ignored by one of the patterns in the ignore manager.",
                dirpath,
            )
            return
        return self.upload_artifacts(
            files=files,
            path=path or "",
            overwrite=overwrite,
            relative_to=relative_to,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def upload_artifacts(
        self,
        files: List[str],
        path: str = "",
        overwrite: bool = True,
        relative_to: str = None,
    ):
        """Uploads multiple artifacts to the run's artifacts store path.

        Args:
            files: List[str], list of files to upload.
            path: str, the relative path of the artifact to return.
            overwrite: bool, optional, if the file uploaded should overwrite any previous content.
            relative_to: str, optional, if the path uploaded is not the current dir,
                 and you want to cancel the relative path.

        Returns:
            str.
        """
        if not files:
            logger.warning("No files to upload to %s.", path)
            return
        url = get_proxy_run_url(
            service=STREAMS_V1_LOCATION,
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            run_uuid=self.run_uuid,
            subpath="artifacts",
        )
        url = absolute_uri(url=url, host=self.client.config.host)

        return self.store.upload_dir(
            url=url,
            path=path,
            files=files,
            overwrite=overwrite,
            relative_to=relative_to,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def delete_artifact(self, path: str):
        """Deletes a single run artifact.

        Args:
            path: str, the relative path of the artifact to return.
        """
        self.client.runs_v1.delete_run_artifact(
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            uuid=self.run_uuid,
            path=path,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def delete_artifacts(self, path: str):
        """Deletes a subpath containing multiple run artifacts.

        Args:
            path: str, the relative path of the artifact to return.
        """
        return self.client.runs_v1.delete_run_artifacts(
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            uuid=self.run_uuid,
            path=path,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def get_artifacts_tree(self, path: str = ""):
        """Return the artifacts tree based on the path.

        Args:
            path: str, the relative path of the artifact tree to return.

        Returns:
            V1ArtifactTree.
        """
        return self.client.runs_v1.get_run_artifacts_tree(
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            uuid=self.run_uuid,
            path=path,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def stop(self):
        """Stops the current run."""
        self.client.runs_v1.stop_run(
            self.owner,
            self.project,
            self.run_uuid,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def approve(self):
        """Approves the current run if it's pending upload or human approval."""
        self.client.runs_v1.approve_run(
            self.owner,
            self.project,
            self.run_uuid,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def invalidate(self):
        """Invalidates the current run."""
        self.client.runs_v1.invalidate_run(
            self.owner,
            self.project,
            self.run_uuid,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def restart(
        self,
        override_config=None,
        copy: bool = False,
        copy_dirs: List[str] = None,
        copy_files: List[str] = None,
        name: str = None,
        description: str = None,
        tags: Union[str, Sequence[str]] = None,
        **kwargs,
    ):
        """Restarts the current run

        Args:
            override_config: Dict or str, optional,
                 config to use for overriding the original run's config.
            copy: bool, optional, default: False, to restart with copy mechanism.
            copy_dirs: List[str], optional, default: None or all in copy mode, list of dirs to copy.
            copy_files: List[str], optional, default: None or all in copy mode, list of files to copy.  # noqa
            name: str, optional, default: None, name to use for the restarted run.
            description: str, optional, default: None, description to use for the restarted run.
            tags: list[str], optional, default: None, tags to use for the restarted run.

        Returns:
            V1Run instance.
        """
        body = polyaxon_sdk.V1Run(content=override_config)
        if name:
            body.name = name
        if description:
            body.description = description
        if tags:
            tags = validate_tags(tags, validate_yaml=True)
            body.tags = tags
        if copy or copy_dirs or copy_files:
            if copy_dirs or copy_files:
                copy_dirs = to_list(copy_dirs, check_none=True)
                copy_files = to_list(copy_files, check_none=True)
                copy_artifacts = V1ArtifactsType()
                if copy_dirs:
                    copy_artifacts.dirs = [
                        "{}/{}".format(self.run_uuid, cp) for cp in copy_dirs
                    ]
                if copy_files:
                    copy_artifacts.files = [
                        "{}/{}".format(self.run_uuid, cp) for cp in copy_files
                    ]
                body.meta_info = {META_COPY_ARTIFACTS: copy_artifacts.to_dict()}
            return self.client.runs_v1.copy_run(
                self.owner, self.project, self.run_uuid, body=body, **kwargs
            )
        else:
            return self.client.runs_v1.restart_run(
                self.owner, self.project, self.run_uuid, body=body, **kwargs
            )

    @client_handler(check_no_op=True, check_offline=True)
    def resume(self, override_config=None, **kwargs):
        """Resumes the current run

        Args:
            override_config: Dict or str, optional,
                 config to use for overriding the original run's config.

        Returns:
            V1Run instance.
        """
        body = polyaxon_sdk.V1Run(content=override_config)
        return self.client.runs_v1.resume_run(
            self.owner, self.project, self.run_uuid, body=body, **kwargs
        )

    @client_handler(check_no_op=True)
    def set_description(self, description: str, async_req: bool = True):
        """Sets a new description for the current run.

        Args:
            description: str, the description to set.
            async_req: bool, optional, default: False, execute request asynchronously.
        """
        self._run_data.description = description
        self._update({"description": description}, async_req=async_req)

    @client_handler(check_no_op=True)
    def set_name(self, name: str, async_req: bool = True):
        """Sets a new name for the current run.

        Args:
            name: str, the name to set.
            async_req: bool, optional, default: False, execute request asynchronously.
        """
        self._run_data.name = name
        self._update({"name": name}, async_req=async_req)

    @client_handler(check_no_op=True)
    def log_inputs(self, reset: bool = False, async_req: bool = True, **inputs):
        """Logs or resets new inputs/params for the current run.


        > **Note**: If you are starting a run from the CLI/UI
        > polyaxon will track all inputs from the Polyaxonfile,
        > so you generally don't need to set them manually.
        > But you can always add or reset these params/inputs once your code starts running.

        Args:
            reset: bool, optional, if True, it will reset the whole inputs state.
                 Note that Polyaxon will automatically populate the inputs based
                 on the Polyaxonfile inputs definition and params passed.
            async_req: bool, optional, default: False, execute request asynchronously.
            inputs: **kwargs, e.g. param1=value1, param2=value2, ...
        """
        inputs = {to_fqn_name(k): v for k, v in inputs.items()}
        patch_dict = {"inputs": inputs}
        if reset is False:
            patch_dict["merge"] = True
            self._run_data.inputs = self._run_data.inputs or {}
            self._run_data.inputs.update(inputs)
        else:
            self._run_data.inputs = inputs
        self._update(patch_dict, async_req=async_req)

    @client_handler(check_no_op=True)
    def log_outputs(self, reset: bool = False, async_req: bool = True, **outputs):
        """Logs a new outputs/results for the current run.


        Args:
            reset: bool, optional, if True, it will reset the whole outputs state.
                 Note that Polyaxon will automatically populate some outputs based
                 on the Polyaxonfile outputs definition and params passed.
            async_req: bool, optional, default: False, execute request asynchronously.
            outputs: **kwargs, e.g. output1=value1, metric2=value2, ...
        """
        outputs = {to_fqn_name(k): v for k, v in outputs.items()}
        patch_dict = {"outputs": outputs}
        if reset is False:
            patch_dict["merge"] = True
            self._run_data.outputs = self._run_data.outputs or {}
            self._run_data.outputs.update(outputs)
        else:
            self._run_data.outputs = outputs
        self._update(patch_dict, async_req=async_req)

    @client_handler(check_no_op=True)
    def log_meta(self, reset: bool = False, async_req: bool = True, **meta):
        """Logs meta_info for the current run.

        > **Note**: Use carefully! The meta information is used by
        > Polyaxon internally to perform several information.

        Polyaxon Client already uses this method to log information
        about several events and artifacts, Polyaxon API/Scheduler uses
        this information to set meta information about the run.

        An example use case for this method is to update the concurrency
        of a pipeline to increase/decrease the initial value:
        ```python
        >>> from polyaxon.client import RunClient
        >>> client = RunClient()
        >>> client.log_meta(concurrency=5)
        ```

        Args:
            reset: bool, optional, if True, it will reset the whole meta info state.
            async_req: bool, optional, default: False, execute request asynchronously.
            meta: **kwargs, e.g. concurrency=10, has_flag=True, ...
        """
        meta = {to_fqn_name(k): v for k, v in meta.items()}
        patch_dict = {"meta_info": meta}
        if reset is False:
            patch_dict["merge"] = True
            self._run_data.meta_info = self._run_data.meta_info or {}
            self._run_data.meta_info.update(meta)
        else:
            self._run_data.meta_info = meta
        self._update(patch_dict, async_req=async_req)

    @client_handler(check_no_op=True)
    def log_tags(
        self,
        tags: Union[str, Sequence[str]],
        reset: bool = False,
        async_req: bool = True,
    ):
        """Logs new tags for the current run.

        Args:
            tags: str or List[str], tag or tags to log.
            reset: bool, optional, if True, it will reset the whole tags state.
                 Note that Polyaxon will automatically populate the tags based
                 on the Polyaxonfile.
            async_req: bool, optional, default: False, execute request asynchronously.
        """
        tags = validate_tags(tags, validate_yaml=True)
        patch_dict = {"tags": tags}
        if reset is False:
            patch_dict["merge"] = True
            self._run_data.tags = self._run_data.tags or []
            self._run_data.tags += [t for t in tags if t not in self._run_data.tags]
        else:
            self._run_data.tags = tags
        self._update(patch_dict, async_req=async_req)

    @client_handler(check_no_op=True)
    def start(self):
        """Sets the current run to `running` status.

        <blockquote class="info">
        <strong>Note</strong>: If you are executing a managed run, you don't need to call this method manually.
        This method is only useful for manual runs outside of Polyaxon.
        </blockquote>
        """
        self.log_status(V1Statuses.RUNNING, message="Operation is running")

    def _log_end_status(
        self,
        status: str,
        reason: str = None,
        message: str = None,
    ):
        """Sets the current run to `status` status.

        <blockquote class="info">
        <strong>Note</strong>: If you are executing a managed run, you don't need to call this method manually.
        This method is only useful for manual runs outside of Polyaxon.
        </blockquote>

        Args:
            status: str, a valid [Statuses](/docs/core/specification/lifecycle/) value.
            reason: str, optional, reason or service issuing the status change.
            message: str, optional, message to log with this status.
        """
        if self.status in LifeCycle.DONE_VALUES:
            return
        self.log_status(status=status, reason=reason, message=message)
        time.sleep(
            0.1
        )  # Just to give the opportunity to the worker to pick the message

    @client_handler(check_no_op=True)
    def log_succeeded(self, message="Operation has succeeded"):
        """Sets the current run to `succeeded` status.

        <blockquote class="info">
        <strong>Note</strong>: If you are executing a managed run,
        you don't need to call this method manually.
        This method is only useful for manual runs outside of Polyaxon.
        </blockquote>
        """
        self._log_end_status(status=V1Statuses.SUCCEEDED, message=message)

    @client_handler(check_no_op=True)
    def log_stopped(self, message="Operation is stopped"):
        """Sets the current run to `stopped` status.

        <blockquote class="info">
        <strong>Note</strong>: If you are executing a managed run,
        you don't need to call this method manually.
        This method is only useful for manual runs outside of Polyaxon.
        </blockquote>
        """
        self._log_end_status(status=V1Statuses.STOPPED, message=message)

    @client_handler(check_no_op=True)
    def log_failed(self, reason: str = None, message: str = None):
        """Sets the current run to `failed` status.

        <blockquote class="info">
        <strong>Note</strong>: If you are executing a managed run, you don't need to call this method manually.
        This method is only useful for manual runs outside of Polyaxon.
        </blockquote>

        Args:
            reason: str, optional, reason or service issuing the status change.
            message: str, optional, message to log with this status.
        """
        self._log_end_status(
            status=V1Statuses.FAILED,
            reason=reason,
            message=message,
        )

    def _sanitize_filename(self, filename: str, for_patterns: List[str] = None) -> str:
        """Ensures that the filename never includes common context paths"""
        if not self.run_uuid or ctx_paths.CONTEXT_ROOT not in filename:
            return to_fqn_name(filename)

        for_patterns = for_patterns or []
        if not self._default_filename_sanitize_paths:
            self._default_filename_sanitize_paths = [
                ctx_paths.CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT.format(self.run_uuid)
                + os.sep,
                ctx_paths.CONTEXT_MOUNT_RUN_EVENTS_FORMAT.format(self.run_uuid)
                + os.sep,
                ctx_paths.CONTEXT_MOUNT_RUN_ASSETS_FORMAT.format(self.run_uuid)
                + os.sep,
                ctx_paths.CONTEXT_MOUNT_RUN_SYSTEM_RESOURCES_EVENTS_FORMAT.format(
                    self.run_uuid
                )
                + os.sep,
                ctx_paths.CONTEXT_MOUNT_ARTIFACTS_FORMAT.format(self.run_uuid) + os.sep,
                ctx_paths.get_offline_path(
                    entity_value=self.run_uuid, entity_kind=V1ProjectFeature.RUNTIME
                )
                + os.sep,
            ]
        for p in self._default_filename_sanitize_paths + for_patterns:
            if filename.startswith(p):
                filename = filename[len(p) :]
                break

        return to_fqn_name(filename)

    def _sanitize_filepath(self, filepath: str, rel_path: str = None) -> str:
        """Ensures that the filepath never includes common context paths"""
        if not filepath or rel_path:
            return rel_path

        if not self.run_uuid:
            return rel_path or filepath

        if self.run_uuid in filepath:
            return filepath.split(self.run_uuid + "/")[1]

        def is_abs():
            if os.path.isabs(filepath):
                return True
            try:
                if urlparse(filepath).scheme:
                    return True
                return False
            except Exception:  # noqa
                return False

        abspath = filepath if is_abs() else os.path.abspath(filepath)

        for_patterns = []
        if getattr(self, "_artifacts_path"):
            for_patterns.append(getattr(self, "_artifacts_path"))
        if getattr(self, "_store_path"):
            for_patterns.append(getattr(self, "_store_path"))
        context_root = (
            ctx_paths.CONTEXT_OFFLINE_ROOT
            if self._is_offline
            else ctx_paths.CONTEXT_MOUNT_ARTIFACTS
        )
        for_patterns += [os.path.join(context_root, self.run_uuid), context_root]

        for _path in for_patterns:
            if _path in abspath:
                try:
                    return os.path.relpath(abspath, _path)
                except Exception as e:
                    logger.debug("could not calculate relative path %s", e)

        return rel_path or abspath

    def _log_has_events(self):
        if not self._has_meta_key("has_events"):
            self.log_meta(has_events=True)

    def _log_has_metrics(self):
        data = {}
        if not self._has_meta_key("has_metrics"):
            data["has_metrics"] = True
        if not self._has_meta_key("has_events"):
            data["has_events"] = True
        if data:
            self.log_meta(**data)

    def _log_has_model(self):
        if not self._has_meta_key("has_model"):
            self.log_meta(has_model=True)

    @client_handler(check_no_op=True)
    def log_progress(self, value: float):
        """Logs the progress of the run.

        In offline

        Args:
            value: float, a value between 0 and 1 representing the percentage of run's progress.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "`log_progress` received the value `{}` of type `{}` "
                "which is not supported. "
                "Please pass a valid percentage between [0, 1].".format(
                    value, type(value).__name__
                )
            )
        if value < 0 or value > 1:
            raise ValueError(
                "`log_progress` received an invalid value `{}`. "
                "Please pass a valid percentage between [0, 1].".format(value)
            )
        current_value = self._get_meta_key("progress", 0) or 0
        if current_value == value:
            return
        if (value - current_value < 0.025 and value < 1) and self._throttle_updates():
            return
        self.log_meta(progress=value)

    @client_handler(check_no_op=True)
    def log_code_ref(self, code_ref: Dict = None, is_input: bool = True):
        """Logs code reference as a
        lineage information with the code_ref dictionary in the summary field.

        Args:
            code_ref: dict, optional, if not provided,
                 Polyaxon will detect the code reference from the git repo in the current path.
            is_input: bool, if the code reference is an input or outputs.
        """
        code_ref = code_ref or get_code_reference()
        if code_ref and "commit" in code_ref:
            artifact_run = V1RunArtifact(
                name=code_ref.get("commit"),
                kind=V1ArtifactKind.CODEREF,
                summary=code_ref,
                is_input=is_input,
            )
            self.log_artifact_lineage(body=artifact_run)

    def _calculate_summary_for_path_or_content(
        self,
        hash: str = None,
        path: str = None,
        content=None,
        summary: Dict = None,
        skip_hash_calculation: bool = False,
    ):
        summary = summary or {}
        if hash:
            summary["hash"] = hash
        elif content is not None and not skip_hash_calculation:
            summary["hash"] = hash_value(content)

        if path is not None:
            try:
                if os.path.exists(path):
                    context_root = (
                        ctx_paths.CONTEXT_OFFLINE_ROOT
                        if self._is_offline
                        else ctx_paths.CONTEXT_MOUNT_ARTIFACTS
                    )
                    summary["path"] = os.path.relpath(path, context_root)
                else:
                    summary["path"] = path
            except Exception as e:  # noqa
                logger.debug(
                    "Could not resolve path `%s` "
                    "in _calculate_summary_for_path_or_content. "
                    "Error: %s",
                    path,
                    e,
                )
                summary["path"] = path

            if not summary.get("hash") and not skip_hash_calculation:
                try:
                    if os.path.exists(path):
                        summary["path"] = os.path.abspath(path)
                        summary["hash"] = (
                            hash_file(path) if os.path.isfile(path) else hash_dir(path)
                        )
                    else:
                        summary["path"] = path
                        logger.info(
                            "The path `%s` is not accessible to the tracking module.",
                            path,
                        )
                except Exception as e:
                    logger.warning(
                        "Could not calculate hash for path `%s` "
                        "in _calculate_summary_for_path_or_content. "
                        "Error: %s",
                        path,
                        e,
                    )
        return summary

    @client_handler(check_no_op=True)
    def log_data_ref(
        self,
        name: str,
        hash: str = None,
        path: str = None,
        content=None,
        summary: Dict = None,
        is_input: bool = True,
        skip_hash_calculation: bool = False,
    ):
        """Logs data reference.

        Args:
            name: str, name of the data.
            hash: str, optional, default = None, the hash version of the data,
                 if not provided it will be calculated based on the data in the content.
            path: str, optional, path of where the data is coming from.
            summary: Dict, optional, additional summary information to log about data
                 in the lineage table.
            is_input: bool, optional, if the data reference is an input or outputs.
            content: optional, if the data content is passed, polyaxon will calculate the hash.
            skip_hash_calculation: optional, flag to instruct the client to skip hash calculation.
        """
        return self.log_artifact_ref(
            path=path,
            hash=hash,
            content=content,
            kind=V1ArtifactKind.DATA,
            name=name,
            summary=summary,
            is_input=is_input,
            skip_hash_calculation=skip_hash_calculation,
        )

    @client_handler(check_no_op=True)
    def log_artifact_ref(
        self,
        path: str,
        kind: V1ArtifactKind,
        name: str = None,
        hash: str = None,
        content=None,
        summary: Dict = None,
        is_input: bool = False,
        rel_path: str = None,
        skip_hash_calculation: bool = False,
    ):
        """Logs an artifact reference with custom kind.

        Logging a generic file reference to the lineage table:

        ```python
        >>> # Get outputs artifact path
        >>> asset_path = tracking.get_outputs_path("test.txt")
        >>> with open(asset_path, "w") as f:
        >>>     f.write("Artifact content.")
        >>> # Log reference to the lineage table
        >>> # Name of the artifact will default to test
        >>> tracking.log_artifact_ref(path=asset_path, kind=V1ArtifactKind.FILE)
        ```

        **Note**: This is a generic method that is used by `log_file_ref` and `log_model_ref`.

        Args:
            path: str, filepath, the name is extracted from the filepath
            kind: V1ArtifactKind, the artifact kind
            name: str, if the name is passed it will be used instead of the filename from the path.
            hash: str, optional, default = None, the hash version of the file,
                 if not provided it will be calculated based on the file content
            content: the file content
            summary: Dict, optional, additional summary information to log about data
                 in the lineage table
            is_input: bool, if the file reference is an input or outputs
            rel_path: str, optional relative path to the run artifacts path
            skip_hash_calculation: optional, flag to instruct the client to skip hash calculation
        """
        summary = self._calculate_summary_for_path_or_content(
            hash=hash,
            path=path,
            content=content,
            summary=summary,
            skip_hash_calculation=skip_hash_calculation,
        )
        if path:
            name = name or get_base_filename(path)
            rel_path = self._sanitize_filepath(filepath=path, rel_path=rel_path)
        if name:
            artifact_run = V1RunArtifact(
                name=self._sanitize_filename(name),
                kind=kind,
                path=rel_path,
                summary=summary,
                is_input=is_input,
            )
            self.log_artifact_lineage(body=artifact_run)

    @client_handler(check_no_op=True)
    def log_model_ref(
        self,
        path: str,
        name: str = None,
        framework: str = None,
        summary: Dict = None,
        is_input: bool = False,
        rel_path: str = None,
        skip_hash_calculation: bool = False,
    ):
        """Logs model reference.

         > **Note**: The difference between this method and the `log_model`
         > is that this one does not copy or move the asset, it only registers a lineage reference.
         > If you need the model asset to be on the `artifacts_path` or the `outputs_path`
         > you have to copy it manually using a relative path to
         > `self.get_artifacts_path` or `self.get_outputs_path`.

         ```python
        >>> # Get outputs artifact path
        >>> asset_path = tracking.get_outputs_path("model/model_data.h5")
        >>> with open(asset_path, "w") as f:
        >>>     f.write("Artifact content.")
        >>> # Log reference to the lineage table
        >>> # Name of the artifact will default to model_data
        >>> tracking.log_model_ref(path=asset_path)
        ```

        Args:
            path: str, filepath, the name is extracted from the filepath.
            name: str, if the name is passed it will be used instead of the filename from the path.
            framework: str, optional, name of the framework.
            summary: Dict, optional, additional summary information to log about data
                 in the lineage table.
            is_input: bool, if the file reference is an input or outputs.
            rel_path: str, optional relative path to the run artifacts path.
            skip_hash_calculation: optional, flag to instruct the client to skip hash calculation.
        """
        summary = summary or {}
        summary["framework"] = framework
        self._log_has_model()
        return self.log_artifact_ref(
            path=path,
            kind=V1ArtifactKind.MODEL,
            name=name,
            summary=summary,
            is_input=is_input,
            rel_path=rel_path,
            skip_hash_calculation=skip_hash_calculation,
        )

    @client_handler(check_no_op=True)
    def log_file_ref(
        self,
        path: str,
        name: str = None,
        hash: str = None,
        content=None,
        summary: Dict = None,
        is_input: bool = False,
        rel_path: str = None,
        skip_hash_calculation: bool = False,
    ):
        """Logs file reference.

        Args:
            path: str, filepath, the name is extracted from the filepath.
            name: str, if the name is passed it will be used instead of the filename from the path.
            hash: str, optional, default = None, the hash version of the file,
                 if not provided it will be calculated based on the file content.
            content: the file content.
            summary: Dict, optional, additional summary information to log about data
                 in the lineage table.
            is_input: bool, if the file reference is an input or outputs.
            rel_path: str, optional relative path to the run artifacts path.
            skip_hash_calculation: optional, flag to instruct the client to skip hash calculation.
        """
        return self.log_artifact_ref(
            path=path,
            kind=V1ArtifactKind.FILE,
            name=name,
            hash=hash,
            content=content,
            summary=summary,
            is_input=is_input,
            rel_path=rel_path,
            skip_hash_calculation=skip_hash_calculation,
        )

    @client_handler(check_no_op=True)
    def log_dir_ref(
        self,
        path: str,
        name: str = None,
        hash: str = None,
        summary: Dict = None,
        is_input: bool = False,
        rel_path: str = None,
        skip_hash_calculation: bool = False,
    ):
        """Logs dir reference.

        Args:
            path: str, dir path, the name is extracted from the path.
            name: str, if the name is passed it will be used instead of the dirname from the path.
            hash: str, optional, default = None, the hash version of the file,
                 if not provided it will be calculated based on the file content.
            summary: Dict, optional, additional summary information to log about data
                 in the lineage table.
            is_input: bool, if the dir reference is an input or outputs.
            rel_path: str, optional relative path to the run artifacts path.
            skip_hash_calculation: optional, flag to instruct the client to skip hash calculation.
        """
        return self.log_artifact_ref(
            path=path,
            kind=V1ArtifactKind.DIR,
            name=name or os.path.basename(path),
            hash=hash,
            summary=summary,
            is_input=is_input,
            rel_path=rel_path,
            skip_hash_calculation=skip_hash_calculation,
        )

    def _get_meta_key(self, key: str, default: Any = None):
        if not self.run_data or not self.run_data.meta_info:
            return default
        return self.run_data.meta_info.get(key, default)

    def _has_meta_key(self, key: str):
        return self._get_meta_key(key, False)

    @client_handler(check_no_op=True)
    def log_tensorboard_ref(
        self,
        path: str,
        name: str = "tensorboard",
        is_input: bool = False,
        rel_path: str = None,
    ):
        """Logs tensorboard reference.

        Args:
            path: str, path to the tensorboard logdir.
            name: str, if the name is passed it will be used instead of the dirname from the path.
            is_input: bool, if the tensorboard reference is an input or outputs
            rel_path: str, optional relative path to run the artifacts path.
        """
        if not self._has_meta_key("has_tensorboard"):
            self.log_artifact_ref(
                path=path,
                kind=V1ArtifactKind.TENSORBOARD,
                name=name,
                is_input=is_input,
                rel_path=rel_path,
                skip_hash_calculation=True,
            )
            self.log_meta(has_tensorboard=True)

    @client_handler(check_no_op=True)
    def log_artifact_lineage(
        self,
        body: Union[Dict, List[Dict], V1RunArtifact, List[V1RunArtifact]],
        async_req: bool = True,
    ):
        """Logs an artifact lineage.

        > **Note**: This method can be used to log manual lineage objects, it is used internally
        > to log model/file/artifact/code refs

        Args:
            body: dict or List[dict] or V1RunArtifact or List[V1RunArtifact], body of the lineage.
            async_req: bool, optional, default: False, execute request asynchronously.
        """
        if self._is_offline:
            for b in to_list(body, check_none=True):
                if not isinstance(b, V1RunArtifact):
                    b = V1RunArtifact.read(b)
                self._artifacts_lineage[b.name] = b
            return
        self.client.runs_v1.create_run_artifacts_lineage(
            self.owner,
            self.project,
            self.run_uuid,
            body=body,
            async_req=async_req,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def get_namespace(self):
        """Fetches the run namespace."""
        return self.client.runs_v1.get_run_namespace(
            self.owner,
            self.project,
            self.run_uuid,
        ).namespace

    @client_handler(check_no_op=True, check_offline=True)
    def delete(self):
        """Deletes the current run."""
        return self.client.runs_v1.delete_run(self.owner, self.project, self.run_uuid)

    @client_handler(check_no_op=True, check_offline=True)
    def list(
        self, query: str = None, sort: str = None, limit: int = None, offset: int = None
    ):
        """Lists runs under the current owner - project.

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
    def list_children(
        self, query: str = None, sort: str = None, limit: int = None, offset: int = None
    ):
        """Lists run's children if the current run has a pipeline.

        [Run API](/docs/api/#operation/ListRuns)

        Args:
            query: str, optional, query filters, please refer to
                 [Project PQL](/docs/core/query-language/runs/#query)
            sort: str, optional, fields to order by, please refer to
                 [Project PQL](/docs/core/query-language/runs/#sort)
            limit: int, optional, limit of runs to return.
            offset: int, optional, offset pages to paginate runs.

        Returns:
            List[V1Run], list of run instances.
        """
        params = get_query_params(limit=limit, offset=offset, query=query, sort=sort)
        query = params.get("query")
        query = query + "&" if query else "?"
        query += "pipeline={}".format(self.run_uuid)
        params["query"] = query

        return self.client.runs_v1.list_runs(self.owner, self.project, **params)

    @client_handler(check_no_op=True, check_offline=True)
    def promote_to_model_version(
        self,
        version: str,
        description: str = None,
        tags: Union[str, List[str]] = None,
        content: Union[str, Dict] = None,
        connection: str = None,
        artifacts: List[str] = None,
        force: bool = False,
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Similar to
        [ProjectClient.register_model_version](/docs/core/python-library/project-client/#register_model_version),
        directly from the run client instance,
        allows to create or Update a model version based on the current run.

        **Available from v1.18**

        Args:
            version: str, optional, the version name/tag.
            description: str, optional, the version description.
            tags: str or List[str], optional.
            content: str or dict, optional, content/metadata (JSON object) of the version.
            connection: str, optional, a uuid reference to a connection.
            artifacts: List[str], optional, list of artifacts to highlight(requires passing a run)
            force: bool, optional, to force push, i.e. update if exists.

        Returns:
            V1ProjectVersion, model version.
        """
        from polyaxon.client.project import ProjectClient

        return ProjectClient(self.owner, self.project).register_model_version(
            version=version,
            description=description,
            tags=tags,
            content=content,
            run=self.run_uuid,
            connection=connection,
            artifacts=artifacts,
            force=force,
        )

    @client_handler(check_no_op=True, check_offline=True)
    def promote_to_artifact_version(
        self,
        version: str,
        description: str = None,
        tags: Union[str, List[str]] = None,
        content: Union[str, Dict] = None,
        connection: str = None,
        artifacts: List[str] = None,
        force: bool = False,
    ) -> polyaxon_sdk.V1ProjectVersion:
        """Similar to
        [ProjectClient.register_artifact_version](/docs/core/python-library/project-client/#register_artifact_version),
        directly from the run client instance,
        allows to create or Update an artifact version based on the current run.

        **Available from v1.18**

        Args:
            version: str, optional, the version name/tag.
            description: str, optional, the version description.
            tags: str or List[str], optional.
            content: str or dict, optional, content/metadata (JSON object) of the version.
            connection: str, optional, a uuid reference to a connection.
            artifacts: List[str], optional, list of artifacts to highlight(requires passing a run)
            force: bool, optional, to force push, i.e. update if exists.

        Returns:
            V1ProjectVersion, artifact version.
        """
        from polyaxon.client.project import ProjectClient

        return ProjectClient(self.owner, self.project).register_artifact_version(
            version=version,
            description=description,
            tags=tags,
            content=content,
            run=self.run_uuid,
            connection=connection,
            artifacts=artifacts,
            force=force,
        )

    def _collect_events_summaries(
        self,
        events_path: str,
        events_kind: str,
        last_check: Optional[datetime],
        is_system_resource: bool = False,
    ) -> Tuple[List, Dict]:
        current_events_path = os.path.join(events_path, events_kind)

        summaries = []
        last_values = {}
        connection_name = get_artifacts_store_name()
        with get_files_in_path_context(current_events_path) as files:
            for f in files:
                if last_check and not file_modified_since(
                    filepath=f, last_time=last_check
                ):
                    continue

                event_name = os.path.basename(f).split(".plx")[0]
                event = V1Events.read(kind=events_kind, name=event_name, data=f)
                if event.df.empty:
                    continue

                # Get only the relpath from run uuid
                event_rel_path = self._sanitize_filepath(filepath=f)
                summary = event.get_summary()
                run_artifact = V1RunArtifact(
                    name=event_name,
                    kind=V1ArtifactKind.SYSTEM if is_system_resource else events_kind,
                    connection=connection_name,
                    summary=summary,
                    path=event_rel_path,
                    is_input=False,
                )
                summaries.append(run_artifact)
                if events_kind == V1ArtifactKind.METRIC:
                    last_values[event_name] = summary[V1ArtifactKind.METRIC]["last"]

        return summaries, last_values

    def _sync_events_summaries(
        self,
        last_check: Optional[datetime],
        events_path: str,
        is_system_resource: bool = False,
    ):
        # check if there's a path to sync
        if not events_path or not os.path.exists(events_path):
            return

        # crawl dirs
        summaries = []
        last_values = {}
        set_last_values = not is_system_resource

        for events_kind in get_dirs_under_path(events_path):
            _summaries, _last_values = self._collect_events_summaries(
                events_path=events_path,
                events_kind=events_kind,
                last_check=last_check,
                is_system_resource=is_system_resource,
            )
            summaries += _summaries
            if set_last_values:
                last_values.update(_last_values)

        if summaries:
            self.log_artifact_lineage(summaries)
        if set_last_values and last_values:
            self.log_outputs(**last_values)

    @client_handler(check_no_op=True)
    def sync_events_summaries(self, last_check: Optional[datetime], events_path: str):
        """Syncs all tracked events and auto-generates summaries and lineage data.

        > **Note**: Both `in-cluster` and `offline` modes will manage syncing events summaries
        > automatically, so you should not call this method manually.
        """
        self._sync_events_summaries(
            last_check=last_check,
            events_path=events_path,
            is_system_resource=False,
        )

    @client_handler(check_no_op=True)
    def sync_system_events_summaries(
        self, last_check: Optional[datetime], events_path: str
    ):
        """Syncs all tracked system events and auto-generates summaries and lineage data.

        > **Note**: Both `in-cluster` and `offline` modes will manage syncing events summaries
        > automatically, so you should not call this method manually.
        """
        self._sync_events_summaries(
            last_check=last_check,
            events_path=events_path,
            is_system_resource=True,
        )

    @client_handler(check_no_op=True)
    def persist_run(self, path: str):
        """Persists a run to a local path.

        > **Note**: You generally do not need to call this method manually,
        > When the `offline` mode is enabled, this method is triggered automatically at the end.

        Args:
            path: str, The path where to persist the run's metadata.
        """
        if not self.run_data:
            logger.debug(
                "Persist offline run call failed. "
                "Make sure that the offline mode is enabled and that run_data is provided."
            )
            return
        if not path or not os.path.exists(path):
            check_or_create_path(path, is_dir=True)
        run_path = "{}/{}".format(path, ctx_paths.CONTEXT_LOCAL_RUN)
        with open(run_path, "w") as config_file:
            config_file.write(
                ujson.dumps(self.client.sanitize_for_serialization(self.run_data))
            )

        if not self._artifacts_lineage:
            logger.debug("Persist offline run call did not find any lineage data. ")
            return

        lineages_path = "{}/{}".format(path, ctx_paths.CONTEXT_LOCAL_LINEAGES)
        with open(lineages_path, "w") as config_file:
            config_file.write(
                ujson.dumps(
                    [
                        self.client.sanitize_for_serialization(l)
                        for l in self._artifacts_lineage.values()
                    ]
                )
            )

    @classmethod
    @client_handler(check_no_op=True)
    def load_offline_run(
        cls,
        path: str,
        run_client: Union["RunClient", "Run"] = None,
        reset_project: bool = False,
        raise_if_not_found: bool = False,
    ) -> Union["RunClient", "Run"]:
        """Loads an offline run from a local path.

        > **Note**: When the `offline` mode is enabled, and the run uuid is provided,
        > this method is triggered automatically to load last checkpoint.

        Args:
            path: str, The path where the run's metadata is persisted.
            run_client: RunClient, optional, instance of the client to update with
                 the loaded run's information.
            reset_project: bool, optional, a flag to reset the run's owner and/or project based on
                 the data from the passed `run_client` instead of the persisted data
                 from the local run.
            raise_if_not_found: bool, optional, a flag to raise an error if the local path does not
                 contain a persisted run.
        """
        run_path = "{}/{}".format(path, ctx_paths.CONTEXT_LOCAL_RUN)
        if not os.path.isfile(run_path):
            if raise_if_not_found:
                raise PolyaxonClientException(f"Offline data was not found: {run_path}")
            else:
                logger.info(f"Offline data was not found: {run_path}")
                return

        with open(run_path, "r") as config_file:
            config_str = config_file.read()
            run_config = polyaxon_sdk.V1Run(**ujson.loads(config_str))
            owner = run_config.owner
            project = run_config.project
            if reset_project or not owner:
                owner = run_client.owner
            if reset_project or not project:
                project = run_client.project
            if run_client:
                run_client._owner = owner
                run_client._project = project
                run_client._run_uuid = run_config.uuid
            else:
                run_client = cls(
                    owner=owner,
                    project=project,
                    run_uuid=run_config.uuid,
                )
            run_client._run_data = run_config
            logger.info(f"Offline data loaded from: {run_path}")

        lineages_path = "{}/{}".format(path, ctx_paths.CONTEXT_LOCAL_LINEAGES)
        if not os.path.isfile(lineages_path):
            logger.info(f"Offline lineage data was not found: {lineages_path}")
            return run_client
        with open(lineages_path, "r") as config_file:
            config_str = config_file.read()
            lineages = [
                V1RunArtifact.from_dict(l, unknown=EXCLUDE)
                for l in ujson.loads(config_str)
            ]
            run_client._artifacts_lineage = {l.name: l for l in lineages}
            logger.info(f"Offline lineage data loaded from: {lineages_path}")

        return run_client

    @client_handler(check_no_op=True)
    def pull_remote_run(
        self,
        path: str = None,
        download_artifacts: bool = True,
    ):
        """Download a run on Polyaxon's API and artifacts store to local path.

        Args:
            path: str, optional, defaults to the offline root path,
                 path where the run's metadata & artifacts will be stored.
            download_artifacts: bool, optional, flag to trigger artifacts download.
        """
        path = ctx_paths.get_offline_path(
            entity_value=self.run_uuid, entity_kind=V1ProjectFeature.RUNTIME, path=path
        )
        delete_path(path)
        self.refresh_data(load_artifacts_lineage=True, load_conditions=True)
        if download_artifacts:
            self.download_artifacts(path_to=path)
        self.persist_run(path)
        return path

    @client_handler(check_no_op=True)
    def push_offline_run(
        self,
        path: str,
        upload_artifacts: bool = True,
        clean: bool = False,
    ):
        """Syncs an offline run to Polyaxon's API and artifacts store.


        Args:
            path: str, root path where the run's metadata & artifacts are stored.
            upload_artifacts: bool, optional, flag to trigger artifacts upload.
            clean: bool, optional, flag to clean local path after pushing the run.
        """
        # We ensure that the is_offline is False
        is_offline = self._is_offline
        self._is_offline = False

        if not self.run_data:
            logger.warning(
                "Push offline run failed. Make sure that run_data is provided."
            )
            return
        self.client.runs_v1.sync_run(
            owner=self.owner,
            project=self.project,
            body=self.run_data,
            async_req=False,
        )
        logger.info(f"Offline data for run {self.run_data.uuid} synced")
        if self._artifacts_lineage:
            self.log_artifact_lineage(
                [l for l in self._artifacts_lineage.values()], async_req=False
            )
            logger.info(f"Offline lineage data for run {self.run_data.uuid} synced")
        else:
            logger.warning("Push offline run failed. No lineage data found.")
            return

        if path and upload_artifacts:
            self.upload_artifacts_dir(
                dirpath=path,
                path="/",
                overwrite=True,
                relative_to=path,
            )
            logger.info(f"Offline artifacts for run {self.run_data.uuid} uploaded")

        if clean:
            delete_path(path)

        # Reset is_offline
        self._is_offline = is_offline


def get_run_logs(
    client: RunClient,
    hide_time: bool = False,
    all_containers: bool = False,
    all_info: bool = False,
    follow: bool = False,
):
    def get_logs(last_file=None, last_time=None):
        try:
            response = client.get_logs(last_file=last_file, last_time=last_time)
            get_logs_streamer(
                show_timestamp=not hide_time,
                all_containers=all_containers,
                all_info=all_info,
            )(response)
            return response
        except (ApiException, HTTPError) as e:
            if not follow:
                handle_cli_error(
                    e,
                    message="Could not get logs for run `{}`.".format(client.run_uuid),
                )
                sys.exit(1)

    def handle_status(last_status: str = None, live_update=None):
        if not last_status:
            return {"status": None}

        if live_update:
            live_update.update(
                status="{}".format(
                    Printer.add_status_color(
                        {"status": last_status}, status_key="status"
                    )["status"]
                )
            )
        else:
            Printer.print(
                "{}".format(
                    Printer.add_status_color(
                        {"status": last_status}, status_key="status"
                    )["status"]
                )
            )
        return last_status

    def handle_logs():
        is_done = False
        last_file = None
        _status = None
        files = []
        last_transition_time = now()
        last_status, conditions = client.get_statuses()
        if conditions:
            last_transition_time = conditions[0].last_transition_time

        with Printer.console.status("Waiting for running condition ...") as live_update:
            while not LifeCycle.is_done(last_status) and not LifeCycle.is_running(
                last_status
            ):
                time.sleep(settings.CLIENT_CONFIG.watch_interval)
                last_status, conditions = client.get_statuses()
                if conditions:
                    last_transition_time = conditions[0].last_transition_time
                if _status != last_status:
                    _status = handle_status(last_status, live_update)

        if LifeCycle.is_done(last_status):
            last_time = None
        else:
            last_time = last_transition_time

        checks = 0
        while not is_done:
            response = get_logs(last_time=last_time, last_file=last_file)

            if response:
                last_time = response.last_time
                last_file = response.last_file
                files = response.files
            else:
                last_time = None
                last_file = None

            # Follow logic
            if not any([last_file, last_time]) or checks > 3:
                if follow:
                    last_status, _ = client.get_statuses()
                    if _status != last_status:
                        _status = handle_status(last_status)
                    is_done = LifeCycle.is_done(last_status)
                    if not is_done:
                        checks = 0
                else:
                    is_done = True
            if last_time and not follow:
                is_done = True

            if not is_done:
                if last_file:
                    if len(files) > 1 and last_file != files[-1]:
                        time.sleep(1)
                    else:
                        is_done = True
                else:
                    time.sleep(settings.CLIENT_CONFIG.watch_interval)
            checks += 1

    handle_logs()
