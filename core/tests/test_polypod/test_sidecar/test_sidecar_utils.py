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

import pytest

from tests.utils import BaseTestCase

from polyaxon.containers.containers import get_sidecar_resources
from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_ARTIFACTS_STORE_NAME,
    POLYAXON_KEYS_CONTAINER_ID,
)
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common.env_vars import get_env_var
from polyaxon.polypod.sidecar.container import get_sidecar_args
from polyaxon.polypod.sidecar.env_vars import get_sidecar_env_vars


@pytest.mark.polypod_mark
class TestSidecarUtils(BaseTestCase):
    def test_get_sidecar_env_vars(self):
        sidecar_env_vars = get_sidecar_env_vars(
            env_vars=None, job_container_name="foo", artifacts_store_name="name"
        )

        assert sidecar_env_vars == [
            get_env_var(name=POLYAXON_KEYS_CONTAINER_ID, value="foo"),
            get_env_var(name=POLYAXON_KEYS_ARTIFACTS_STORE_NAME, value="name"),
        ]

        # Initial env vars
        env_vars = [
            get_env_var(name="key1", value="value1"),
            get_env_var(name="key2", value="value2"),
        ]
        sidecar_env_vars = get_sidecar_env_vars(
            env_vars=env_vars, job_container_name="foo", artifacts_store_name="name"
        )

        assert sidecar_env_vars == env_vars + [
            get_env_var(name=POLYAXON_KEYS_CONTAINER_ID, value="foo"),
            get_env_var(name=POLYAXON_KEYS_ARTIFACTS_STORE_NAME, value="name"),
        ]

        # Outputs Path
        sidecar_env_vars = get_sidecar_env_vars(
            env_vars=None, job_container_name="foo", artifacts_store_name="name"
        )

        assert sidecar_env_vars == [
            get_env_var(name=POLYAXON_KEYS_CONTAINER_ID, value="foo"),
            get_env_var(name=POLYAXON_KEYS_ARTIFACTS_STORE_NAME, value="name"),
        ]

    def test_get_sidecar_resources(self):
        assert get_sidecar_resources() == k8s_schemas.V1ResourceRequirements(
            limits={"cpu": "1", "memory": "100Mi"},
            requests={"cpu": "0.1", "memory": "60Mi"},
        )

    def test_get_sidecar_args(self):
        assert get_sidecar_args(
            container_id="job.2", sleep_interval=23, sync_interval=2
        ) == (
            "polyaxon sidecar "
            "--container_id=job.2 "
            "--sleep_interval=23 "
            "--sync_interval=2"
        )
