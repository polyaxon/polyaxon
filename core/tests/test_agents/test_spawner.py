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

import mock
import pytest

from polyaxon.agents.spawners.spawner import Spawner
from polyaxon.exceptions import PolyaxonAgentError
from polyaxon.polyflow import V1RunKind
from tests.utils import BaseTestCase


@pytest.mark.agent_mark
class TestSpawner(BaseTestCase):
    def setUp(self):

        self.spawner = Spawner()
        super().setUp()

    def test_start_apply_stop_get(self):
        k8s_manager = mock.MagicMock()
        k8s_manager.create_custom_object.return_value = ("", "")
        self.spawner._k8s_manager = k8s_manager

        self.spawner.create(run_uuid="", run_kind=V1RunKind.JOB, resource={})
        assert k8s_manager.create_custom_object.call_count == 1

        self.spawner.apply(run_uuid="", run_kind=V1RunKind.JOB, resource={})
        assert k8s_manager.update_custom_object.call_count == 1

        self.spawner.stop(run_uuid="", run_kind=V1RunKind.JOB)
        assert k8s_manager.delete_custom_object.call_count == 1

        self.spawner.get(run_uuid="", run_kind=V1RunKind.JOB)
        assert k8s_manager.get_custom_object.call_count == 1

    def test_start_apply_stop_get_raises_for_non_recognized_kinds(self):

        with self.assertRaises(PolyaxonAgentError):
            self.spawner.create(run_uuid="", run_kind="foo", resource={})

        with self.assertRaises(PolyaxonAgentError):
            self.spawner.apply(run_uuid="", run_kind="foo", resource={})

        with self.assertRaises(PolyaxonAgentError):
            self.spawner.stop(run_uuid="", run_kind="foo")

        with self.assertRaises(PolyaxonAgentError):
            self.spawner.get(run_uuid="", run_kind="foo")
