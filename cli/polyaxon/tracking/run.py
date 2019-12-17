#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

import atexit
import sys
import time

from datetime import datetime

import polyaxon_sdk

from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon import settings
from polyaxon.client import PolyaxonClient
from polyaxon.client.handlers.conf import setup_logging
from polyaxon.client.statuses import get_run_statuses
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.specs import get_specification
from polyaxon.stores import StoreManager
from polyaxon.tracking.is_managed import ensure_is_managed
from polyaxon.tracking.no_op import check_no_op
from polyaxon.tracking.offline import check_offline
from polyaxon.tracking.paths import get_artifacts_paths, get_log_level, get_outputs_path
from polyaxon.tracking.utils.env import get_run_env
from polyaxon.tracking.utils.project import get_project_info
from polyaxon.tracking.utils.run_info import get_run_info
from polyaxon.utils.code_reference import get_code_reference
from polyaxon.utils.validation import validate_tags


class Run(object):
    @check_no_op
    def __init__(
        self,
        owner=None,
        project=None,
        run_uuid=None,
        client=None,
        track_logs=True,
        track_code=True,
        track_env=False,
        outputs_store=None,
    ):

        owner, project = get_project_info(owner=owner, project=project)

        if project is None:
            if settings.CLIENT_CONFIG.is_managed:
                owner, project, _run_uuid = self.get_run_info()
                run_uuid = run_uuid or _run_uuid
            else:
                raise PolyaxonClientException("Please provide a valid project.")

        self.status = None
        self.client = client
        if not (self.client or settings.CLIENT_CONFIG.is_offline):
            self.client = PolyaxonClient()

        self.track_logs = track_logs
        self.track_code = track_code
        self.track_env = track_env
        self._owner = owner
        self._project = project
        self._run_uuid = run_uuid
        self.outputs_store = outputs_store

        # Setup the outputs store
        if outputs_store is None and settings.CLIENT_CONFIG.is_managed:
            self.set_outputs_store(outputs_path=get_outputs_path(), set_env_vars=True)

        self._run = polyaxon_sdk.V1Run()
        if settings.CLIENT_CONFIG.is_offline:
            return

        if self._run_uuid:
            self.refresh_data()

        # Track run env
        if settings.CLIENT_CONFIG.is_managed and self.track_env:
            self.log_run_env()

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
    def data(self):
        return self._run

    @check_no_op
    def create(
        self,
        name=None,
        tags=None,
        description=None,
        content=None,
        base_outputs_path=None,
    ):
        run = polyaxon_sdk.V1Run()
        if self.track_env:
            run.run_env = get_run_env()
        if name:
            run.name = name
        if tags:
            run.tags = tags
        if description:
            run.description = description
        if content:
            try:
                specification = get_specification(data=[content])
            except Exception as e:
                raise PolyaxonClientException(e)
            run.content = specification.config_dump
        else:
            run.is_managed = False

        if self.client:
            try:
                run = self.client.runs_v1.create_run(
                    owner=self.owner, project=self.project, body=run
                )
            except (ApiException, HTTPError) as e:
                raise PolyaxonClientException(e)
            if not run:
                raise PolyaxonClientException("Could not create a run.")
        if not settings.CLIENT_CONFIG.is_managed and self.track_logs:
            setup_logging(send_logs=self.send_logs)
        self._run = run
        self._run_uuid = run.uuid
        self.status = "created"

        # Setup the outputs store
        if self.outputs_store is None and base_outputs_path:
            outputs_path = "{}/{}/{}/{}".format(
                base_outputs_path, self.owner, self.project, self.run_uuid
            )
            self.set_outputs_store(outputs_path=outputs_path)

        if self.track_code:
            self.log_code_ref()

        if not settings.CLIENT_CONFIG.is_managed:
            self._start()
        else:
            self._register_wait()

        return self

    @check_no_op
    @check_offline
    def refresh_data(self):
        self._run = self.client.runs_v1.get_run(self.owner, self.project, self.run_uuid)
        for status, conditions in get_run_statuses(
            self.owner, self.project, self.run_uuid
        ):
            self.status = status

    @check_no_op
    @check_offline
    def _update(self, patch_dict):
        self.client.runs_v1.patch_run(
            owner=self.owner,
            project=self.project,
            run_uuid=self.run_uuid,
            body=patch_dict,
            async_req=True,
        )

    @property
    def is_service(self):
        if settings.CLIENT_CONFIG.no_op:
            return None

        return settings.CLIENT_CONFIG.is_managed and settings.CLIENT_CONFIG.is_service

    @check_no_op
    @check_offline
    def send_logs(self, log_line):
        self.client.experiment.send_logs(
            owner=self.owner,
            project_name=self.project_name,
            experiment_id=self.experiment_id,
            log_lines=log_line,
            periodic=True,
        )

    @check_no_op
    @check_offline
    def log_status(self, status, reason=None, message=None):
        status_condition = polyaxon_sdk.V1StatusCondition(
            type=status, status=True, reason=reason, message=message
        )
        self.client.runs_v1.create_run_status(
            owner=self.owner,
            project=self.project,
            uuid=self.run_uuid,
            body=status_condition,
            async_req=True,
        )

    @check_no_op
    @check_offline
    def get_statuses(self, watch=False):
        for status, conditions in get_run_statuses(
            self.owner, self.project, self.run_uuid, watch
        ):
            self.status = status
            yield conditions

    @check_no_op
    @check_offline
    def log_code_ref(self):
        self.client.experiment.create_code_reference(
            owner=self.owner,
            project_name=self.project_name,
            experiment_id=self.experiment_id,
            coderef=get_code_reference(),
            async_req=True,
        )

    @check_no_op
    @check_offline
    def log_metrics(self, **metrics):
        self.client.experiment.create_metric(
            owner=self.owner,
            project_name=self.project_name,
            experiment_id=self.experiment_id,
            values=metrics,
            created_at=datetime.utcnow(),
            periodic=True,
        )

    @staticmethod
    @check_no_op
    def get_run_info():
        """
        Returns information about the current run:
            * owner
            * project
            * run_uuid
        """
        ensure_is_managed()

        return get_run_info()

    @check_no_op
    def get_inputs(self):
        """
        Returns all the run inputs/params.
        """
        return self.data.inputs

    @check_no_op
    def get_outputs(self):
        """
        Returns all the run inputs/params.
        """
        return self.data.outputs

    @check_no_op
    def get_default_artifacts_path(self):
        return get_outputs_path()

    @check_no_op
    def get_log_level(self):
        return get_log_level()

    @staticmethod
    def get_artifacts_paths():
        if settings.CLIENT_CONFIG.no_op:
            return None
        return get_artifacts_paths()

    @check_no_op
    @check_offline
    def _register_wait(self):
        atexit.register(self._wait)

    @check_no_op
    @check_offline
    def _start(self):
        atexit.register(self._end)
        self.start()

        def excepthook(exception, value, tb):
            self.log_failed(message="Type: {}, Value: {}".format(exception, value))
            # Resume normal work
            sys.__excepthook__(exception, value, tb)

        sys.excepthook = excepthook

    @check_no_op
    @check_offline
    def _end(self):
        self.log_succeeded()
        self._wait()

    @check_no_op
    @check_offline
    def _wait(self):
        time.sleep(1)

    @check_no_op
    @check_offline
    def start(self):
        self.log_status("running", "Job is running")
        self.status = "running"

    @check_no_op
    @check_offline
    def end(self, status, message=None, traceback=None):
        if self.status in ["succeeded", "failed", "stopped"]:
            return
        self.log_status(status=status, reason=message, message=traceback)
        self.status = status
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
    def set_outputs_store(
        self, outputs_store=None, outputs_path=None, set_env_vars=False
    ):
        if not any([outputs_store, outputs_path]):
            raise PolyaxonClientException(
                "An Store instance or and outputs path is required."
            )
        self.outputs_store = outputs_store or StoreManager(path=outputs_path)
        if self.outputs_store and set_env_vars:
            self.outputs_store.set_env_vars()

    @check_no_op
    def log_artifact(self, filepath):
        self.outputs_store.upload_file(filename=filepath)

    @check_no_op
    def log_artifacts(self, dir_path):
        self.outputs_store.upload_dir(dirname=dir_path)

    @check_no_op
    @check_offline
    def log_run_env(self):
        self._update({"run_env": get_run_env()})

    @check_no_op
    @check_offline
    def log_tags(self, tags, reset=False):
        patch_dict = {"tags": validate_tags(tags)}
        if reset is False:
            patch_dict["merge"] = True
        self._update(patch_dict)

    @check_no_op
    @check_offline
    def log_inputs(self, reset=False, **inputs):
        patch_dict = {"inputs": inputs}
        if reset is False:
            patch_dict["merge"] = True
            self.data.inputs = inputs
        else:
            self.data.inputs.update(inputs)
        self._update(patch_dict)

    @check_no_op
    @check_offline
    def log_outputs(self, reset=False, **outputs):
        patch_dict = {"outputs": outputs}
        if reset is False:
            patch_dict["merge"] = True
            self.data.outputs = outputs
        else:
            self.data.inputs.update(outputs)
        self._update(patch_dict)

    @check_no_op
    @check_offline
    def set_description(self, description):
        self._update({"description": description})
        self.data.description = description

    @check_no_op
    @check_offline
    def set_name(self, name):
        self._update({"name": name})
        self.data.name = name
