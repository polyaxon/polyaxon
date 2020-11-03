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

import os
import sys
import time

from collections.abc import Mapping
from typing import Dict, List, Sequence, Tuple, Union

import click
import polyaxon_sdk

from polyaxon_sdk import V1Run
from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon import settings
from polyaxon.cli.errors import handle_cli_error
from polyaxon.client import PolyaxonClient
from polyaxon.client.decorators import check_no_op, check_offline
from polyaxon.containers.contexts import CONTEXT_MOUNT_ARTIFACTS
from polyaxon.env_vars.getters import (
    get_project_full_name,
    get_project_or_local,
    get_run_info,
    get_run_or_local,
)
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.lifecycle import LifeCycle, V1StatusCondition
from polyaxon.logger import logger
from polyaxon.polyaxonfile import check_polyaxonfile
from polyaxon.polyboard.artifacts import V1ArtifactKind, V1RunArtifact
from polyaxon.polyboard.logging.handler import get_logs_handler
from polyaxon.polyflow import V1Operation
from polyaxon.stores.polyaxon_store import PolyaxonStore
from polyaxon.utils.code_reference import get_code_reference
from polyaxon.utils.formatting import Printer
from polyaxon.utils.hashing import hash_value
from polyaxon.utils.http_utils import clean_host
from polyaxon.utils.list_utils import to_list
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

    @check_no_op
    def __init__(
        self,
        owner: str = None,
        project: str = None,
        run_uuid: str = None,
        client: PolyaxonClient = None,
    ):

        try:
            owner, project = get_project_or_local(
                get_project_full_name(owner=owner, project=project)
            )
        except PolyaxonClientException:
            pass

        if project is None:
            if settings.CLIENT_CONFIG.is_managed:
                owner, project, _run_uuid = get_run_info()
                run_uuid = run_uuid or _run_uuid
            else:
                raise PolyaxonClientException("Please provide a valid project.")

        if not owner or not project:
            raise PolyaxonClientException("Please provide a valid project with owner.")

        self.client = client
        if not (self.client or settings.CLIENT_CONFIG.is_offline):
            self.client = PolyaxonClient()

        self._owner = owner
        self._project = project
        self._run_uuid = get_run_or_local(run_uuid)
        self._run_data = polyaxon_sdk.V1Run()
        self._namespace = None

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
            self._namespace = self.run_data.settings
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

    @check_no_op
    def get_inputs(self) -> Dict:
        """Gets the run's inputs.
        Returns:
            dict, all the run inputs/params.
        """
        return self._run_data.inputs

    @check_no_op
    def get_outputs(self) -> Dict:
        """Gets the run's outputs.
        Returns:
             dict, all the run outputs/metrics.
        """
        return self._run_data.outputs

    @check_no_op
    @check_offline
    def refresh_data(self):
        """Fetches the run data from the api."""
        self._run_data = self.client.runs_v1.get_run(
            self.owner, self.project, self.run_uuid
        )

    def _update(
        self, data: Union[Dict, polyaxon_sdk.V1Run], async_req: bool = True
    ) -> V1Run:
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

    @check_no_op
    @check_offline
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
        return self._update(data=data, async_req=async_req)

    @check_no_op
    @check_offline
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
        return response

    def _post_create(self):
        pass

    @check_no_op
    @check_offline
    def create(
        self,
        name: str = None,
        description: str = None,
        tags: Union[str, Sequence[str]] = None,
        content: Union[str, Dict, V1Operation] = None,
        is_managed: bool = True,
    ) -> V1Run:
        """Creates a new run based on the data passed.

        N.B. Create methods are only useful if you want to create a run programmatically,
        if you run a component/operation from the CLI/UI an instance will be created automatically.

        This is a generic create function, you can check other methods for creating runs:
          * from yaml: `create_from_polyaxonfile`
          * from url: `create_from_url`
          * from hub: `create_from_hub`

        > Note that if you don't pass `content`, the creation will pass,
        and the run will be marked as non-managed.

        [Run API](/docs/api/#operation/CreateRun)

        Args:
            name: str, optional, it will override the name in the operation if provided.
            description: str, optional,
                it will override the description in the operation if provided.
            tags: str or List[str], optional, list of tags,
                it will override the tags in the operation if provided.
            content: str or Dict or V1Operation, optional.
            is_managed: bool flag to create a managed run.

        Returns:
            V1Run, run instance from the response.
        """
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
        )
        self._create(data=data, async_req=False)
        self._post_create()
        return self.run_data

    @check_no_op
    @check_offline
    def create_from_polyaxonfile(
        self,
        polyaxonfile: str,
        name: str = None,
        description: str = None,
        tags: Union[str, Sequence[str]] = None,
        params: Dict = None,
        presets: List[str] = None,
        queue: str = None,
        nocache: bool = None,
        cache: bool = None,
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
            presets: List[str], optional, the name of the
                [presets](/docs/core/introduction/concepts/#preset).
            queue: str, optional, the name of the
                [queue](/docs/core/scheduling-strategies/queue-routing/) to assign the run to.
            nocache: bool, optional, simple flag to disable
                [cache check](/docs/automation/helpers/cache/).
                If passed and the Polyaxonfile has cache section,
                it will be patched with `disabled: true`.
            cache: bool, optional, simple flag to enable
                [cache check](/docs/automation/helpers/cache/).
                If passed and the Polyaxonfile has cache section,
                it will be patched with `disabled: false`.

        Returns:
            V1Run, run instance from the response.
        """
        op_spec = check_polyaxonfile(
            polyaxonfile=polyaxonfile,
            params=params,
            presets=presets,
            queue=queue,
            nocache=nocache,
            cache=cache,
            verbose=False,
        )
        return self.create(
            name=name, description=description, tags=tags, content=op_spec
        )

    @check_no_op
    @check_offline
    def create_from_url(
        self,
        url: str,
        name: str = None,
        description: str = None,
        tags: Union[str, Sequence[str]] = None,
        params: Dict = None,
        presets: List[str] = None,
        queue: str = None,
        nocache: bool = None,
        cache: bool = None,
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
            presets: List[str], optional, the name of the
                [presets](/docs/core/introduction/concepts/#preset).
            queue: str, optional, the name of the
                [queue](/docs/core/scheduling-strategies/queue-routing/) to assign the run to.
            nocache: bool, optional, simple flag to disable
                [cache check](/docs/automation/helpers/cache/).
                If passed and the Polyaxonfile has cache section,
                it will be patched with `disabled: true`.
            cache: bool, optional, simple flag to enable
                [cache check](/docs/automation/helpers/cache/).
                If passed and the Polyaxonfile has cache section,
                it will be patched with `disabled: false`.

        Returns:
            V1Run, run instance from the response.
        """
        op_spec = check_polyaxonfile(
            url=url,
            params=params,
            presets=presets,
            queue=queue,
            nocache=nocache,
            cache=cache,
            verbose=False,
        )
        return self.create(
            name=name, description=description, tags=tags, content=op_spec
        )

    @check_no_op
    @check_offline
    def create_from_hub(
        self,
        component: str,
        name: str = None,
        description: str = None,
        tags: Union[str, Sequence[str]] = None,
        params: Dict = None,
        presets: str = None,
        queue: str = None,
        nocache: bool = None,
        cache: bool = None,
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
            presets: List[str], optional, the name of the
                [presets](/docs/core/introduction/concepts/#preset).
            queue: str, optional, the name of the
                [queue](/docs/core/scheduling-strategies/queue-routing/) to assign the run to.
            nocache: bool, optional, simple flag to disable
                [cache check](/docs/automation/helpers/cache/).
                If passed and the Polyaxonfile has cache section,
                it will be patched with `disabled: true`.
            cache: bool, optional, simple flag to enable
                [cache check](/docs/automation/helpers/cache/).
                If passed and the Polyaxonfile has cache section,
                it will be patched with `disabled: false`.

        Returns:
            V1Run, run instance from the response.
        """
        op_spec = check_polyaxonfile(
            hub=component,
            params=params,
            presets=presets,
            queue=queue,
            nocache=nocache,
            cache=cache,
            verbose=False,
        )
        return self.create(
            name=name, description=description, tags=tags, content=op_spec
        )

    @check_no_op
    @check_offline
    def log_status(self, status: str, reason: str = None, message: str = None):
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
            reason: str, optional, reason for this status change.
            message: str, optional, message to log with this status.
        """
        status_condition = V1StatusCondition(
            type=status, status=True, reason=reason, message=message
        )
        self.client.runs_v1.create_run_status(
            owner=self.owner,
            project=self.project,
            uuid=self.run_uuid,
            body={"condition": status_condition},
            async_req=True,
        )

    @check_no_op
    @check_offline
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

    @check_no_op
    @check_offline
    def wait_for_condition(
        self, statuses: List[str] = None, print_status: bool = False
    ):
        """Waits for the run's last status to meet a condition.

        If statuses is passed the it will wait for the condition:
         * last status is one of the statuses passed.

        Otherwise, it will wait until the user interrupts the function or reaches a final status.

        N.B. if you want to watch statuses and and receive the status/conditions,
        please use `watch_statuses` instead which yields the results.
        """
        for status, conditions in self._wait_for_condition(statuses):
            self._run_data.status = status
            if print_status:
                print("Last received status: {}\n".format(status))

    @check_no_op
    @check_offline
    def watch_statuses(self, statuses: List[str] = None):
        """Watches run statuses.

        If statuses is passed the watch will wait for a condition:
         * last status is one of the statuses passed.

        Otherwise, it will watch until the user interrupts it or reaches a final status.

        N.B. if you just wait for a status condition without expecting a yield,
        please use `wait_for_condition` instead

        Yields:
            Tuple[status, List[conditions]]:
                This function will yield the last status and condition for every check.
        """
        for status, conditions in self._wait_for_condition(statuses):
            self._run_data.status = status
            yield status, conditions

    @check_no_op
    @check_offline
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

    @check_no_op
    @check_offline
    def watch_logs(self, hide_time: bool = False, all_info: bool = False):
        """Watches run logs.

        Args:
            hide_time: bool, optional, default: False, remove time information from log lines.
            all_info: bool, optional, default: False, show all information about log lines.
        """
        return get_run_logs(
            client=self, hide_time=hide_time, all_info=all_info, follow=True
        )

    @check_no_op
    @check_offline
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

    @check_no_op
    @check_offline
    def get_multi_runs_events(
        self,
        kind: V1ArtifactKind,
        runs: List[str],
        names: List[str],
        orient: str = None,
        force: bool = False,
    ):
        """Gets multi-runs events.

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

    @check_no_op
    @check_offline
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

    @check_no_op
    @check_offline
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
        url = "{host}/{url}".format(host=clean_host(self.client.config.host), url=url)
        if force:
            url = "{}?force=true".format(url)

        return PolyaxonStore(client=self).download_file(
            url=url, path=path, path_to=path_to
        )

    @check_no_op
    @check_offline
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
        url = "{host}/{url}".format(host=clean_host(self.client.config.host), url=url)

        return PolyaxonStore(client=self).download_file(
            url=url,
            path=path,
            untar=untar,
            path_to=path_to,
            delete_tar=delete_tar and untar,
            extract_path=extract_path,
        )

    @check_no_op
    @check_offline
    def get_artifacts_tree(self, path: str = ""):
        """Return the artifacts tree based on the path.

        Args:
            path: str, the relative path of the artifact to return.

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

    @check_no_op
    @check_offline
    def stop(self):
        """Stops the current run."""
        self.client.runs_v1.stop_run(
            self.owner,
            self.project,
            self.run_uuid,
        )

    @check_no_op
    @check_offline
    def invalidate(self):
        """Invalidates the current run."""
        self.client.runs_v1.invalidate_run(
            self.owner,
            self.project,
            self.run_uuid,
        )

    @check_no_op
    @check_offline
    def restart(self, override_config=None, copy: bool = False, **kwargs):
        """Restarts the current run

        Args:
            override_config: Dict or str, optional,
                config to use for overriding the original run's config.
            copy: bool, optional, default: False, to restart with copy mechanism.

        Returns:
            V1Run instance.
        """
        body = polyaxon_sdk.V1Run(content=override_config)
        if copy:
            return self.client.runs_v1.copy_run(
                self.owner, self.project, self.run_uuid, body=body, **kwargs
            )
        else:
            return self.client.runs_v1.restart_run(
                self.owner, self.project, self.run_uuid, body=body, **kwargs
            )

    @check_no_op
    @check_offline
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

    @check_no_op
    @check_offline
    def set_description(self, description: str, async_req: bool = True):
        """Sets a new description for the current run.

        Args:
            description: str, the description to set.
            async_req: bool, optional, default: False, execute request asynchronously.
        """
        self._update({"description": description}, async_req=async_req)
        self._run_data.description = description

    @check_no_op
    @check_offline
    def set_name(self, name: str, async_req: bool = True):
        """Sets a new name for the current run.

        Args:
            name: str, the name to set.
            async_req: bool, optional, default: False, execute request asynchronously.
        """
        self._update({"name": name}, async_req=async_req)
        self._run_data.name = name

    @check_no_op
    @check_offline
    def log_inputs(self, reset: bool = False, async_req: bool = True, **inputs):
        """Logs or resets new inputs/params for the current run.

        <blockquote class="light">
        N.B. If you are starting a run from the CLI/UI
        polyaxon will track all inputs from the Polyaxonfile,
        so you generally don't need to set them manually.
        But you can always add or reset these params/inputs once your code starts running.
        </blockquote>

        Args:
            reset: bool, optional, if True, it will reset the whole inputs state.
                Note that Polyaxon will automatically populate the inputs based
                on the Polyaxonfile inputs definition and params passed.
            async_req: bool, optional, default: False, execute request asynchronously.
            inputs: **kwargs, e.g. param1=value1, param2=value2, ...
        """
        patch_dict = {"inputs": inputs}
        if reset is False:
            patch_dict["merge"] = True
            self._run_data.inputs = self._run_data.inputs or {}
            self._run_data.inputs.update(inputs)
        else:
            self._run_data.inputs = inputs
        self._update(patch_dict, async_req=async_req)

    @check_no_op
    @check_offline
    def log_outputs(self, reset: bool = False, async_req: bool = True, **outputs):
        """Logs a new outputs for the current run.


        Args:
            reset: bool, optional, if True, it will reset the whole outputs state.
                Note that Polyaxon will automatically populate some outputs based
                on the Polyaxonfile outputs definition and params passed.
            async_req: bool, optional, default: False, execute request asynchronously.
            outputs: **kwargs, e.g. output1=value1, metric2=value2, ...
        """
        patch_dict = {"outputs": outputs}
        if reset is False:
            patch_dict["merge"] = True
            self._run_data.outputs = self._run_data.outputs or {}
            self._run_data.outputs.update(outputs)
        else:
            self._run_data.outputs = outputs
        self._update(patch_dict, async_req=async_req)

    def log_meta(self, reset: bool = False, async_req: bool = True, **meta):
        """Logs meta_info for the current run.

        > **Note**: Use carefully! The meta information is used by
        Polyaxon internally to perform several information.

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
        patch_dict = {"meta_info": meta}
        if reset is False:
            patch_dict["merge"] = True
            self._run_data.meta_info = self._run_data.meta_info or {}
            self._run_data.meta_info.update(meta)
        else:
            self._run_data.meta_info = meta
        self._update(patch_dict, async_req=async_req)

    @check_no_op
    @check_offline
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
        patch_dict = {"tags": validate_tags(tags)}
        if reset is False:
            patch_dict["merge"] = True
        self._update(patch_dict, async_req=async_req)

    @check_no_op
    @check_offline
    def start(self):
        """Sets the current run to `running` status.

        <blockquote class="info">
        N.B. If you are executing a managed run, you don't need to call this method manually.
        This method is only useful for manual runs outside of Polyaxon.
        </blockquote>
        """
        self.log_status(polyaxon_sdk.V1Statuses.RUNNING, "Operation is running")
        self._run_data.status = polyaxon_sdk.V1Statuses.RUNNING

    @check_no_op
    @check_offline
    def end(self, status: str, message: str = None, traceback: str = None):
        """Sets the current run to `status` status.

        <blockquote class="info">
        N.B. If you are executing a managed run, you don't need to call this method manually.
        This method is only useful for manual runs outside of Polyaxon.
        </blockquote>

        Args:
            status: str, a valid [Statuses](/docs/core/specification/lifecycle/) value.
            message: str, optional, message to log with this status.
            traceback: str, optional, reason for this status change.
        """
        if self.status in LifeCycle.DONE_VALUES:
            return
        self.log_status(status=status, reason=message, message=traceback)
        self._run_data.status = status
        time.sleep(
            0.1
        )  # Just to give the opportunity to the worker to pick the message

    @check_no_op
    @check_offline
    def log_succeeded(self, message="Operation has succeeded"):
        """Sets the current run to `succeeded` status.

        <blockquote class="info">
        N.B. If you are executing a managed run, you don't need to call this method manually.
        This method is only useful for manual runs outside of Polyaxon.
        </blockquote>
        """
        self.end(polyaxon_sdk.V1Statuses.SUCCEEDED, message)

    @check_no_op
    @check_offline
    def log_stopped(self, message="Operation is stopped"):
        """Sets the current run to `stopped` status.

        <blockquote class="info">
        N.B. If you are executing a managed run, you don't need to call this method manually.
        This method is only useful for manual runs outside of Polyaxon.
        </blockquote>
        """
        self.end(polyaxon_sdk.V1Statuses.STOPPED, message)

    @check_no_op
    @check_offline
    def log_failed(self, message: str = None, traceback: str = None):
        """Sets the current run to `failed` status.

        <blockquote class="info">
        N.B. If you are executing a managed run, you don't need to call this method manually.
        This method is only useful for manual runs outside of Polyaxon.
        </blockquote>

        Args:
            message: str, optional, message to log with this status.
            traceback: str, optional, reason for this status change.
        """
        self.end(
            status=polyaxon_sdk.V1Statuses.FAILED, message=message, traceback=traceback
        )

    @check_no_op
    @check_offline
    def log_code_ref(self, code_ref: Dict = None, is_input: bool = True):
        """Logs code reference.

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

    @staticmethod
    def get_rel_asset_path(path: str = None, rel_path: str = None):
        if not path or rel_path:
            return rel_path
        if CONTEXT_MOUNT_ARTIFACTS in path:
            try:
                return os.path.relpath(path, CONTEXT_MOUNT_ARTIFACTS)
            except Exception as e:
                logger.debug("could not calculate relative path %s", e)

        return rel_path or path

    @check_no_op
    @check_offline
    def log_data_ref(
        self,
        name: str,
        hash: str = None,
        path: str = None,
        content=None,
        is_input: bool = True,
    ):
        """Logs data reference.

        Args:
            name: str, name of the data.
            hash: str, optional, default = None, the hash version of the data,
                if not provided it will be calculated based on the data in the content.
            path: str, optional, path of where the data is coming from.
            is_input: bool, if the data reference is an input or outputs.
            content: the data content.
        """
        summary = {}
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

    @check_no_op
    @check_offline
    def log_file_ref(
        self,
        path: str,
        name: str = None,
        hash: str = None,
        content=None,
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
            is_input: bool, if the file reference is an input or outputs.
            rel_path: str, optional relative path to the run artifacts path.
        """
        summary = {"path": path}
        if hash:
            summary["hash"] = hash
        elif content is not None:
            summary["hash"] = hash_value(content)
        name = name or os.path.basename(path)
        rel_path = self.get_rel_asset_path(path=path, rel_path=rel_path)
        if name:
            artifact_run = V1RunArtifact(
                name=name,
                kind=V1ArtifactKind.FILE,
                path=rel_path,
                summary=summary,
                is_input=is_input,
            )
            self.log_artifact_lineage(body=artifact_run)

    @check_no_op
    @check_offline
    def log_dir_ref(
        self,
        path: str,
        name: str = None,
        is_input: bool = False,
        rel_path: str = None,
    ):
        """Logs dir reference.

        Args:
            path: str, dir path, the name is extracted from the path.
            name: str, if the name is passed it will be used instead of the dirname from the path.
            is_input: bool, if the dir reference is an input or outputs.
            rel_path: str, optional relative path to the run artifacts path.
        """
        name = name or os.path.basename(path)
        rel_path = self.get_rel_asset_path(path=path, rel_path=rel_path)
        if name:
            artifact_run = V1RunArtifact(
                name=name,
                kind=V1ArtifactKind.DIR,
                path=rel_path,
                summary={"path": path},
                is_input=is_input,
            )
            self.log_artifact_lineage(body=artifact_run)

    @check_no_op
    @check_offline
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
        rel_path = self.get_rel_asset_path(path=path, rel_path=rel_path)
        artifact_run = V1RunArtifact(
            name=name,
            kind=V1ArtifactKind.TENSORBOARD,
            path=rel_path,
            summary={"path": path},
            is_input=is_input,
        )
        self.log_artifact_lineage(body=artifact_run)
        self.log_meta(has_tensorboard=True)

    @check_no_op
    @check_offline
    def log_artifact_lineage(
        self, body: Union[Dict, List[Dict], V1RunArtifact, List[V1RunArtifact]]
    ):
        """Logs an artifact lineage.

        Args:
            body: dict or List[dict] or V1RunArtifact or List[V1RunArtifact], body of the lineage.
        """
        self.client.runs_v1.create_run_artifacts_lineage(
            self.owner,
            self.project,
            self.run_uuid,
            body=body,
        )

    @check_no_op
    @check_offline
    def get_namespace(self):
        """Fetches the run namespace."""
        return self.client.runs_v1.get_run_namespace(
            self.owner,
            self.project,
            self.run_uuid,
        ).namespace

    @check_no_op
    @check_offline
    def delete(self):
        """Deletes the current run."""
        return self.client.runs_v1.delete_run(self.owner, self.project, self.run_uuid)

    @check_no_op
    @check_offline
    def list(
        self, query: str = None, sort: str = None, limit: int = None, offset: int = None
    ):
        """Lists runs under the current owner - project.

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
        return self.client.runs_v1.list_runs(self.owner, self.project, **params)

    @check_no_op
    @check_offline
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
            get_logs_handler(
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
                    if not last_time:
                        last_time = last_transition_time
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
