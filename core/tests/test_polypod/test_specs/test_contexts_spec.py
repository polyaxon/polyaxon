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

from polyaxon.polyaxonfile.specs import kinds
from polyaxon.polyflow import V1CompiledOperation, V1Plugins, V1RunKind
from polyaxon.polypod.specs.contexts import PluginsContextsSpec


@pytest.mark.polypod_mark
class TestPluginsContextsSpec(BaseTestCase):
    def test_get_from_spec(self):
        compiled_operation = V1CompiledOperation.read(
            {
                "version": 1.1,
                "kind": kinds.COMPILED_OPERATION,
                "plugins": {
                    "auth": False,
                    "shm": False,
                    "collectLogs": False,
                    "collectArtifacts": False,
                    "syncStatuses": False,
                },
                "run": {"kind": V1RunKind.JOB, "container": {"image": "test"},},
            }
        )
        spec = PluginsContextsSpec.from_config(compiled_operation.plugins)
        assert spec.auth is False
        assert spec.docker is False
        assert spec.shm is False
        assert spec.collect_artifacts is False
        assert spec.collect_logs is False
        assert spec.sync_statuses is False

    def test_get_from_env(self):
        config = V1Plugins(
            auth=True,
            shm=True,
            docker=True,
            collect_artifacts=True,
            collect_logs=True,
            sync_statuses=True,
        )
        spec = PluginsContextsSpec.from_config(config)
        assert spec.auth is True
        assert spec.docker is True
        assert spec.shm is True
        assert spec.collect_artifacts is True
        assert spec.collect_logs is True
        assert spec.sync_statuses is True

    def test_get_from_empty_env(self):
        spec = PluginsContextsSpec.from_config(V1Plugins(), default_auth=True)
        assert spec.auth is True
        assert spec.docker is False
        assert spec.shm is True
        assert spec.collect_artifacts is True
        assert spec.collect_logs is True
        assert spec.sync_statuses is True

        spec = PluginsContextsSpec.from_config(V1Plugins())
        assert spec.auth is False
        assert spec.docker is False
        assert spec.shm is True
        assert spec.collect_artifacts is True
        assert spec.collect_logs is True
        assert spec.sync_statuses is True
