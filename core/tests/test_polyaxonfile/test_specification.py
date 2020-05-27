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

import os

import pytest

from marshmallow import ValidationError
from tests.utils import BaseTestCase

from polyaxon import types
from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.polyaxonfile.specs import (
    CompiledOperationSpecification,
    ComponentSpecification,
    OperationSpecification,
)
from polyaxon.polyflow import V1CompiledOperation, V1Component, V1Operation, V1RunKind
from polyaxon.schemas.types import V1GitType
from polyaxon.schemas.types.image import V1ImageType


@pytest.mark.polyaxonfile_mark
class TestSpecifications(BaseTestCase):
    def test_non_yaml_spec(self):
        config = ",sdf;ldjks"
        with self.assertRaises(PolyaxonSchemaError):
            OperationSpecification.read(config)

        with self.assertRaises(PolyaxonSchemaError):
            ComponentSpecification.read(config)

    def test_job_specification_raises_for_missing_container_section(self):
        with self.assertRaises(ValidationError):
            OperationSpecification.read(
                os.path.abspath("tests/fixtures/plain/job_missing_container.yml")
            )

    def test_patch_experiment_without_io_and_params_raises(self):
        content = {
            "version": 1.1,
            "kind": "component",
            "run": {
                "kind": V1RunKind.JOB,
                "container": {
                    "name": "polyaxon-main",
                    "image": "test/test:latest",
                    "command": "train",
                },
            },
        }
        config = V1Component.read(content)
        assert config.to_dict() == content

        content = {
            "version": 1.1,
            "kind": "compiled_operation",
            "run": {
                "kind": V1RunKind.JOB,
                "container": {
                    "name": "polyaxon-main",
                    "image": "test/test:latest",
                    "command": "train",
                },
            },
        }
        config = V1CompiledOperation.read(content)
        config = CompiledOperationSpecification.apply_context(config)
        assert config.to_dict() == content

        # Add params
        params = {"params": {"lr": 0.1}}
        with self.assertRaises(ValidationError):
            config.patch(values=params)

    def test_apply_context_raises_with_required_inputs(self):
        content = {
            "version": 1.1,
            "kind": "component",
            "inputs": [
                {"name": "lr", "type": types.FLOAT},
                {"name": "num_steps", "type": types.INT},
            ],
            "run": {
                "kind": V1RunKind.JOB,
                "container": {
                    "name": "polyaxon-main",
                    "image": "test/test:latest",
                    "command": "train",
                },
            },
        }
        component_config = V1Component.read(content)
        assert component_config.to_dict() == content

        content = {
            "version": 1.1,
            "kind": "compiled_operation",
            "inputs": [
                {"name": "lr", "type": types.FLOAT},
                {"name": "num_steps", "type": types.INT},
            ],
            "run": {
                "kind": V1RunKind.JOB,
                "container": {
                    "name": "polyaxon-main",
                    "image": "test/test:latest",
                    "command": "train",
                },
            },
        }
        run_config = V1CompiledOperation.read(content)

        # Raise because required inputs are not met
        with self.assertRaises(ValidationError):
            CompiledOperationSpecification.apply_context(run_config)

        # Validation for template should pass
        validated_params = run_config.validate_params()
        assert {"lr": None, "num_steps": None} == {
            p.name: p.param.value for p in validated_params
        }
        # Validation for non template should raise
        with self.assertRaises(ValidationError):
            run_config.validate_params(is_template=False)

    def test_apply_context_passes_with_required_inputs_and_params(self):
        content = {
            "version": 1.1,
            "kind": "component",
            "inputs": [
                {"name": "lr", "type": types.FLOAT},
                {"name": "num_steps", "type": types.INT},
            ],
            "run": {
                "kind": V1RunKind.JOB,
                "container": {
                    "name": "polyaxon-main",
                    "image": "test/test:latest",
                    "command": "train",
                },
            },
        }
        component_config = V1Component.read(content)
        assert component_config.to_dict() == content

        content = {
            "version": 1.1,
            "kind": "compiled_operation",
            "inputs": [
                {"name": "lr", "type": types.FLOAT},
                {"name": "num_steps", "type": types.INT},
            ],
            "run": {
                "kind": V1RunKind.JOB,
                "container": {
                    "name": "polyaxon-main",
                    "image": "test/test:latest",
                    "command": "train",
                },
            },
        }
        run_config = V1CompiledOperation.read(content)
        # no params
        with self.assertRaises(ValidationError):
            CompiledOperationSpecification.apply_context(run_config)

        params = {"lr": {"value": 0.1}, "num_steps": {"value": 100}}

        assert run_config.inputs[0].value is None
        assert run_config.inputs[1].value is None
        validated_params = run_config.validate_params(params=params)
        run_config.apply_params(params=params)
        assert params == {p.name: p.param.to_dict() for p in validated_params}
        assert run_config.inputs[0].value == 0.1
        assert run_config.inputs[1].value == 100

        run_config = CompiledOperationSpecification.apply_context(run_config)
        updated_content = {
            "version": 1.1,
            "kind": "compiled_operation",
            "inputs": [
                {"name": "lr", "type": types.FLOAT, "isOptional": True, "value": 0.1},
                {
                    "name": "num_steps",
                    "type": types.INT,
                    "isOptional": True,
                    "value": 100,
                },
            ],
            "run": {
                "kind": V1RunKind.JOB,
                "container": {
                    "name": "polyaxon-main",
                    "image": "test/test:latest",
                    "command": "train",
                },
            },
        }
        assert run_config.to_dict() == updated_content

        env = {
            "run": {
                "container": {
                    "resources": {
                        "requests": {"gpu": 1, "tpu": 1},
                        "limits": {"gpu": 1, "tpu": 1},
                    }
                }
            }
        }
        run_config = run_config.patch(values=env)
        assert (
            run_config.run.container.resources == env["run"]["container"]["resources"]
        )

    def test_apply_params_extends_connections_and_init(self):
        content = {
            "version": 1.1,
            "kind": "compiled_operation",
            "inputs": [
                {"name": "docker_image", "type": types.IMAGE},
                {"name": "git_repo", "type": types.GIT},
            ],
            "run": {
                "kind": V1RunKind.JOB,
                "connections": ["{{ docker_image.connection }}"],
                "container": {
                    "name": "polyaxon-main",
                    "image": "{{ docker_image.name }}",
                    "command": "train",
                },
            },
        }
        run_config = V1CompiledOperation.read(content)
        # no params
        with self.assertRaises(ValidationError):
            CompiledOperationSpecification.apply_context(run_config)

        params = {
            "docker_image": {
                "value": V1ImageType(
                    name="destination:tag", connection="docker-registry"
                )
            },
            "git_repo": {"value": V1GitType(connection="repo-connection")},
        }

        assert run_config.inputs[0].value is None
        assert run_config.inputs[1].value is None
        validated_params = run_config.validate_params(params=params)
        run_config.apply_params(params=params)
        assert params == {p.name: p.param.to_dict() for p in validated_params}
        assert run_config.inputs[0].value.connection == "docker-registry"
        assert run_config.inputs[1].value.connection == "repo-connection"
        run_config = CompiledOperationSpecification.apply_context(run_config)
        run_config = CompiledOperationSpecification.apply_params(run_config)
        run_config = CompiledOperationSpecification.apply_run_contexts(run_config)
        assert run_config.run.connections == ["docker-registry"]

    def test_patch_experiment_with_optional_inputs(self):
        content = {
            "version": 1.1,
            "kind": "compiled_operation",
            "inputs": [
                {"name": "lr", "type": types.FLOAT, "value": 0.6, "isOptional": True},
                {
                    "name": "num_steps",
                    "type": types.INT,
                    "value": 16,
                    "isOptional": True,
                },
            ],
            "run": {
                "kind": V1RunKind.JOB,
                "container": {
                    "name": "polyaxon-main",
                    "image": "test/test:latest",
                    "command": "train",
                },
            },
        }
        config = V1CompiledOperation.read(content)
        assert config.inputs[0].value == 0.6
        assert config.inputs[1].value == 16
        config = CompiledOperationSpecification.apply_context(config)
        validated_params = config.validate_params()
        assert {"lr": 0.6, "num_steps": 16} == {
            p.name: p.param.value for p in validated_params
        }
        assert config.inputs[0].value == 0.6
        assert config.inputs[1].value == 16

        with self.assertRaises(ValidationError):  # not valid
            params = {"params": {"lr": 0.1}}
            config.patch(values=params)

        # Add env
        assert config.run.container.resources is None
        env = {
            "run": {
                "container": {
                    "resources": {
                        "requests": {"gpu": 1, "tpu": 1},
                        "limits": {"gpu": 1, "tpu": 1},
                    }
                }
            }
        }
        config = config.patch(values=env)
        assert config.run.container.resources == {
            "requests": {"gpu": 1, "tpu": 1},
            "limits": {"gpu": 1, "tpu": 1},
        }

        # Patch with unsupported spec
        matrix = {"hptuning": {"params": {"lr": {"values": [0.1, 0.2]}}}}
        with self.assertRaises(ValidationError):
            config.patch(values=matrix)

        # Patch with unsupported spec
        wrong_config = {"lr": {"values": [0.1, 0.2]}}
        with self.assertRaises(ValidationError):
            config.patch(values=wrong_config)

    def test_op_specification_with_override_info(self):
        config_dict = {
            "version": 1.1,
            "kind": "operation",
            "name": "foo",
            "description": "a description",
            "tags": ["value"],
            "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
            "trigger": "all_succeeded",
            "component": {
                "name": "build-template",
                "tags": ["kaniko"],
                "run": {
                    "kind": V1RunKind.JOB,
                    "init": [
                        {
                            "connection": "foo",
                            "container": {
                                "name": "polyaxon-init",
                                "args": "--branch=dev",
                            },
                        }
                    ],
                    "container": {"name": "polyaxon-main", "image": "test"},
                },
            },
        }
        op_config = V1Operation.read(values=config_dict)
        assert op_config.name == "foo"
        assert op_config.description == "a description"
        assert op_config.tags == ["value"]

        run_config = OperationSpecification.compile_operation(op_config)
        assert run_config.name == "foo"
        assert run_config.description == "a description"
        assert run_config.tags == ["value"]
        assert [i.to_light_dict() for i in run_config.run.init] == [
            {
                "connection": "foo",
                "container": {"name": "polyaxon-init", "args": "--branch=dev"},
            }
        ]

        env = {
            "run": {
                "container": {
                    "resources": {
                        "requests": {"gpu": 1, "tpu": 1},
                        "limits": {"gpu": 1, "tpu": 1},
                    }
                }
            }
        }
        run_config = OperationSpecification.compile_operation(op_config, env)
        assert (
            run_config.run.container.resources == env["run"]["container"]["resources"]
        )

    def test_op_specification(self):
        config_dict = {
            "version": 1.1,
            "kind": "operation",
            "name": "foo",
            "description": "a description",
            "tags": ["value"],
            "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
            "trigger": "all_succeeded",
            "component": {
                "name": "build-template",
                "tags": ["kaniko"],
                "run": {
                    "kind": V1RunKind.JOB,
                    "container": {"image": "test"},
                    "init": [
                        {
                            "container": {
                                "name": "polyaxon-init",
                                "image": "foo",
                                "args": "dev",
                            }
                        }
                    ],
                    "sidecars": [{"name": "foo", "image": "foo", "args": "dev"}],
                },
            },
        }
        op_config = V1Operation.read(values=config_dict)

        run_config = OperationSpecification.compile_operation(op_config)
        assert run_config.name == "foo"
        assert run_config.description == "a description"
        assert run_config.tags == ["value"]
        assert [
            {
                "container": {
                    "name": i.container.name,
                    "image": i.container.image,
                    "args": i.container.args,
                }
            }
            for i in run_config.run.init
        ] == [{"container": {"name": "polyaxon-init", "image": "foo", "args": "dev"}}]

        env = {
            "run": {
                "container": {
                    "resources": {
                        "requests": {"gpu": 1, "tpu": 1},
                        "limits": {"gpu": 1, "tpu": 1},
                    }
                }
            }
        }
        run_config = OperationSpecification.compile_operation(op_config, env)
        assert (
            run_config.run.container.resources == env["run"]["container"]["resources"]
        )

    def test_op_specification_with_nocache(self):
        config_dict = {
            "version": 1.1,
            "kind": "operation",
            "name": "foo",
            "description": "a description",
            "tags": ["value"],
            "cache": {"disable": True, "ttl": 12},
            "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
            "trigger": "all_succeeded",
            "component": {
                "name": "build-template",
                "tags": ["kaniko"],
                "run": {
                    "kind": V1RunKind.JOB,
                    "container": {"name": "polyaxon-main", "image": "test"},
                    "init": [{"connection": "some-connection"}],
                },
            },
        }
        op_config = V1Operation.read(values=config_dict)

        run_config = OperationSpecification.compile_operation(op_config)
        assert run_config.name == "foo"
        assert run_config.description == "a description"
        assert run_config.tags == ["value"]
        assert run_config.cache.to_dict() == {"disable": True, "ttl": 12}
        assert [i.to_light_dict() for i in run_config.run.init] == [
            {"connection": "some-connection"}
        ]

        env = {
            "run": {
                "container": {
                    "resources": {
                        "requests": {"gpu": 1, "tpu": 1},
                        "limits": {"gpu": 1, "tpu": 1},
                    }
                }
            }
        }
        run_config = OperationSpecification.compile_operation(op_config, env)
        assert (
            run_config.run.container.resources == env["run"]["container"]["resources"]
        )
