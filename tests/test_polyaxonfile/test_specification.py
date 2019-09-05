# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

import pytest

from flaky import flaky
from marshmallow import ValidationError
from tests.utils import assert_equal_dict

from polyaxon_schemas.exceptions import PolyaxonConfigurationError, PolyaxonfileError
from polyaxon_schemas.ops.environments import EnvironmentConfig
from polyaxon_schemas.ops.job import JobConfig
from polyaxon_schemas.specs import (
    JobSpecification,
    PipelineSpecification,
    ServiceSpecification,
)
from polyaxon_schemas.utils import TaskType


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
    def test_patch_experiment(self):
        content = {
            "version": 0.6,
            "kind": "job",
            "container": {"image": "test/test:latest", "command": "train"},
        }
        spec = JobSpecification.read(content)
        spec.apply_context()
        new_spec = JobSpecification.read(spec.raw_data)
        new_spec.apply_context()
        assert new_spec.parsed_data == content
        assert spec.params is None

        # Add params
        params = {"params": {"lr": 0.1}}
        spec = spec.patch(values=params)
        assert spec.params == params["params"]

        # Update params
        params = {"params": {"lr": 0.01, "num_steps": 100}}
        spec = spec.patch(values=params)
        assert spec.params == params["params"]

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
        assert spec.params == params["params"]
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
