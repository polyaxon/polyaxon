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
import uuid

from tests.test_k8s.fixtures import (
    status_run_job_event,
    status_run_job_event_with_conditions,
)
from tests.utils import BaseTestCase

from polyaxon.env_vars.keys import POLYAXON_KEYS_RUN_INSTANCE
from polyaxon.exceptions import PolyaxonContainerException
from polyaxon.k8s.monitor import is_container_terminated
from polyaxon.sidecar import start_sidecar


class TestSidecar(BaseTestCase):
    def test_is_container_terminated_no_status(self):
        status = {"container_statuses": []}
        assert is_container_terminated(status, container_id="test") is None

        status = {"container_statuses": {}}
        assert is_container_terminated(status, container_id="test") is None

    def test_is_container_terminated(self):
        assert (
            is_container_terminated(
                status_run_job_event["object"]["status"], container_id="test"
            )
            is None
        )

        # using wrong container id
        assert (
            is_container_terminated(
                status_run_job_event_with_conditions["object"]["status"],
                container_id="test",
            )
            is None
        )

        # using correct container id
        assert (
            is_container_terminated(
                status_run_job_event_with_conditions["object"]["status"],
                container_id="polyaxon-main-job",
            )["exit_code"]
            == 1
        )

    def test_monitor_raise_if_no_env_is_set(self):
        os.environ[POLYAXON_KEYS_RUN_INSTANCE] = "foo"
        with self.assertRaises(PolyaxonContainerException):
            start_sidecar(
                container_id="foo",
                sleep_interval=3,
                sync_interval=6,
                monitor_outputs=True,
                monitor_logs=False,
            )
        del os.environ[POLYAXON_KEYS_RUN_INSTANCE]

    def test_monitor_raise_if_no_pod_id(self):
        os.environ[POLYAXON_KEYS_RUN_INSTANCE] = "owner.project.runs.{}".format(
            uuid.uuid4().hex
        )
        with self.assertRaises(PolyaxonContainerException):
            start_sidecar(
                container_id="foo",
                sleep_interval=3,
                sync_interval=6,
                monitor_outputs=True,
                monitor_logs=False,
            )
        del os.environ[POLYAXON_KEYS_RUN_INSTANCE]
