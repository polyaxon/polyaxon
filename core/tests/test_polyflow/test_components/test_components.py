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

from polyaxon import types
from polyaxon.polyflow import V1Component, V1RunKind, ops_params
from polyaxon.utils.tz_utils import local_datetime, now
from tests.utils import BaseTestCase


@pytest.mark.components_mark
class TestComponentsConfigs(BaseTestCase):
    def test_passing_params_declarations_raises(self):
        config_dict = {
            "params": {"foo": {"value": "bar"}},
            "declarations": {"foo": "bar"},
        }

        with self.assertRaises(ValidationError):
            V1Component.from_dict(config_dict)

    def test_passing_wrong_params(self):
        config_dict = {"params": {"foo": "bar"}}

        with self.assertRaises(ValidationError):
            V1Component.from_dict(config_dict)

    def test_passing_params_raises(self):
        config_dict = {"params": {"foo": "bar"}}

        with self.assertRaises(ValidationError):
            V1Component.from_dict(config_dict)

    def test_param_validation_with_inputs(self):
        config_dict = {
            "inputs": [
                {"name": "param1", "type": types.STR},
                {"name": "param2", "type": types.INT},
                {"name": "param3", "type": types.FLOAT},
                {"name": "param4", "type": types.BOOL},
                {"name": "param5", "type": types.DICT},
                {"name": "param6", "type": types.LIST},
                {"name": "param7", "type": types.GCS},
                {"name": "param8", "type": types.S3},
                {"name": "param9", "type": types.WASB},
                {"name": "param10", "type": types.PATH},
            ],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        component = V1Component.from_dict(config_dict)

        params = {
            "param1": {"value": "text"},
            "param2": {"value": 12},
            "param3": {"value": 13.3},
            "param4": {"value": False},
            "param5": {"value": {"foo": "bar"}},
            "param6": {"value": [1, 3, 45, 5]},
            "param7": {"value": "gs://bucket/path/to/blob/"},
            "param8": {"value": "s3://test/this/is/bad/key.txt"},
            "param9": {"value": "wasbs://container@user.blob.core.windows.net/"},
            "param10": {"value": "/foo/bar"},
        }
        validated_params = ops_params.validate_params(
            params=params, inputs=component.inputs, outputs=None, is_template=False
        )
        assert params == {p.name: {"value": p.param.value} for p in validated_params}

        # Passing missing params
        params.pop("param1")
        params.pop("param2")
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params=params, inputs=component.inputs, outputs=None, is_template=False
            )

    def test_param_validation_with_outputs(self):
        config_dict = {
            "outputs": [
                {"name": "param1", "type": types.STR},
                {"name": "param2", "type": types.INT},
                {"name": "param3", "type": types.FLOAT},
                {"name": "param4", "type": types.BOOL},
                {"name": "param5", "type": types.DICT},
                {"name": "param6", "type": types.LIST},
                {"name": "param7", "type": types.GCS},
                {"name": "param8", "type": types.S3},
                {"name": "param9", "type": types.WASB},
                {"name": "param10", "type": types.PATH},
                {"name": "param11", "type": types.METRIC},
                {"name": "param12", "type": types.METADATA},
                {"name": "param13", "type": types.METADATA},
                {"name": "param14", "type": types.METADATA},
            ],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        component = V1Component.from_dict(config_dict)
        params = {
            "param1": {"value": "text"},
            "param2": {"value": 12},
            "param3": {"value": 13.3},
            "param4": {"value": False},
            "param5": {"value": {"foo": "bar"}},
            "param6": {"value": [1, 3, 45, 5]},
            "param7": {"value": "gs://bucket/path/to/blob/"},
            "param8": {"value": "s3://test/this/is/bad/key.txt"},
            "param9": {"value": "wasbs://container@user.blob.core.windows.net/"},
            "param10": {"value": "/foo/bar"},
            "param11": {"value": 124.4},
            "param12": {"value": {"foo": 124.4}},
            "param13": {"value": {"foo": "bar"}},
            "param14": {"value": {"foo": ["foo", 124.4]}},
        }
        validated_params = ops_params.validate_params(
            params=params, inputs=None, outputs=component.outputs, is_template=False
        )
        assert params == {p.name: {"value": p.param.value} for p in validated_params}

        # Passing missing params
        params.pop("param1")
        params.pop("param2")
        validated_params = ops_params.validate_params(
            params=params, inputs=None, outputs=component.outputs, is_template=False
        )
        params["param1"] = {"value": None}
        params["param2"] = {"value": None}
        assert params == {p.name: {"value": p.param.value} for p in validated_params}

    def test_required_input_no_param_only_validated_on_run(self):
        # Inputs
        config_dict = {
            "inputs": [
                {"name": "param1", "type": types.STR},
                {"name": "param10", "type": types.PATH},
            ],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1Component.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": {"value": "text"}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        # Outputs
        config_dict = {
            "outputs": [
                {"name": "param1", "type": types.STR},
                {"name": "param10", "type": types.PATH},
            ],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1Component.from_dict(config_dict)

        ops_params.validate_params(
            params={"param1": {"value": "text"}},
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )

        # IO
        config_dict = {
            "inputs": [{"name": "param1", "type": types.STR}],
            "outputs": [{"name": "param10", "type": types.PATH}],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1Component.from_dict(config_dict)
        ops_params.validate_params(
            params={"param1": {"value": "text"}},
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )

    def test_incomplete_params(self):
        config_dict = {
            "inputs": [
                {"name": "param1", "type": types.INT},
                {"name": "param2", "type": types.INT},
            ],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1Component.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": {"value": 1}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        config_dict = {
            "outputs": [
                {"name": "param1", "type": types.INT, "value": 12, "isOptional": True},
                {"name": "param2", "type": types.INT},
            ],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1Component.from_dict(config_dict)
        ops_params.validate_params(
            params={"param1": {"value": 1}},
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )

    def test_extra_params(self):
        # inputs
        config_dict = {
            "inputs": [{"name": "param1", "type": types.INT}],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1Component.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": {"value": 1}, "param2": {"value": 2}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        # outputs
        config_dict = {
            "outputs": [{"name": "param1", "type": types.INT}],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1Component.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": {"value": 1}, "param2": {"value": 2}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

    def test_param_validation_with_mismatched_inputs(self):
        config_dict = {
            "inputs": [{"name": "param1", "type": types.INT}],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1Component.from_dict(config_dict)
        # Passing correct param
        ops_params.validate_params(
            params={"param1": {"value": 1}},
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )
        # Passing wrong type
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": {"value": "text"}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": {"value": 12.1}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": {"value": {"foo": "bar"}}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": {"value": "gs://bucket/path/to/blob/"}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        config_dict = {
            "inputs": [{"name": "param2", "type": types.STR}],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1Component.from_dict(config_dict)
        # Passing correct param
        ops_params.validate_params(
            params={"param2": {"value": "text"}},
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )
        # Passing wrong type
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param2": {"value": 1}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param2": {"value": False}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param2": {"foo": "bar"}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param2": {"value": ["gs://bucket/path/to/blob/"]}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        config_dict = {
            "inputs": [{"name": "param7", "type": types.WASB}],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1Component.from_dict(config_dict)
        # Passing correct param
        ops_params.validate_params(
            params={
                "param7": {"value": "wasbs://container@user.blob.core.windows.net/"}
            },
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )
        # Passing wrong param
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param7": {"value": "gs://bucket/path/to/blob/"}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param7": {"value": "s3://test/this/is/bad/key.txt"}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param7": {"value": 1}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

    def test_param_validation_with_mismatched_outputs(self):
        config_dict = {
            "outputs": [{"name": "param1", "type": types.INT}],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1Component.from_dict(config_dict)
        # Passing correct param
        ops_params.validate_params(
            params={"param1": {"value": 1}},
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )
        # Passing wrong type
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": {"value": "text"}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": {"value": 12.1}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": {"value": {"foo": "bar"}}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": {"value": "gs://bucket/path/to/blob/"}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        config_dict = {
            "outputs": [{"name": "param2", "type": types.STR}],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1Component.from_dict(config_dict)
        # Passing correct param
        ops_params.validate_params(
            params={"param2": {"value": "text"}},
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )
        # Passing wrong type
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param2": {"value": 1}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param2": {"value": False}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param2": {"value": {"foo": "bar"}}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param2": {"value": ["gs://bucket/path/to/blob/"]}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        config_dict = {
            "outputs": [{"name": "param7", "type": types.WASB}],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1Component.from_dict(config_dict)
        # Passing correct param
        ops_params.validate_params(
            params={
                "param7": {"value": "wasbs://container@user.blob.core.windows.net/"}
            },
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )
        # Passing wrong param
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param7": {"value": "gs://bucket/path/to/blob/"}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param7": {"value": "s3://test/this/is/bad/key.txt"}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param7": {"value": 1}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

    def test_experiment_and_job_refs_params(self):
        config_dict = {
            "inputs": [
                {"name": "param1", "type": types.INT},
                {"name": "param2", "type": types.FLOAT},
                {"name": "param9", "type": types.WASB},
                {"name": "param11", "type": types.METRIC},
            ],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        op = V1Component.from_dict(config_dict)
        params = {
            "param1": {
                "ref": "runs.64332180bfce46eba80a65caf73c5396",
                "value": "outputs.foo",
            },
            "param2": {
                "ref": "runs.0de53b5bf8b04a219d12a39c6b92bcce",
                "value": "outputs.foo",
            },
            "param9": {"value": "wasbs://container@user.blob.core.windows.net/"},
            "param11": {
                "ref": "runs.fcc462d764104eb698d3cca509f34154",
                "value": "outputs.accuracy",
            },
        }
        validated_params = ops_params.validate_params(
            params=params, inputs=op.inputs, outputs=None, is_template=False
        )
        assert {p.name: p.param.to_dict() for p in validated_params} == {
            "param1": {
                "ref": "runs.64332180bfce46eba80a65caf73c5396",
                "value": "outputs.foo",
            },
            "param2": {
                "ref": "runs.0de53b5bf8b04a219d12a39c6b92bcce",
                "value": "outputs.foo",
            },
            "param9": {"value": "wasbs://container@user.blob.core.windows.net/"},
            "param11": {
                "ref": "runs.fcc462d764104eb698d3cca509f34154",
                "value": "outputs.accuracy",
            },
        }

    def test_job_refs_params(self):
        config_dict = {
            "inputs": [
                {"name": "param1", "type": types.INT},
                {"name": "param9", "type": types.FLOAT},
            ],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        params = {
            "param1": {"ref": "job.A", "value": "outputs.foo"},
            "param9": {"value": 13.1},
        }
        config = V1Component.from_dict(config_dict)
        # Validation outside the context of a pipeline
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params=params, inputs=config.inputs, outputs=None, is_template=False
            )

    def test_component_base_attrs(self):
        config_dict = {
            "concurrency": "foo",
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        with self.assertRaises(ValidationError):
            V1Component.from_dict(config_dict)

        config_dict = {
            "concurrency": 2,
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        with self.assertRaises(ValidationError):
            V1Component.from_dict(config_dict)

        config_dict = {
            "kind": "component",
            "matrix": {
                "concurrency": 2,
                "kind": "mapping",
                "values": [{"a": 1}, {"a": 1}],
            },
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        with self.assertRaises(ValidationError):
            V1Component.from_dict(config_dict)

        config_dict = {
            "kind": "component",
            "matrix": {
                "concurrency": 2,
                "kind": "mapping",
                "values": [{"a": 1}, {"a": 1}],
            },
            "schedule": {
                "kind": "datetime",
                "startAt": local_datetime(now()).isoformat(),
            },
            "termination": {"timeout": 1000},
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        with self.assertRaises(ValidationError):
            V1Component.from_dict(config_dict)

        config_dict = {
            "kind": "component",
            "termination": {"timeout": 1000},
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1Component.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_component_actions_and_hooks(self):
        config_dict = {
            "kind": "component",
            "actions": [
                {"hubRef": "ref1"},
                {"hubRef": "ref2", "label": "customLabel", "many": True},
            ],
            "hooks": [
                {"trigger": "succeeded", "connection": "connection1"},
                {"connection": "connection1", "hubRef": "ref2"},
            ],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1Component.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_component_template(self):
        config_dict = {
            "kind": "component",
            "actions": [
                {"hubRef": "ref1"},
                {"hubRef": "ref2", "label": "customLabel", "many": True},
            ],
            "hooks": [
                {"trigger": "succeeded", "connection": "connection1"},
                {"connection": "connection1", "hubRef": "ref2"},
            ],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
            "template": {
                "description": "This is a template, check the fields",
                "fields": ["actions[1].hubRef", "hooks[0].trigger"],
            },
        }
        config = V1Component.from_dict(config_dict)
        assert config.to_dict() == config_dict
