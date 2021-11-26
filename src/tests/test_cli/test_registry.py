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

import pytest

from mock import patch

from polyaxon.cli.registry import registry
from tests.test_cli.utils import BaseCommandTestCase


@pytest.mark.cli_mark
class TestCliRegistry(BaseCommandTestCase):
    @patch("polyaxon_sdk.ModelRegistryV1Api.create_model_registry")
    def test_create_registry(self, create_model):
        self.runner.invoke(registry, ["create"])
        assert create_model.call_count == 0
        self.runner.invoke(registry, ["create", "--name=owner/foo"])
        assert create_model.call_count == 1

    @patch("polyaxon_sdk.ModelRegistryV1Api.list_model_registries")
    def test_list_registries(self, list_models):
        self.runner.invoke(registry, ["ls", "--owner=owner"])
        assert list_models.call_count == 1

    @patch("polyaxon_sdk.ModelRegistryV1Api.get_model_registry")
    def test_get_registry(self, get_model):
        self.runner.invoke(registry, ["get", "-m", "admin/foo"])
        assert get_model.call_count == 1

    @patch("polyaxon_sdk.ModelRegistryV1Api.patch_model_registry")
    def test_update_registry(self, update_model):
        self.runner.invoke(registry, ["update", "-m", "admin/foo", "--description=foo"])
        assert update_model.call_count == 1
