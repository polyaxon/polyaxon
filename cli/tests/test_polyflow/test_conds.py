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

from marshmallow import ValidationError

from polyaxon.schemas.polyflow.conditions import (
    ConditionSchema,
    OpInputsConditionConfig,
    OpOutputsConditionConfig,
    OpStatusConditionConfig,
)


@pytest.mark.polyflow_mark
class TestCondsConfigs(TestCase):
    def test_status_cond(self):
        config_dict = {"foo": "bar", "op": "foo", "trigger": "done"}
        with self.assertRaises(ValidationError):
            OpStatusConditionConfig.from_dict(config_dict)

        config_dict = {"kind": "foo", "op": "foo", "trigger": "done"}
        with self.assertRaises(ValidationError):
            OpStatusConditionConfig.from_dict(config_dict)

        config_dict = {"op": "foo", "trigger": "done"}
        OpStatusConditionConfig.from_dict(config_dict)

        config_dict = {"kind": "status", "op": "foo", "trigger": "done"}
        OpStatusConditionConfig.from_dict(config_dict)

    def test_outputs_cond(self):
        config_dict = {"op": "foo", "exp": "done", "params": ["op1.done", "foo"]}
        with self.assertRaises(ValidationError):
            OpOutputsConditionConfig.from_dict(config_dict)

        config_dict = {
            "kind": "foo",
            "op": "foo",
            "exp": "eq",
            "params": [["op1.done", "foo"]],
        }
        with self.assertRaises(ValidationError):
            OpOutputsConditionConfig.from_dict(config_dict)

        config_dict = {"op": "foo", "exp": "eq", "params": ["op1.done", "foo"]}
        with self.assertRaises(ValidationError):
            OpOutputsConditionConfig.from_dict(config_dict)

        config_dict = {"op": "foo", "exp": "eq", "params": [["op1.done", "foo"]]}
        OpOutputsConditionConfig.from_dict(config_dict)

        config_dict = {
            "kind": "outputs",
            "op": "foo",
            "exp": "eq",
            "params": [["op1.done", "foo"]],
        }
        OpOutputsConditionConfig.from_dict(config_dict)

    def test_inputs_cond(self):
        config_dict = {"op": "foo", "exp": "done", "params": ["op1.done", "foo"]}
        with self.assertRaises(ValidationError):
            OpInputsConditionConfig.from_dict(config_dict)

        config_dict = {
            "kind": "foo",
            "op": "foo",
            "exp": "eq",
            "params": [["op1.done", "foo"]],
        }
        with self.assertRaises(ValidationError):
            OpInputsConditionConfig.from_dict(config_dict)

        config_dict = {"op": "foo", "exp": "eq", "params": ["op1.done", "foo"]}
        with self.assertRaises(ValidationError):
            OpInputsConditionConfig.from_dict(config_dict)

        config_dict = {"op": "foo", "exp": "eq", "params": [["op1.done", "foo"]]}
        OpInputsConditionConfig.from_dict(config_dict)

        config_dict = {
            "kind": "outputs",
            "op": "foo",
            "exp": "eq",
            "params": [["op1.done", "foo"]],
        }
        OpInputsConditionConfig.from_dict(config_dict)

    def test_conds(self):
        configs = [
            {"kind": "status", "op": "foo", "trigger": "done"},
            {
                "kind": "outputs",
                "op": "foo",
                "exp": "eq",
                "params": [["op1.done", "foo"]],
            },
        ]

        ConditionSchema().load(configs, many=True)
