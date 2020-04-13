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
import sys
import time

from typing import Dict, Iterator, List, Tuple, Union

import click
import polyaxon_sdk

from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon import settings
from polyaxon.cli.errors import handle_cli_error
from polyaxon.client import PolyaxonClient
from polyaxon.client.decorators import check_no_op, check_offline
from polyaxon.env_vars.getters import (
    get_project_full_name,
    get_project_or_local,
    get_run_info,
    get_run_or_local,
)
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.lifecycle import LifeCycle, V1StatusCondition
from polyaxon.polyboard.artifacts import V1ArtifactKind, V1RunArtifact
from polyaxon.polyboard.logging.handler import get_logs_handler
from polyaxon.stores.polyaxon_store import PolyaxonStore
from polyaxon.utils.code_reference import get_code_reference
from polyaxon.utils.formatting import Printer
from polyaxon.utils.query_params import get_logs_params, get_query_params
from polyaxon.utils.validation import validate_tags


class RunClient:
    @check_no_op
    def __init__(
        self, owner=None, project=None, run_uuid=None, client=None,
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
    def status(self):
        return self._run_data.status

    @property
    def namespace(self):
        if self._namespace:
            return self._namespace
        self._namespace = self.get_namespace()
        return self._namespace

    @property
    def owner(self):
        return self._owner

    @property
    def project(self):
        return self._project

    @property
    def run_uuid(self):
        return self._run_uuid

    @property
    def run_data(self):
        return self._run_data

    @check_no_op
    def get_inputs(self):
        """
        Returns all the run inputs/params.
        """
        return self._run_data.inputs

    @check_no_op
    def get_outputs(self):
        """
        Returns all the run inputs/params.
        """
        return self._run_data.outputs

    @check_no_op
    @check_offline
    def refresh_data(self):
        self._run_data = self.client.runs_v1.get_run(
            self.owner, self.project, self.run_uuid
        )

    @check_no_op
    @check_offline
    def update(self, data: Union[Dict, polyaxon_sdk.V1Run]):
        return self._update(data=data, async_req=False)

    @check_no_op
    @check_offline
    def _update(self, data: Union[Dict, polyaxon_sdk.V1Run], async_req: bool = True):
        self.client.runs_v1.patch_run(
            owner=self.owner,
            project=self.project,
            run_uuid=self.run_uuid,
            body=data,
            async_req=async_req,
        )

    @check_no_op
    @check_offline
    def log_status(self, status, reason=None, message=None):
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
    def get_statuses(self, last_status: str = None):

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

    @check_no_op
    @check_offline
    def watch_statuses(self):
        def watch_run_statuses() -> Tuple[str, Iterator]:
            last_status = None
            while not LifeCycle.is_done(last_status):
                last_status, _conditions = self.get_statuses(last_status)
                yield last_status, _conditions
                time.sleep(settings.CLIENT_CONFIG.watch_interval)

        for status, conditions in watch_run_statuses():
            self._run_data.status = status
            yield status, conditions

    @check_no_op
    @check_offline
    def get_logs(self, last_file=None, last_time=None):
        params = get_logs_params(last_file=last_file, last_time=last_time)
        return self.client.runs_v1.get_run_logs(
            self.namespace, self.owner, self.project, self.run_uuid, **params
        )

    @check_no_op
    @check_offline
    def watch_logs(self, hide_time: bool = False, all_info: bool = False):
        return get_run_logs(
            client=self, hide_time=hide_time, all_info=all_info, follow=True
        )

    @check_no_op
    @check_offline
    def get_events(self, kind: V1ArtifactKind, names: List[str], orient: str = None):
        return self.client.runs_v1.get_run_events(
            self.namespace,
            self.owner,
            self.project,
            self.run_uuid,
            kind=kind,
            names=names,
            orient=orient,
        )

    @check_no_op
    @check_offline
    def get_multi_runs_events(
        self,
        kind: V1ArtifactKind,
        runs: List[str],
        names: List[str],
        orient: str = None,
    ):
        return self.client.runs_v1.get_multi_run_events(
            self.namespace,
            self.owner,
            self.project,
            kind=kind,
            names=names,
            runs=runs,
            orient=orient,
        )

    @check_no_op
    @check_offline
    def get_artifact(self, path: str, stream: bool = True):
        return self.client.runs_v1.get_run_artifact(
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            uuid=self.run_uuid,
            path=path,
            stream=stream,
            _preload_content=True,
        )

    @check_no_op
    @check_offline
    def download_artifact(self, path: str):
        url = "{host}/streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/artifact".format(
            host=self.client.config.host,
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            uuid=self.run_uuid,
        )

        return PolyaxonStore(client=self).download_file(url=url, path=path)

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
        url = "{host}/streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/artifacts".format(
            host=self.client.config.host,
            namespace=self.namespace,
            owner=self.owner,
            project=self.project,
            uuid=self.run_uuid,
        )

        return PolyaxonStore(client=self).download_file(
            url=url,
            path=path,
            untar=untar,
            delete_tar=delete_tar,
            extract_path=extract_path,
        )

    @check_no_op
    @check_offline
    def get_artifacts_tree(self, path: str = ""):
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
        self.client.runs_v1.stop_run(
            self.owner, self.project, self.run_uuid,
        )

    @check_no_op
    @check_offline
    def invalidate(self):
        self.client.runs_v1.invalidate_run(
            self.owner, self.project, self.run_uuid,
        )

    @check_no_op
    @check_offline
    def restart(self, override_config=None, copy: bool = False, **kwargs):
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
        body = polyaxon_sdk.V1Run(content=override_config)
        return self.client.runs_v1.resume_run(
            self.owner, self.project, self.run_uuid, body=body, **kwargs
        )

    @check_no_op
    @check_offline
    def set_description(self, description, async_req=True):
        self._update({"description": description}, async_req=async_req)
        self._run_data.description = description

    @check_no_op
    @check_offline
    def set_name(self, name, async_req=True):
        self._update({"name": name}, async_req=async_req)
        self._run_data.name = name

    @check_no_op
    @check_offline
    def log_inputs(self, reset=False, async_req=True, **inputs):
        patch_dict = {"inputs": inputs}
        if reset is False:
            patch_dict["merge"] = True
            self._run_data.inputs = inputs
        else:
            self._run_data.inputs.update(inputs)
        self._update(patch_dict, async_req=async_req)

    @check_no_op
    @check_offline
    def log_outputs(self, reset=False, async_req=True, **outputs):
        patch_dict = {"outputs": outputs}
        if reset is False:
            patch_dict["merge"] = True
            self._run_data.outputs = outputs
        else:
            self._run_data.inputs.update(outputs)
        self._update(patch_dict, async_req=async_req)

    @check_no_op
    @check_offline
    def log_tags(self, tags, reset=False, async_req=True):
        patch_dict = {"tags": validate_tags(tags)}
        if reset is False:
            patch_dict["merge"] = True
        self._update(patch_dict, async_req=async_req)

    @check_no_op
    @check_offline
    def start(self):
        self.log_status(polyaxon_sdk.V1Statuses.RUNNING, "Job is running")
        self._run_data.status = polyaxon_sdk.V1Statuses.RUNNING

    @check_no_op
    @check_offline
    def end(self, status, message=None, traceback=None):
        if self.status in LifeCycle.DONE_VALUES:
            return
        self.log_status(status=status, reason=message, message=traceback)
        self._run_data.status = status
        time.sleep(
            0.1
        )  # Just to give the opportunity to the worker to pick the message

    @check_no_op
    @check_offline
    def log_succeeded(self):
        self.end("succeeded", "Job has succeeded")

    @check_no_op
    @check_offline
    def log_stopped(self):
        self.end("stopped", "Job is stopped")

    @check_no_op
    @check_offline
    def log_failed(self, message=None, traceback=None):
        self.end(status="failed", message=message, traceback=traceback)

    @check_no_op
    @check_offline
    def log_code_ref(self):
        code_ref = get_code_reference()
        if code_ref:
            artifact_run = V1RunArtifact(
                name=code_ref.get("commit"),
                kind=V1ArtifactKind.CODEREF,
                summary=code_ref,
                is_input=True,
            )
            self.log_artifact_lineage(body=artifact_run)

    @check_no_op
    @check_offline
    def log_artifact_lineage(self, body: Union[V1RunArtifact, List[V1RunArtifact]]):
        self.client.runs_v1.create_run_artifacts_lineage(
            self.owner, self.project, self.run_uuid, body=body,
        )

    @check_no_op
    @check_offline
    def get_namespace(self):
        return self.client.runs_v1.get_run_namespace(
            self.owner, self.project, self.run_uuid,
        ).namespace

    @check_no_op
    @check_offline
    def delete(self):
        return self.client.runs_v1.delete_run(self.owner, self.project, self.run_uuid)

    @check_no_op
    @check_offline
    def list(
        self, query: str = None, sort: str = None, limit: int = None, offset: int = None
    ):
        params = get_query_params(limit=limit, offset=offset, query=query, sort=sort)
        return self.client.runs_v1.list_runs(self.owner, self.project, **params)

    @check_no_op
    @check_offline
    def list_children(
        self, query: str = None, sort: str = None, limit: int = None, offset: int = None
    ):
        params = get_query_params(limit=limit, offset=offset, query=query, sort=sort)
        query = params.get("query")
        query = query + "&" if query else "?"
        query += "pipeline={}".format(self.run_uuid)
        params["query"] = query

        return self.client.runs_v1.list_runs(self.owner, self.project, **params)


def get_run_logs(
    client: RunClient,
    hide_time: bool = False,
    all_info: bool = False,
    follow: bool = False,
):
    def get_logs(last_file=None, last_time=None):
        try:
            response = client.get_logs(last_file=last_file, last_time=last_time)
            get_logs_handler(show_timestamp=not hide_time, all_info=all_info)(response)
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
        last_time = None
        last_file = None
        _status = None
        last_status, _ = client.get_statuses()
        while not LifeCycle.is_done(last_status) and not LifeCycle.is_running(
            last_status
        ):
            time.sleep(1)
            last_status, _ = client.get_statuses()
            if _status != last_status:
                _status = handle_status(last_status)

        while not is_done:
            response = get_logs(last_time=last_time, last_file=last_file)

            if response:
                last_time = response.last_time
                last_file = response.last_file
            else:
                last_time = None
                last_file = None

            # Follow logic
            if not any([last_file, last_time]):
                if follow:
                    last_status, _ = client.get_statuses()
                    if _status != last_status:
                        _status = handle_status(last_status)
                    is_done = LifeCycle.is_done(last_status)
                else:
                    is_done = True
            if last_time and not follow:
                is_done = True

            if not is_done:
                if last_file:
                    time.sleep(1)
                else:
                    time.sleep(settings.CLIENT_CONFIG.watch_interval)

    handle_logs()
