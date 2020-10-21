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
import pytest
import uuid

from polyaxon.env_vars.keys import POLYAXON_KEYS_RUN_INSTANCE
from polyaxon.exceptions import PolyaxonContainerException
from polyaxon.sidecar import start_sidecar
from tests.utils import patch_settings


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::RuntimeWarning")
async def test_monitor_raise_if_no_env_is_set():
    patch_settings()
    os.environ[POLYAXON_KEYS_RUN_INSTANCE] = "foo"
    with pytest.raises(PolyaxonContainerException):
        await start_sidecar(
            container_id="foo",
            sleep_interval=3,
            sync_interval=6,
            monitor_outputs=True,
            monitor_logs=False,
        )
    del os.environ[POLYAXON_KEYS_RUN_INSTANCE]


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::RuntimeWarning")
async def test_monitor_raise_if_no_pod_id():
    patch_settings()
    os.environ[POLYAXON_KEYS_RUN_INSTANCE] = "owner.project.runs.{}".format(
        uuid.uuid4().hex
    )
    with pytest.raises(PolyaxonContainerException):
        await start_sidecar(
            container_id="foo",
            sleep_interval=3,
            sync_interval=6,
            monitor_outputs=True,
            monitor_logs=False,
        )
    del os.environ[POLYAXON_KEYS_RUN_INSTANCE]
