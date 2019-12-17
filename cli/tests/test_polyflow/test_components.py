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

from hestia.tz_utils import local_now
from marshmallow import ValidationError

from polyaxon.schemas.polyflow import params as ops_params
from polyaxon.schemas.polyflow.component import ComponentConfig
from polyaxon.types import types


@pytest.mark.components_mark
class TestOperationsConfigs(TestCase):
    def test_passing_params_declarations_raises(self):
        config_dict = {"params": {"foo": "bar"}, "declarations": {"foo": "bar"}}

        with self.assertRaises(ValidationError):
            ComponentConfig.from_dict(config_dict)

    def test_passing_declarations_sets_params(self):
        config_dict = {"declarations": {"foo": "bar"}}

        with self.assertRaises(ValidationError):
            ComponentConfig.from_dict(config_dict)

    def test_passing_params_raises(self):
        config_dict = {"params": {"foo": "bar"}}

        with self.assertRaises(ValidationError):
            ComponentConfig.from_dict(config_dict)

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
            "run": {"kind": "container", "image": "test"},
        }
        op = ComponentConfig.from_dict(config_dict)

        params = {
            "param1": "text",
            "param2": 12,
            "param3": 13.3,
            "param4": False,
            "param5": {"foo": "bar"},
            "param6": [1, 3, 45, 5],
            "param7": "gs://bucket/path/to/blob/",
            "param8": "s3://test/this/is/bad/key.txt",
            "param9": "wasbs://container@user.blob.core.windows.net/",
            "param10": "/foo/bar",
        }
        validated_params = ops_params.validate_params(
            params=params, inputs=op.inputs, outputs=None, is_template=False
        )
        assert params == {p.name: p.value for p in validated_params}

        # Passing missing params
        params.pop("param1")
        params.pop("param2")
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params=params, inputs=op.inputs, outputs=None, is_template=False
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
            "run": {"kind": "container", "image": "test"},
        }
        op = ComponentConfig.from_dict(config_dict)
        params = {
            "param1": "text",
            "param2": 12,
            "param3": 13.3,
            "param4": False,
            "param5": {"foo": "bar"},
            "param6": [1, 3, 45, 5],
            "param7": "gs://bucket/path/to/blob/",
            "param8": "s3://test/this/is/bad/key.txt",
            "param9": "wasbs://container@user.blob.core.windows.net/",
            "param10": "/foo/bar",
            "param11": 124.4,
            "param12": {"foo": 124.4},
            "param13": {"foo": "bar"},
            "param14": {"foo": ["foo", 124.4]},
        }
        validated_params = ops_params.validate_params(
            params=params, inputs=None, outputs=op.outputs, is_template=False
        )
        assert params == {p.name: p.value for p in validated_params}

        # Passing missing params
        params.pop("param1")
        params.pop("param2")
        validated_params = ops_params.validate_params(
            params=params, inputs=None, outputs=op.outputs, is_template=False
        )
        params["param1"] = None
        params["param2"] = None
        assert params == {p.name: p.value for p in validated_params}

    def test_required_input_no_param_only_validated_on_run(self):
        # Inputs
        config_dict = {
            "inputs": [
                {"name": "param1", "type": types.STR},
                {"name": "param10", "type": types.PATH},
            ],
            "run": {"kind": "container", "image": "test"},
        }
        config = ComponentConfig.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": "text"},
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
            "run": {"kind": "container", "image": "test"},
        }
        config = ComponentConfig.from_dict(config_dict)

        ops_params.validate_params(
            params={"param1": "text"},
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )

        # IO
        config_dict = {
            "inputs": [{"name": "param1", "type": types.STR}],
            "outputs": [{"name": "param10", "type": types.PATH}],
            "run": {"kind": "container", "image": "test"},
        }
        config = ComponentConfig.from_dict(config_dict)
        ops_params.validate_params(
            params={"param1": "text"},
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
            "run": {"kind": "container", "image": "test"},
        }
        config = ComponentConfig.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": 1},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        config_dict = {
            "outputs": [
                {"name": "param1", "type": types.INT, "value": 12, "is_optional": True},
                {"name": "param2", "type": types.INT},
            ],
            "run": {"kind": "container", "image": "test"},
        }
        config = ComponentConfig.from_dict(config_dict)
        ops_params.validate_params(
            params={"param1": 1},
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )

    def test_extra_params(self):
        # inputs
        config_dict = {
            "inputs": [{"name": "param1", "type": types.INT}],
            "run": {"kind": "container", "image": "test"},
        }
        config = ComponentConfig.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": 1, "param2": 2},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        # outputs
        config_dict = {
            "outputs": [{"name": "param1", "type": types.INT}],
            "run": {"kind": "container", "image": "test"},
        }
        config = ComponentConfig.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": 1, "param2": 2},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

    def test_param_validation_with_mismatched_inputs(self):
        config_dict = {
            "inputs": [{"name": "param1", "type": types.INT}],
            "run": {"kind": "container", "image": "test"},
        }
        config = ComponentConfig.from_dict(config_dict)
        # Passing correct param
        ops_params.validate_params(
            params={"param1": 1},
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )
        # Passing wrong type
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": "text"},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": 12.1},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": {"foo": "bar"}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": "gs://bucket/path/to/blob/"},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        config_dict = {
            "inputs": [{"name": "param2", "type": types.STR}],
            "run": {"kind": "container", "image": "test"},
        }
        config = ComponentConfig.from_dict(config_dict)
        # Passing correct param
        ops_params.validate_params(
            params={"param2": "text"},
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )
        # Passing wrong type
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param2": 1},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param2": False},
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
                params={"param2": ["gs://bucket/path/to/blob/"]},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        config_dict = {
            "inputs": [{"name": "param7", "type": types.WASB}],
            "run": {"kind": "container", "image": "test"},
        }
        config = ComponentConfig.from_dict(config_dict)
        # Passing correct param
        ops_params.validate_params(
            params={"param7": "wasbs://container@user.blob.core.windows.net/"},
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )
        # Passing wrong param
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param7": "gs://bucket/path/to/blob/"},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param7": "s3://test/this/is/bad/key.txt"},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param7": 1},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

    def test_param_validation_with_mismatched_outputs(self):
        config_dict = {
            "outputs": [{"name": "param1", "type": types.INT}],
            "run": {"kind": "container", "image": "test"},
        }
        config = ComponentConfig.from_dict(config_dict)
        # Passing correct param
        ops_params.validate_params(
            params={"param1": 1},
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )
        # Passing wrong type
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": "text"},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": 12.1},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": {"foo": "bar"}},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param1": "gs://bucket/path/to/blob/"},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        config_dict = {
            "outputs": [{"name": "param2", "type": types.STR}],
            "run": {"kind": "container", "image": "test"},
        }
        config = ComponentConfig.from_dict(config_dict)
        # Passing correct param
        ops_params.validate_params(
            params={"param2": "text"},
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )
        # Passing wrong type
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param2": 1},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param2": False},
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
                params={"param2": ["gs://bucket/path/to/blob/"]},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        config_dict = {
            "outputs": [{"name": "param7", "type": types.WASB}],
            "run": {"kind": "container", "image": "test"},
        }
        config = ComponentConfig.from_dict(config_dict)
        # Passing correct param
        ops_params.validate_params(
            params={"param7": "wasbs://container@user.blob.core.windows.net/"},
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
        )
        # Passing wrong param
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param7": "gs://bucket/path/to/blob/"},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param7": "s3://test/this/is/bad/key.txt"},
                inputs=config.inputs,
                outputs=config.outputs,
                is_template=False,
            )

        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params={"param7": 1},
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
            "run": {"kind": "container", "image": "test"},
        }
        op = ComponentConfig.from_dict(config_dict)
        params = {
            "param1": "{{ runs.64332180bfce46eba80a65caf73c5396.outputs.foo }}",
            "param2": "{{ runs.0de53b5bf8b04a219d12a39c6b92bcce.outputs.foo }}",
            "param9": "wasbs://container@user.blob.core.windows.net/",
            "param11": "{{ runs.fcc462d764104eb698d3cca509f34154.outputs.accuracy }}",
        }
        validated_params = ops_params.validate_params(
            params=params, inputs=op.inputs, outputs=None, is_template=False
        )
        assert {p.name: p.value for p in validated_params} == {
            "param1": "runs.64332180bfce46eba80a65caf73c5396.outputs.foo",
            "param2": "runs.0de53b5bf8b04a219d12a39c6b92bcce.outputs.foo",
            "param9": "wasbs://container@user.blob.core.windows.net/",
            "param11": "runs.fcc462d764104eb698d3cca509f34154.outputs.accuracy",
        }

    def test_job_refs_params(self):
        config_dict = {
            "inputs": [
                {"name": "param1", "type": types.INT},
                {"name": "param9", "type": types.FLOAT},
            ],
            "run": {"kind": "container", "image": "test"},
        }
        params = {"param1": "{{ job.A.outputs.foo }}", "param9": 13.1}
        config = ComponentConfig.from_dict(config_dict)
        # Validation outside the context of a pipeline
        with self.assertRaises(ValidationError):
            ops_params.validate_params(
                params=params, inputs=config.inputs, outputs=None, is_template=False
            )

    def test_executable(self):
        config_dict = {"start_at": "foo", "run": {"kind": "container", "image": "test"}}
        with self.assertRaises(ValidationError):
            ComponentConfig.from_dict(config_dict)

        config_dict = {
            "schedule": {"start_at": "foo"},
            "run": {"kind": "container", "image": "test"},
        }
        with self.assertRaises(ValidationError):
            ComponentConfig.from_dict(config_dict)

        config_dict = {"timeout": 2}
        with self.assertRaises(ValidationError):
            ComponentConfig.from_dict(config_dict)

        config_dict = {
            "termination": {"timeout": 2},
            "schedule": {"kind": "exact_time", "start_at": local_now().isoformat()},
            "run": {"kind": "container", "image": "test"},
        }
        ComponentConfig.from_dict(config_dict)

    def test_pipelines_base_attrs(self):
        config_dict = {
            "concurrency": "foo",
            "run": {"kind": "container", "image": "test"},
        }
        with self.assertRaises(ValidationError):
            ComponentConfig.from_dict(config_dict)

        config_dict = {"concurrency": 2, "run": {"kind": "container", "image": "test"}}
        with self.assertRaises(ValidationError):
            ComponentConfig.from_dict(config_dict)

        config_dict = {
            "parallel": {
                "concurrency": 2,
                "kind": "mapping",
                "values": [{"a": 1}, {"a": 1}],
            },
            "run": {"kind": "container", "image": "test"},
        }
        config = ComponentConfig.from_dict(config_dict)
        assert config.to_dict()["run"] == config_dict["run"]
        assert config.to_dict()["parallel"] == config_dict["parallel"]

        config_dict = {
            "parallel": {
                "concurrency": 2,
                "kind": "mapping",
                "values": [{"a": 1}, {"a": 1}],
            },
            "schedule": {"kind": "exact_time", "start_at": local_now().isoformat()},
            "termination": {"timeout": 1000},
            "run": {"kind": "container", "image": "test"},
        }
        config = ComponentConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        config_to_light["schedule"].pop("start_at")
        config_dict["schedule"].pop("start_at")
        assert config_to_light == config_dict
