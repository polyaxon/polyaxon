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
import sys
import time
import uuid

from collections.abc import Mapping
from datetime import datetime
from typing import Dict, List, Optional, Sequence, Tuple, Union

import click
import polyaxon_sdk
import ujson

from polyaxon_sdk import V1Run
from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon import settings
from polyaxon.cli.errors import handle_cli_error
from polyaxon.client.client import PolyaxonClient
from polyaxon.client.decorators import client_handler
from polyaxon.constants.metadata import META_COPY_ARTIFACTS
from polyaxon.containers.contexts import CONTEXT_MOUNT_ARTIFACTS, CONTEXT_OFFLINE_ROOT
from polyaxon.env_vars.getters import (
    get_artifacts_store_name,
    get_project_error_message,
    get_project_or_local,
    get_run_info,
    get_run_or_local,
)
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.lifecycle import LifeCycle, V1StatusCondition, V1Statuses
from polyaxon.logger import logger
from polyaxon.managers.ignore import IgnoreConfigManager
from polyaxon.polyaxonfile import check_polyaxonfile
from polyaxon.polyboard.artifacts import V1ArtifactKind, V1RunArtifact
from polyaxon.polyboard.events import V1Events
from polyaxon.polyboard.logging.streamer import get_logs_streamer
from polyaxon.polyflow import V1Matrix, V1Operation, V1RunKind
from polyaxon.schemas.types import V1ArtifactsType
from polyaxon.stores.polyaxon_store import PolyaxonStore
from polyaxon.utils.code_reference import get_code_reference
from polyaxon.utils.date_utils import file_modified_since
from polyaxon.utils.formatting import Printer
from polyaxon.utils.fqn_utils import get_entity_full_name, to_fqn_name
from polyaxon.utils.hashing import hash_value
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
from polyaxon.utils.validation import validate_tags


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
    ):
        self._is_offline = (
            is_offline if is_offline is not None else settings.CLIENT_CONFIG.is_offline
        )
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
        self._lineages = {}

    @property
    def client(self):
        if self._client:
            return self._client
        self._client = PolyaxonClient()
        return self._client

    @property
    def status(self) -> str:
        return self._run_data.status

    @property
    def namespace(self) -> str:
        if self._namespace:
            return self._namespace
        if (
            self.run_data
            and self.run_data.settings
            and self.run_data.settings.namespace
        ):
            self._namespace = self.run_data.settings.namespace
        else:
            self._namespace = self.get_namespace()
        return self._namespace

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def project(self) -> str:
        return self._project

    @property
    def run_uuid(self) -> str:
        return self._run_uuid

    @property
    def run_data(self):
        return self._run_data

    @client_handler(check_no_op=True)
    def get_inputs(self) -> Dict:
        """Gets the run's inputs.
        Returns:
            dict, all the run inputs/params.
        """
        return self._run_data.inputs

    @client_handler(check_no_op=True)
    def get_outputs(self) -> Dict:
        """Gets the run's outputs.
        Returns:
             dict, all the run outputs/metrics.
        """
        return self._run_data.outputs

    @client_handler(check_no_op=True, check_offline=True)
    def refresh_data(self):
        """Fetches the run data from the api."""
        self._run_data = self.client.runs_v1.get_run(
            self.owner, self.project, self.run_uuid
        )

    def _update(
        self, data: Union[Dict, polyaxon_sdk.V1Run], async_req: bool = True
    ) -> V1Run:
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
    ) -> V1Run:
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

    def _create(
        self, data: Union[Dict, polyaxon_sdk.V1OperationBody], async_req: bool = False
    ) -> V1Run:
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
            self._lineages = {}
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
    ) -> V1Run:
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
        tags = validate_tags(tags)
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
    ) -> V1Run:
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
    ) -> V1Run:
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
    ) -> V1Run:
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
        N.B. If you are executing a managed run, you don't need to call this method manually.
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
            if status == polyaxon_sdk.V1Statuses.CREATED:
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
            last_status, _conditions = self.get_statuses(last_status)
            yield last_status, _conditions

    @client_handler(check_no_op=True, check_offline=True)
    def wait_for_condition(
        self, statuses: List[str] = None, print_status: bool = False
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
        logger.warning("This method is deprecated in favor of `get_multi_run_events`")
        return self.get_multi_run_events(
            kind=kind, runs=runs, names=names, orient=orient, force=force
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
        """Gets multi-run events.

        Args:
            kind: str, a valid `V1ArtifactKind`.
            runs: List[str], list of run uuids to return events for.
            names: List[str], list of events to return.
            orient: str, csv or dict.
            force: bool, force reload the events.
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
    def download_artifact(self, path: str, force: bool = False, path_to: str = None):
        """Downloads a single run artifact.

        Args:
            path: str, the relative path of the artifact to return.
            path_to: str, optional, path to download to.
            force: bool, force reload the artifact.

        Returns:
            str
        """
        url = PolyaxonStore.URL.format(
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            uuid=self.run_uuid,
            subpath="artifact",
        )
        url = absolute_uri(url=url, host=self.client.config.host)
        if force:
            url = "{}?force=true".format(url)

        return PolyaxonStore(client=self).download_file(
            url=url, path=path, path_to=path_to
        )

    @client_handler(check_no_op=True, check_offline=True)
    def download_artifacts(
        self,
        path: str = "",
        path_to: str = None,
        untar: bool = True,
        delete_tar: bool = True,
        extract_path: str = None,
    ):
        """Downloads a subpath containing multiple run artifacts.

        Args:
            path: str, the relative path of the artifact to return.
            path_to: str, optional, path to download to.
            untar: bool, optional, default: true.
            delete_tar: bool, optional, default: true.
            extract_path: str, optional.

        Returns:
            str.
        """
        url = PolyaxonStore.URL.format(
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            uuid=self.run_uuid,
            subpath="artifacts",
        )
        url = absolute_uri(url=url, host=self.client.config.host)

        return PolyaxonStore(client=self).download_file(
            url=url,
            path=path,
            untar=untar,
            path_to=path_to,
            delete_tar=delete_tar and untar,
            extract_path=extract_path,
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
        url = PolyaxonStore.URL.format(
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            uuid=self.run_uuid,
            subpath="artifact",
        )
        url = absolute_uri(url=url, host=self.client.config.host)

        return PolyaxonStore(client=self).upload_file(
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

        > This function crawls all files to upload and uses `upload_artifacts`.

        Args:
            dirpath: str, the dirpath to upload.
            path: str, the relative path of the artifact to return.
            overwrite: bool, optional, if the file uploaded should overwrite any previous content.
            relative_to: str, optional, if the path uploaded is not the current dir,
                 and you want to cancel the relative path.

        Returns:
            str.
        """
        files = IgnoreConfigManager.get_unignored_filepaths(dirpath)
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
        """Uploads a multiple artifacts to the run's artifacts store path.

        Args:
            files: List[str], list of files to upload.
            path: str, the relative path of the artifact to return.
            overwrite: bool, optional, if the file uploaded should overwrite any previous content.
            relative_to: str, optional, if the path uploaded is not the current dir,
                 and you want to cancel the relative path.

        Returns:
            str.
        """
        url = PolyaxonStore.URL.format(
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            uuid=self.run_uuid,
            subpath="artifacts",
        )
        url = absolute_uri(url=url, host=self.client.config.host)

        return PolyaxonStore(client=self).upload_dir(
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
        """Stops the current run."""
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
            tags = validate_tags(tags)
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
        tags = validate_tags(tags)
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
        N.B. If you are executing a managed run, you don't need to call this method manually.
        This method is only useful for manual runs outside of Polyaxon.
        </blockquote>
        """
        self.log_status(polyaxon_sdk.V1Statuses.RUNNING, message="Operation is running")

    def _log_end_status(
        self,
        status: str,
        reason: str = None,
        message: str = None,
    ):
        """Sets the current run to `status` status.

        <blockquote class="info">
        N.B. If you are executing a managed run, you don't need to call this method manually.
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
        N.B. If you are executing a managed run, you don't need to call this method manually.
        This method is only useful for manual runs outside of Polyaxon.
        </blockquote>
        """
        self._log_end_status(status=polyaxon_sdk.V1Statuses.SUCCEEDED, message=message)

    @client_handler(check_no_op=True)
    def log_stopped(self, message="Operation is stopped"):
        """Sets the current run to `stopped` status.

        <blockquote class="info">
        N.B. If you are executing a managed run, you don't need to call this method manually.
        This method is only useful for manual runs outside of Polyaxon.
        </blockquote>
        """
        self._log_end_status(status=polyaxon_sdk.V1Statuses.STOPPED, message=message)

    @client_handler(check_no_op=True)
    def log_failed(self, reason: str = None, message: str = None):
        """Sets the current run to `failed` status.

        <blockquote class="info">
        N.B. If you are executing a managed run, you don't need to call this method manually.
        This method is only useful for manual runs outside of Polyaxon.
        </blockquote>

        Args:
            reason: str, optional, reason or service issuing the status change.
            message: str, optional, message to log with this status.
        """
        self._log_end_status(
            status=polyaxon_sdk.V1Statuses.FAILED,
            reason=reason,
            message=message,
        )

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
    def log_code_ref(self, code_ref: Dict = None, is_input: bool = True):
        """Logs code reference as a
        lineage information with the code_ref dictionary in the summary field.

        In offline

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

    @client_handler(check_no_op=True)
    def log_data_ref(
        self,
        name: str,
        hash: str = None,
        path: str = None,
        content=None,
        summary: Dict = None,
        is_input: bool = True,
    ):
        """Logs data reference.

        Args:
            name: str, name of the data.
            hash: str, optional, default = None, the hash version of the data,
                 if not provided it will be calculated based on the data in the content.
            path: str, optional, path of where the data is coming from.
            summary: Dict, optional, additional summary information to log about data
                 in the lineage table.
            is_input: bool, if the data reference is an input or outputs.
            content: the data content.
        """
        summary = summary or {}
        if hash:
            summary["hash"] = hash
        elif content is not None:
            summary["hash"] = hash_value(content)
        if path is not None:
            summary["path"] = path
        if name:
            artifact_run = V1RunArtifact(
                name=name,
                kind=V1ArtifactKind.DATA,
                path=path,
                summary=summary,
                is_input=is_input,
            )
            self.log_artifact_lineage(body=artifact_run)

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
            path: str, filepath, the name is extracted from the filepath.
            kind: V1ArtifactKind, the artifact kind.
            name: str, if the name is passed it will be used instead of the filename from the path.
            hash: str, optional, default = None, the hash version of the file,
                 if not provided it will be calculated based on the file content.
            content: the file content.
            summary: Dict, optional, additional summary information to log about data
                 in the lineage table.
            is_input: bool, if the file reference is an input or outputs.
            rel_path: str, optional relative path to the run artifacts path.
        """
        summary = summary or {}
        summary["path"] = path
        if hash:
            summary["hash"] = hash
        elif content is not None:
            summary["hash"] = hash_value(content)
        name = name or get_base_filename(path)
        rel_path = get_rel_asset_path(
            path=path, rel_path=rel_path, is_offline=self._is_offline
        )
        if name:
            artifact_run = V1RunArtifact(
                name=to_fqn_name(name),
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
            framework: str, optional ,name of the framework
            summary: Dict, optional, additional summary information to log about data
                 in the lineage table.
            is_input: bool, if the file reference is an input or outputs.
            rel_path: str, optional relative path to the run artifacts path.
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
        )

    @client_handler(check_no_op=True)
    def log_dir_ref(
        self,
        path: str,
        name: str = None,
        summary: Dict = None,
        is_input: bool = False,
        rel_path: str = None,
    ):
        """Logs dir reference.

        Args:
            path: str, dir path, the name is extracted from the path.
            name: str, if the name is passed it will be used instead of the dirname from the path.
            summary: Dict, optional, additional summary information to log about data
                 in the lineage table.
            is_input: bool, if the dir reference is an input or outputs.
            rel_path: str, optional relative path to the run artifacts path.
        """
        name = name or os.path.basename(path)
        rel_path = get_rel_asset_path(
            path=path, rel_path=rel_path, is_offline=self._is_offline
        )
        summary = summary or {}
        summary["path"] = path
        if name:
            artifact_run = V1RunArtifact(
                name=to_fqn_name(name),
                kind=V1ArtifactKind.DIR,
                path=rel_path,
                summary=summary,
                is_input=is_input,
            )
            self.log_artifact_lineage(body=artifact_run)

    def _has_meta_key(self, key: str):
        return (
            self.run_data
            and self.run_data.meta_info
            and self.run_data.meta_info.get(key, False)
        )

    @client_handler(check_no_op=True)
    def log_tensorboard_ref(
        self,
        path: str,
        name: str = "tensorboard",
        is_input: bool = False,
        rel_path: str = None,
    ):
        """Logs dir reference.

        Args:
            path: str, path to the tensorboard logdir.
            name: str, if the name is passed it will be used instead of the dirname from the path.
            is_input: bool, if the tensorboard reference is an input or outputs
            rel_path: str, optional relative path to run the artifacts path.
        """
        if not self._has_meta_key("has_tensorboard"):
            rel_path = get_rel_asset_path(
                path=path, rel_path=rel_path, is_offline=self._is_offline
            )
            artifact_run = V1RunArtifact(
                name=to_fqn_name(name),
                kind=V1ArtifactKind.TENSORBOARD,
                path=rel_path,
                summary={"path": path},
                is_input=is_input,
            )
            self.log_artifact_lineage(body=artifact_run)
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
                self._lineages[b.name] = b
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
                event_rel_path = get_rel_asset_path(path=f, is_offline=self._is_offline)
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
    def persist_offline_run(self, artifacts_path: str):
        """Persists an offline run to a local path.

        > **Note**: You generally do not need to call this method manually,
        > When the `offline` mode is enabled, this method is triggered automatically at the end.
        """
        if not self._is_offline or not self.run_data:
            logger.debug(
                "Persist offline run call failed. "
                "Make sure that the offline mode is enabled and that run_data is provided."
            )
            return
        if not artifacts_path or not os.path.exists(artifacts_path):
            check_or_create_path(artifacts_path, is_dir=True)
        run_path = "{}/run_data.json".format(artifacts_path)
        with open(run_path, "w") as config_file:
            config_file.write(
                ujson.dumps(self.client.sanitize_for_serialization(self.run_data))
            )

        if not self._lineages:
            logger.debug("Persist offline run call did not find any lineage data. ")
            return

        lineages_path = "{}/lineages.json".format(artifacts_path)
        with open(lineages_path, "w") as config_file:
            config_file.write(
                ujson.dumps(
                    [
                        self.client.sanitize_for_serialization(l)
                        for l in self._lineages.values()
                    ]
                )
            )

    @classmethod
    @client_handler(check_no_op=True)
    def load_offline_run(
        cls, artifacts_path: str, run_client: Union["RunClient", "Run"] = None
    ) -> Union["RunClient", "Run"]:
        """Loads an offline run from a local path.

        > **Note**: When the `offline` mode is enabled, and the run uuid is provided,
        > this method is triggered automatically to load last checkpoint.
        """
        run_path = "{}/run_data.json".format(artifacts_path)
        if not os.path.isfile(run_path):
            logger.info(f"Offline data was not found: {run_path}")
            return
        with open(run_path, "r") as config_file:
            config_str = config_file.read()
            run_config = polyaxon_sdk.V1Run(**ujson.loads(config_str))
            if run_client:
                run_client._owner = run_config.owner
                run_client._project = run_config.project
                run_client._run_uuid = run_config.uuid
            else:
                run_client = cls(
                    owner=run_config.owner,
                    project=run_config.project,
                    run_uuid=run_config.uuid,
                )
            run_client._run_data = run_config
            logger.info(f"Offline data loaded from: {run_path}")

        lineages_path = "{}/lineages.json".format(artifacts_path)
        if not os.path.isfile(lineages_path):
            logger.info(f"Offline lineage data was not found: {lineages_path}")
            return
        with open(lineages_path, "r") as config_file:
            config_str = config_file.read()
            lineages = [V1RunArtifact(**l) for l in ujson.loads(config_str)]
            run_client._lineages = {l.name: l for l in lineages}
            logger.info(f"Offline lineage data loaded from: {run_path}")

        return run_client

    @client_handler(check_no_op=True)
    def sync_offline_run(
        self,
        artifacts_path: str = None,
        load_offline_run: bool = False,
        upload_artifacts: bool = True,
        clean: bool = False,
    ):
        """Syncs an offline run to Polyaxon's API and artifacts store."""
        if artifacts_path and load_offline_run:
            self._run_uuid = None
            self._run_data = None
            self.load_offline_run(artifacts_path=artifacts_path, run_client=self)

        # We ensure that the is_offline is False
        is_offline = self._is_offline
        self._is_offline = False

        if not self.run_data:
            logger.warning(
                "Sync offline run failed. Make sure that run_data is provided."
            )
            return
        self.client.runs_v1.sync_run(
            owner=self.owner,
            project=self.project,
            body=self.run_data,
            async_req=False,
        )
        logger.info(f"Offline data for run {self.run_data.uuid} synced")
        if self._lineages:
            self.log_artifact_lineage(
                [l for l in self._lineages.values()], async_req=False
            )
            logger.info(f"Offline lineage data for run {self.run_data.uuid} synced")
        else:
            logger.info("Sync offline run failed. No lineage data found.")
            return

        if artifacts_path and upload_artifacts:
            self.upload_artifacts_dir(
                dirpath=artifacts_path,
                path="/",
                overwrite=True,
                relative_to=artifacts_path,
            )
            logger.info(f"Offline artifacts for run {self.run_data.uuid} uploaded")

        if clean:
            delete_path(artifacts_path)

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

    def handle_status(last_status: str = None):
        if not last_status:
            return {"status": None}

        click.echo(
            "{}".format(
                Printer.add_status_color({"status": last_status}, status_key="status")[
                    "status"
                ]
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

        while not LifeCycle.is_done(last_status) and not LifeCycle.is_running(
            last_status
        ):
            time.sleep(settings.CLIENT_CONFIG.watch_interval)
            last_status, conditions = client.get_statuses()
            if conditions:
                last_transition_time = conditions[0].last_transition_time
            if _status != last_status:
                _status = handle_status(last_status)

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


def get_rel_asset_path(
    path: str = None, rel_path: str = None, is_offline: bool = False
):
    if not path or rel_path:
        return rel_path
    artifacts_root = CONTEXT_OFFLINE_ROOT if is_offline else CONTEXT_MOUNT_ARTIFACTS
    if artifacts_root in path:
        try:
            return os.path.relpath(path, artifacts_root)
        except Exception as e:
            logger.debug("could not calculate relative path %s", e)

    return rel_path or path
