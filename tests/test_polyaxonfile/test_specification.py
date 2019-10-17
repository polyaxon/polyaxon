# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

import pytest

from flaky import flaky
from marshmallow import ValidationError
from tests.utils import assert_equal_dict

from polyaxon.exceptions import PolyaxonConfigurationError, PolyaxonfileError
from polyaxon.schemas.ops.environments import EnvironmentConfig
from polyaxon.schemas.ops.io import IOTypes
from polyaxon.schemas.specs import (
    JobSpecification,
    OperationSpecification,
    PipelineSpecification,
    ServiceSpecification,
    get_specification,
)
from polyaxon.schemas.utils import TaskType


@pytest.mark.polyaxonfile_mark
class TestSpecifications(TestCase):
    def test_non_yaml_spec(self):
        config = ",sdf;ldjks"
        with self.assertRaises(PolyaxonConfigurationError):
            JobSpecification.read(config)

        with self.assertRaises(PolyaxonConfigurationError):
            ServiceSpecification.read(config)

        with self.assertRaises(PolyaxonConfigurationError):
            PipelineSpecification.read(config)

    def test_job_specification_raises_for_missing_container_section(self):
        with self.assertRaises(PolyaxonfileError):
            JobSpecification.read(
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
            "version": 0.6,
            "kind": "job",
            "container": {"image": "test/test:latest", "command": "train"},
        }
        spec = JobSpecification.read(content)
        spec = spec.apply_context()
        new_spec = JobSpecification.read(spec.data)
        spec = new_spec.apply_context()
        assert new_spec.data == content

        # Add params
        params = {"params": {"lr": 0.1}}
        with self.assertRaises(PolyaxonfileError):
            spec.patch(values=params)

    def test_apply_context_raises_with_required_inputs(self):
        content = {
            "version": 0.6,
            "kind": "job",
            "inputs": [
                {"name": "lr", "type": IOTypes.FLOAT},
                {"name": "num_steps", "type": IOTypes.INT},
            ],
            "container": {"image": "test/test:latest", "command": "train"},
        }
        spec = JobSpecification.read(content)

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
            "version": 0.6,
            "kind": "job",
            "inputs": [
                {"name": "lr", "type": IOTypes.FLOAT},
                {"name": "num_steps", "type": IOTypes.INT},
            ],
            "container": {"image": "test/test:latest", "command": "train"},
        }
        spec = JobSpecification.read(content)
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
            "version": 0.6,
            "kind": "job",
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
            "container": {"image": "test/test:latest", "command": "train"},
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
            "version": 0.6,
            "kind": "job",
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
            "container": {"image": "test/test:latest", "command": "train"},
        }
        spec = JobSpecification.read(content)
        assert spec.config.inputs[0].value == 0.6
        assert spec.config.inputs[1].value == 16
        spec = spec.apply_context()
        validated_params = spec.validate_params()
        assert {"lr": 0.6, "num_steps": 16} == {
            p.name: p.value for p in validated_params
        }
        assert spec.config.inputs[0].value == 0.6
        assert spec.config.inputs[1].value == 16

        new_spec = JobSpecification.read(spec.data)
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
            "version": 0.6,
            "kind": "op",
            "name": "foo",
            "description": "a description",
            "tags": ["value"],
            "template": {"name": "foo"},
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "_template": {
                "version": 0.6,
                "kind": "job",
                "name": "build-template",
                "tags": ["kaniko"],
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                "container": {"image": "test"},
            },
        }
        spec = OperationSpecification.read(values=config_dict)
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
            "version": 0.6,
            "kind": "op",
            "name": "foo",
            "description": "a description",
            "tags": ["value"],
            "template": {"name": "foo"},
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "_template": {
                "version": 0.6,
                "kind": "job",
                "name": "build-template",
                "tags": ["kaniko"],
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                "container": {"image": "test"},
            },
        }
        spec = OperationSpecification.read(values=config_dict)

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
            "version": 0.6,
            "kind": "op",
            "name": "foo",
            "description": "a description",
            "tags": ["value"],
            "nocache": True,
            "template": {"name": "foo"},
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "_template": {
                "version": 0.6,
                "kind": "job",
                "name": "build-template",
                "tags": ["kaniko"],
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                "container": {"image": "test"},
            },
        }
        spec = OperationSpecification.read(values=config_dict)

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

    # def test_job_replicas_environment_config(self):
    #     config_dict = {
    #         "resources": {'requests': {"cpu": 1}, "limits": {"cpu": 0.5}},
    #         "replicas": {"n_workers": 10, "n_ps": 5},
    #     }
    #     config = EnvironmentConfig.from_dict(config_dict)
    #     results = config.to_dict()
    #     assert_equal_dict(config_dict["replicas"], results["replicas"])
    #     assert_equal_dict(
    #         {"requests": {"cpu": 0.5}, "limits": {"cpu": 1}}, results["resources"]
    #     )
    #
    #     # Add some field should raise
    #     config_dict.pop("resources")
    #     config_dict["foo"] = {"n_workers": 10, "n_ps": 5}
    #
    #     with self.assertRaises(ValidationError):
    #         EnvironmentConfig.from_dict(config_dict)
    #
    #     del config_dict["foo"]
    #
    #     experiment_config = {"environment": config_dict, "framework": "tensorflow"}
    #     config = JobConfig.from_dict(experiment_config)
    #     assert_equal_dict(experiment_config, config.to_dict())
    #
    #     # Removing framework tensorflow should raise
    #     del experiment_config["framework"]
    #     with self.assertRaises(ValidationError):
    #         JobConfig.from_dict(experiment_config)
    #
    #     # Using unknown framework should raise
    #     experiment_config["framework"] = "foo"
    #     with self.assertRaises(ValidationError):
    #         JobConfig.from_dict(experiment_config)
    #
    #     # Using known framework
    #     experiment_config["framework"] = "mxnet"
    #     config = JobConfig.from_dict(experiment_config)
    #     assert_equal_dict(experiment_config, config.to_dict())
    #
    #     # Adding horovod should raise
    #     experiment_config["framework"] = "horovod"
    #     with self.assertRaises(ValidationError):
    #         JobConfig.from_dict(experiment_config)
    #
    #     # Setting correct horovod replicas should pass
    #     experiment_config["environment"]["replicas"] = {"n_workers": 5}
    #     config = ExperimentConfig.from_dict(experiment_config)
    #     assert_equal_dict(experiment_config, config.to_dict())
    #
    #     # Adding pytorch should pass
    #     experiment_config["framework"] = "pytorch"
    #     config = ExperimentConfig.from_dict(experiment_config)
    #     assert_equal_dict(experiment_config, config.to_dict())
    #
    #     # Setting wrong pytorch replicas should raise
    #     experiment_config["environment"]["replicas"] = {"n_workers": 5, "n_ps": 1}
    #
    #     with self.assertRaises(ValidationError):
    #         ExperimentConfig.from_dict(experiment_config)
    #
    # @flaky(max_runs=3)
    # def test_group_environment(self):
    #     content = {
    #         "version": 1,
    #         "kind": "group",
    #         "hptuning": {"matrix": {"lr": {"values": [0.1, 0.2]}}},
    #         "build": {"image": "my_image"},
    #         "run": {"cmd": "train"},
    #     }
    #     spec = GroupSpecification.read(content)
    #     assert GroupSpecification.read(spec.raw_data).raw_data == spec.raw_data
    #     assert spec.environment is None
    #     assert spec.config_map_refs is None
    #     assert spec.secret_refs is None
    #
    #     content["environment"] = {"config_map_refs": ["foo", "boo"]}
    #     spec = GroupSpecification.read(content)
    #     assert spec.environment is not None
    #     assert spec.config_map_refs is not None
    #     assert [r.to_light_dict() for r in spec.config_map_refs] == [
    #         {"name": "foo"},
    #         {"name": "boo"},
    #     ]
    #     assert spec.secret_refs is None
    #
    #     content["environment"] = {"secret_refs": ["foo", {"name": "boo"}]}
    #     spec = GroupSpecification.read(content)
    #     assert spec.environment is not None
    #     assert spec.config_map_refs is None
    #     assert spec.secret_refs is not None
    #     assert [r.to_light_dict() for r in spec.secret_refs] == [
    #         {"name": "foo"},
    #         {"name": "boo"},
    #     ]
    #
    #     content["environment"] = {
    #         "secret_refs": ["foo", "boo"],
    #         "config_map_refs": ["foo", "boo"],
    #     }
    #     spec = GroupSpecification.read(content)
    #     assert spec.environment is not None
    #     assert spec.config_map_refs is not None
    #     assert [r.to_light_dict() for r in spec.config_map_refs] == [
    #         {"name": "foo"},
    #         {"name": "boo"},
    #     ]
    #     assert [r.to_light_dict() for r in spec.secret_refs] == [
    #         {"name": "foo"},
    #         {"name": "boo"},
    #     ]
