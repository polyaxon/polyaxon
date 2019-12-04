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

import os

from unittest import TestCase

import pytest

from flaky import flaky
from marshmallow import ValidationError
from tests.utils import assert_equal_dict

from polyaxon.exceptions import PolyaxonfileError, PolyaxonSchemaError
from polyaxon.schemas.polyflow.environment import EnvironmentConfig
from polyaxon.schemas.polyflow.io import IOTypes
from polyaxon.schemas.utils import TaskType
from polyaxon.specs import ComponentSpecification, OpSpecification, get_specification


@pytest.mark.polyaxonfile_mark
class TestSpecifications(TestCase):
    def test_non_yaml_spec(self):
        config = ",sdf;ldjks"
        with self.assertRaises(PolyaxonSchemaError):
            OpSpecification.read(config)

        with self.assertRaises(PolyaxonSchemaError):
            ComponentSpecification.read(config)

    def test_job_specification_raises_for_missing_container_section(self):
        with self.assertRaises(PolyaxonfileError):
            OpSpecification.read(
                os.path.abspath("tests/fixtures/plain/job_missing_container.yml")
            )

    # def test_cluster_def_without_framework(self):
    #     spec = ExperimentSpecification.read(
    #         os.path.abspath("tests/fixtures/plain/env_without_framework.yml")
    #     )
    #     spec.apply_context()
    #     self.assertEqual(spec.cluster_def, ({TaskType.MASTER: 1}, False))
    #
    def test_patch_experiment_without_io_and_params_raises(self):
        content = {
            "version": 1.0,
            "kind": "component",
            "run": {
                "kind": "container",
                "image": "test/test:latest",
                "command": "train",
            },
        }
        spec = ComponentSpecification.read(content)
        spec = spec.apply_context()
        new_spec = ComponentSpecification.read(spec.data)
        spec = new_spec.apply_context()
        assert new_spec.data == content

        # Add params
        params = {"params": {"lr": 0.1}}
        with self.assertRaises(PolyaxonfileError):
            spec.patch(values=params)

    def test_apply_context_raises_with_required_inputs(self):
        content = {
            "version": 1.0,
            "kind": "component",
            "inputs": [
                {"name": "lr", "type": IOTypes.FLOAT},
                {"name": "num_steps", "type": IOTypes.INT},
            ],
            "run": {
                "kind": "container",
                "image": "test/test:latest",
                "command": "train",
            },
        }
        spec = ComponentSpecification.read(content)

        # Raise because required inputs are not met
        with self.assertRaises(PolyaxonfileError):
            spec.apply_context()

        # Validation for template should pass
        validated_params = spec.validate_params()
        assert {"lr": None, "num_steps": None} == {
            p.name: p.value for p in validated_params
        }
        # Validation for non template should raise
        with self.assertRaises(PolyaxonfileError):
            spec.validate_params(is_template=False)

    def test_apply_context_passes_with_required_inputs_and_params(self):
        content = {
            "version": 1.0,
            "kind": "component",
            "inputs": [
                {"name": "lr", "type": IOTypes.FLOAT},
                {"name": "num_steps", "type": IOTypes.INT},
            ],
            "run": {
                "kind": "container",
                "image": "test/test:latest",
                "command": "train",
            },
        }
        spec = ComponentSpecification.read(content)
        # no params
        with self.assertRaises(PolyaxonfileError):
            spec.apply_context()

        params = {"lr": 0.1, "num_steps": 100}

        assert spec.config.inputs[0].value is None
        assert spec.config.inputs[1].value is None
        validated_params = spec.validate_params(params=params)
        spec.apply_params(params=params)
        assert params == {p.name: p.value for p in validated_params}
        assert spec.config.inputs[0].value == 0.1
        assert spec.config.inputs[1].value == 100

        new_spec = spec.apply_context()
        updated_content = {
            "version": 1.0,
            "kind": "component",
            "inputs": [
                {
                    "name": "lr",
                    "type": IOTypes.FLOAT,
                    "is_optional": True,
                    "value": 0.1,
                },
                {
                    "name": "num_steps",
                    "type": IOTypes.INT,
                    "is_optional": True,
                    "value": 100,
                },
            ],
            "run": {
                "kind": "container",
                "image": "test/test:latest",
                "command": "train",
            },
        }
        assert new_spec.data == updated_content

        env = {
            "environment": {
                "resources": {
                    "requests": {"gpu": 1, "tpu": 1},
                    "limits": {"gpu": 1, "tpu": 1},
                }
            }
        }
        spec = spec.patch(values=env)
        assert spec.data["environment"] == env["environment"]

    def test_patch_experiment_with_optional_inputs(self):
        content = {
            "version": 1.0,
            "kind": "component",
            "inputs": [
                {
                    "name": "lr",
                    "type": IOTypes.FLOAT,
                    "value": 0.6,
                    "is_optional": True,
                },
                {
                    "name": "num_steps",
                    "type": IOTypes.INT,
                    "value": 16,
                    "is_optional": True,
                },
            ],
            "run": {
                "kind": "container",
                "image": "test/test:latest",
                "command": "train",
            },
        }
        spec = ComponentSpecification.read(content)
        assert spec.config.inputs[0].value == 0.6
        assert spec.config.inputs[1].value == 16
        spec = spec.apply_context()
        validated_params = spec.validate_params()
        assert {"lr": 0.6, "num_steps": 16} == {
            p.name: p.value for p in validated_params
        }
        assert spec.config.inputs[0].value == 0.6
        assert spec.config.inputs[1].value == 16

        new_spec = ComponentSpecification.read(spec.data)
        assert new_spec.data == content

        params = {"lr": 0.6, "num_steps": 16}
        new_spec.validate_params(params=params)
        new_spec.apply_context()
        assert spec.config.inputs[0].value == 0.6
        assert spec.config.inputs[1].value == 16

        with self.assertRaises(PolyaxonfileError):  # not valid
            params = {"params": {"lr": 0.1}}
            spec.patch(values=params)

        # Add env
        assert spec.environment is None
        env = {
            "environment": {
                "resources": {
                    "requests": {"gpu": 1, "tpu": 1},
                    "limits": {"gpu": 1, "tpu": 1},
                }
            }
        }
        spec = spec.patch(values=env)
        assert spec.environment.resources.to_dict() == {
            "requests": {"gpu": 1, "tpu": 1},
            "limits": {"gpu": 1, "tpu": 1},
        }

        # Patch with unsupported spec
        matrix = {"hptuning": {"matrix": {"lr": {"values": [0.1, 0.2]}}}}
        with self.assertRaises(PolyaxonfileError):
            spec.patch(values=matrix)

        # Patch with unsupported spec
        wrong_config = {"lr": {"values": [0.1, 0.2]}}
        with self.assertRaises(PolyaxonfileError):
            spec.patch(values=wrong_config)

    def test_op_specification_with_override_info(self):
        config_dict = {
            "version": 1.0,
            "kind": "op",
            "name": "foo",
            "description": "a description",
            "tags": ["value"],
            "component_ref": {"name": "foo"},
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "component": {
                "name": "build-template",
                "tags": ["kaniko"],
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                "run": {"kind": "container", "image": "test"},
            },
        }
        spec = OpSpecification.read(values=config_dict)
        assert spec.name == "foo"
        assert spec.description == "a description"
        assert spec.tags == ["value"]

        run_data = spec.generate_run_data()
        job_spec = get_specification(run_data)
        assert job_spec.config.name == "foo"
        assert job_spec.config.description == "a description"
        assert job_spec.tags == ["value"]
        assert job_spec.init.to_light_dict() == {
            "repos": [{"name": "foo", "branch": "dev"}]
        }
        assert job_spec.environment is None

        env = {
            "environment": {
                "resources": {
                    "requests": {"gpu": 1, "tpu": 1},
                    "limits": {"gpu": 1, "tpu": 1},
                }
            }
        }
        run_data = spec.generate_run_data(env)
        job_spec = get_specification(run_data)
        assert job_spec.environment.to_light_dict() == env["environment"]

    def test_op_specification(self):
        config_dict = {
            "version": 1.0,
            "kind": "op",
            "name": "foo",
            "description": "a description",
            "tags": ["value"],
            "component_ref": {"name": "foo"},
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "component": {
                "name": "build-template",
                "tags": ["kaniko"],
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                "run": {"kind": "container", "image": "test"},
            },
        }
        spec = OpSpecification.read(values=config_dict)

        run_data = spec.generate_run_data()
        job_spec = get_specification(run_data)
        assert job_spec.config.name == "foo"
        assert job_spec.config.description == "a description"
        assert job_spec.tags == ["value"]
        assert job_spec.init.to_light_dict() == {
            "repos": [{"name": "foo", "branch": "dev"}]
        }
        assert job_spec.environment is None

        env = {
            "environment": {
                "resources": {
                    "requests": {"gpu": 1, "tpu": 1},
                    "limits": {"gpu": 1, "tpu": 1},
                }
            }
        }
        run_data = spec.generate_run_data(env)
        job_spec = get_specification(run_data)
        assert job_spec.environment.to_light_dict() == env["environment"]

    def test_op_specification_with_nocache(self):
        config_dict = {
            "version": 1.0,
            "kind": "op",
            "name": "foo",
            "description": "a description",
            "tags": ["value"],
            "nocache": True,
            "component_ref": {"name": "foo"},
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "component": {
                "name": "build-template",
                "tags": ["kaniko"],
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                "run": {"kind": "container", "image": "test"},
            },
        }
        spec = OpSpecification.read(values=config_dict)

        run_data = spec.generate_run_data()
        job_spec = get_specification(run_data)
        assert job_spec.config.name == "foo"
        assert job_spec.config.description == "a description"
        assert job_spec.tags == ["value"]
        assert job_spec.nocache is True
        assert job_spec.init.to_light_dict() == {
            "repos": [{"name": "foo", "branch": "dev"}]
        }
        assert job_spec.environment is None

        env = {
            "environment": {
                "resources": {
                    "requests": {"gpu": 1, "tpu": 1},
                    "limits": {"gpu": 1, "tpu": 1},
                }
            }
        }
        run_data = spec.generate_run_data(env)
        job_spec = get_specification(run_data)
        assert job_spec.environment.to_light_dict() == env["environment"]
