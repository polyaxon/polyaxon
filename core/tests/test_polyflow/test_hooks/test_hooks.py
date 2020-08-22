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

from marshmallow import ValidationError
from tests.utils import BaseTestCase, assert_equal_dict

from polyaxon.polyflow import V1Hook


@pytest.mark.hooks_mark
class TestHooksConfigs(BaseTestCase):
    def test_hooks_config(self):
        config_dict = {}

        with self.assertRaises(ValidationError):
            V1Hook.from_dict(config_dict)

        config_dict["connections"] = "test"
        with self.assertRaises(ValidationError):
            V1Hook.from_dict(config_dict)
        config_dict.pop("connections")

        # Add connection
        config_dict["connection"] = "test"
        config = V1Hook.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add a trigger policy
        config_dict["trigger"] = "not-supported"
        with self.assertRaises(ValidationError):
            V1Hook.from_dict(config_dict)

        # Add trigger
        config_dict["trigger"] = "succeeded"
        config = V1Hook.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add component ref
        config_dict["hubRef"] = "comp1"
        config = V1Hook.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add params
        config_dict["params"] = "comp1"
        with self.assertRaises(ValidationError):
            V1Hook.from_dict(config_dict)

        config_dict["params"] = {"param1": {"value": "value1"}}
        config = V1Hook.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add run patch
        config_dict["runPatch"] = {"container": {"args": ["--branch=dev"]}}
        config = V1Hook.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())
