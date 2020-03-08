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
from tests.utils import BaseTestCase

from polyaxon.polyflow.conditions import ConditionSchema, V1IoCond, V1StatusCond


@pytest.mark.polyflow_mark
class TestCondsConfigs(BaseTestCase):
    def test_status_cond(self):
        config_dict = {"foo": "bar", "operation": "foo", "trigger": "done"}
        with self.assertRaises(ValidationError):
            V1StatusCond.from_dict(config_dict)

        config_dict = {"kind": "foo", "operation": "foo", "trigger": "done"}
        with self.assertRaises(ValidationError):
            V1StatusCond.from_dict(config_dict)

        config_dict = {"operation": "foo", "trigger": "done"}
        V1StatusCond.from_dict(config_dict)

        config_dict = {"kind": "status", "operation": "foo", "trigger": "done"}
        V1StatusCond.from_dict(config_dict)

    def test_io_cond(self):
        config_dict = {
            "operation": "foo",
            "param": "done",
            "trigger": ["op1.done", "foo"],
        }
        with self.assertRaises(ValidationError):
            V1IoCond.from_dict(config_dict)

        config_dict = {"kind": "io", "param": "done", "trigger": ["foo"]}
        with self.assertRaises(ValidationError):
            V1IoCond.from_dict(config_dict)

        config_dict = {"kind": "foo", "param": "done", "trigger": "true"}
        with self.assertRaises(ValidationError):
            V1IoCond.from_dict(config_dict)

        config_dict = {"kind": "outputs", "param": "foo", "trigger": "done"}
        with self.assertRaises(ValidationError):
            V1IoCond.from_dict(config_dict)

        config_dict = {"param": "name", "trigger": ["true"]}
        with self.assertRaises(ValidationError):
            V1IoCond.from_dict(config_dict)

        config_dict1 = {"param": "build.outputs.image", "trigger": "value1"}
        V1IoCond.from_dict(config_dict1)

        config_dict2 = {
            "kind": "io",
            "param": "build.outputs.image",
            "trigger": "~value1|value2|value3",
        }
        V1IoCond.from_dict(config_dict2)

    def test_conds(self):
        configs = [
            {"kind": "status", "operation": "foo", "trigger": "done"},
            {"kind": "io", "param": "foo.outputs.param1", "trigger": "~value1|value2"},
        ]

        ConditionSchema().load(configs, many=True)
