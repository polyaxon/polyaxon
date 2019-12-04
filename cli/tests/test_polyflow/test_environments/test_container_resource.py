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

from unittest import TestCase

import pytest

from tests.utils import assert_equal_dict

from polyaxon.schemas.polyflow.environment.container_resources import (
    ResourceRequirementsConfig,
)


@pytest.mark.environment_mark
class TestContainerResourceConfigs(TestCase):
    def test_container_resource_config(self):
        config_dict = {"limits": {"cpu": 0.1}}
        config = ResourceRequirementsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"requests": {"cpu": 0.1}}
        config = ResourceRequirementsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"requests": {"cpu": 0.1}, "limits": {"cpu": 0.1}}
        config = ResourceRequirementsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {
            "requests": {"cpu": 0.1, "memory": "10mi"},
            "limits": {"cpu": 0.1, "memory": 1024},
        }
        config = ResourceRequirementsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {
            "requests": {"cpu": 0.1, "memory": "10Mi", "amd.com/gpu": 2},
            "limits": {"cpu": 0.1, "memory": 1024, "amd.com/gpu": 2},
        }
        config = ResourceRequirementsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
