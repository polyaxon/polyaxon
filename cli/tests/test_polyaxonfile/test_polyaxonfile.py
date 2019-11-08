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

from polyaxon.exceptions import PolyaxonfileError
from polyaxon.polyaxonfile import PolyaxonFile
from polyaxon.schemas.polyflow.environments import EnvironmentConfig
from polyaxon.schemas.polyflow.init import InitConfig
from polyaxon.schemas.polyflow.termination import TerminationConfig
from polyaxon.schemas.polyflow.workflows import (
    GridSearchConfig,
    HyperbandConfig,
    MappingConfig,
    RandomSearchConfig,
    WorkflowConfig,
)
from polyaxon.schemas.polyflow.workflows.early_stopping_policies import (
    MetricEarlyStoppingConfig,
)
from polyaxon.schemas.polyflow.workflows.matrix import (
    MatrixChoiceConfig,
    MatrixLinSpaceConfig,
)
from polyaxon.specs import ComponentSpecification


@pytest.mark.polyaxonfile_mark
class TestPolyaxonfiles(TestCase):
    def test_missing_version_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath("tests/fixtures/plain/missing_version.yml"))

    def test_non_supported_version_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath("tests/fixtures/plain/non_supported_file.yml"))

    def test_non_existing_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath("tests/fixtures/plain/non_existing_file.yml"))

    def test_missing_kind_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath("tests/fixtures/plain/missing_kind.yml"))

    def test_simple_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath("tests/fixtures/plain/simple_job.yml"))
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.version == 0.6
        assert spec.tags is None
        assert spec.container.image == "python-with-boto3"
        assert spec.container.command == "python download-s3-bucket"
        assert spec.environment is not None
        assert spec.resources.to_dict() == {
            "requests": {"nvidia.com/gpu": 1},
            "limits": {"nvidia.com/gpu": 1},
        }
        assert spec.is_component

    def test_passing_params_to_no_io_overrides_polyaxonfiles_raises(self):
        polyaxonfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/simple_job.yml")
        )
        with self.assertRaises(PolyaxonfileError):
            polyaxonfile.get_op_specification(
                params={"flag": True, "loss": "some-loss"}
            )

    def test_passing_params_overrides_polyaxonfiles(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/typing/required_inputs.yml")
        )
        spec = plxfile.specification
        with self.assertRaises(PolyaxonfileError):
            spec.apply_context()
        assert spec.config.inputs[0].value is None
        assert spec.config.inputs[1].value is None
        spec.apply_params(params={"flag": True, "loss": "some-loss"})
        assert spec.config.inputs[0].value == "some-loss"
        assert spec.config.inputs[1].value is True
        spec = spec.apply_context()
        spec = spec.apply_container_contexts()
        assert spec.version == 0.6
        assert spec.tags == ["foo", "bar"]
        assert spec.container.image == "my_image"
        assert spec.container.command == ["/bin/sh", "-c"]
        assert spec.container.args == "video_prediction_train --loss=some-loss --flag"
        assert spec.environment is None
        assert spec.is_component

    def test_passing_wrong_params_raises(self):
        with self.assertRaises(PolyaxonfileError):
            polyaxonfile = PolyaxonFile(
                os.path.abspath("tests/fixtures/plain/simple_job.yml")
            )
            polyaxonfile.get_op_specification(params="foo")

    def test_job_file_with_init_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/job_file_with_init.yml")
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_component
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.environment.log_level == "INFO"
        assert isinstance(spec.init, InitConfig)
        assert spec.auth_context is True
        assert spec.shm_context is True
        assert spec.docker_context is True
        assert spec.outputs is True
        assert spec.logs is None
        assert len(spec.artifacts) == 2
        assert spec.artifacts[0].to_dict() == {
            "name": "data1",
            "paths": ["path1", "path2"],
        }
        assert spec.artifacts[1].to_dict() == {"name": "data2"}
        assert len(spec.secrets) == 1
        assert spec.secrets[0].to_dict() == {
            "name": "my_ssh_secret",
            "mount_path": "~/.ssh/id_rsa",
        }
        assert len(spec.config_maps) == 2
        assert spec.config_maps[0].to_dict() == {"name": "config_map1"}
        assert spec.config_maps[1].to_dict() == {
            "name": "config_map2",
            "items": ["item1", "item2"],
        }

    def test_job_file_with_termination_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/job_file_with_termination.yml")
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_component
        assert isinstance(spec.termination, TerminationConfig)
        assert spec.max_retries == 5
        assert spec.timeout == 500
        assert spec.restart_policy == "never"
        assert spec.ttl == 400

    def test_job_file_with_environment_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/job_file_with_environment.yml")
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_component
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.node_selector == {"polyaxon.com": "core"}
        assert spec.resources.to_dict() == {
            "requests": {"cpu": 1, "memory": 200},
            "limits": {"cpu": 2, "memory": 200},
        }
        assert spec.affinity == {
            "nodeAffinity": {"requiredDuringSchedulingIgnoredDuringExecution": {}}
        }
        assert spec.tolerations == [{"key": "key", "operator": "Exists"}]
        assert spec.labels == {"label_key1": "val1", "label_key2": "val2"}
        assert spec.annotations == {
            "annotation_key1": "val1",
            "annotation_key2": "val2",
        }
        assert spec.service_account == "new_sa"
        assert spec.image_pull_secrets == ["secret1", "secret2"]
        assert spec.env_vars == {"env_var_key1": "val1", "env_var_key2": "val2"}
        assert spec.security_context == {
            "runAsUser": 1000,
            "runAsGroup": 3000,
            "fsGroup": 5000,
        }
        assert spec.log_level == "DEBUG"

    def test_matrix_file_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/matrix_job_file.yml")
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_component
        assert isinstance(spec.workflow, WorkflowConfig)
        assert isinstance(spec.workflow.strategy.matrix["lr"], MatrixLinSpaceConfig)
        assert isinstance(spec.workflow.strategy.matrix["loss"], MatrixChoiceConfig)
        assert spec.workflow.strategy.matrix["lr"].to_dict() == {
            "kind": "linspace",
            "value": {"start": 0.01, "stop": 0.1, "num": 5},
        }
        assert spec.workflow.strategy.matrix["loss"].to_dict() == {
            "kind": "choice",
            "value": ["MeanSquaredError", "AbsoluteDifference"],
        }
        assert spec.workflow.strategy.matrix["normal_rate"].to_dict() == {
            "kind": "normal",
            "value": {"loc": 0, "scale": 0.9},
        }
        assert spec.workflow.strategy.matrix["dropout"].to_dict() == {
            "kind": "qloguniform",
            "value": {"high": 0.8, "low": 0, "q": 0.1},
        }
        assert spec.workflow.strategy.matrix["activation"].to_dict() == {
            "kind": "pchoice",
            "value": [["relu", 0.1], ["sigmoid", 0.8]],
        }
        assert spec.workflow.strategy.matrix["model"].to_dict() == {
            "kind": "choice",
            "value": ["CDNA", "DNA", "STP"],
        }
        assert spec.workflow.concurrency == 2
        assert spec.concurrency == 2
        assert isinstance(spec.workflow_strategy, HyperbandConfig)
        assert spec.workflow_strategy_kind == HyperbandConfig.IDENTIFIER
        assert spec.workflow.early_stopping is None
        assert spec.early_stopping == []

    def test_matrix_file_passes_int_float_types(self):
        plxfile = PolyaxonFile(
            os.path.abspath(
                "tests/fixtures/plain/matrix_job_file_with_int_float_types.yml"
            )
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_component
        assert isinstance(spec.workflow, WorkflowConfig)
        assert isinstance(spec.workflow.strategy.matrix["param1"], MatrixChoiceConfig)
        assert isinstance(spec.workflow.strategy.matrix["param2"], MatrixChoiceConfig)
        assert spec.workflow.strategy.matrix["param1"].to_dict() == {
            "kind": "choice",
            "value": [1, 2],
        }
        assert spec.workflow.strategy.matrix["param2"].to_dict() == {
            "kind": "choice",
            "value": [3.3, 4.4],
        }
        assert spec.workflow.concurrency == 2
        assert isinstance(spec.workflow_strategy, GridSearchConfig)
        assert spec.workflow_strategy_kind == GridSearchConfig.IDENTIFIER
        assert spec.workflow.early_stopping is None
        assert spec.early_stopping == []

    def test_matrix_early_stopping_file_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/matrix_job_file_early_stopping.yml")
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_component
        assert isinstance(spec.workflow, WorkflowConfig)
        assert isinstance(spec.workflow.strategy.matrix["lr"], MatrixLinSpaceConfig)
        assert isinstance(spec.workflow.strategy.matrix["loss"], MatrixChoiceConfig)
        assert spec.workflow.strategy.matrix["lr"].to_dict() == {
            "kind": "linspace",
            "value": {"start": 0.01, "stop": 0.1, "num": 5},
        }
        assert spec.workflow.strategy.matrix["loss"].to_dict() == {
            "kind": "choice",
            "value": ["MeanSquaredError", "AbsoluteDifference"],
        }
        assert spec.workflow.concurrency == 2
        assert spec.workflow.strategy.n_experiments == 300
        assert isinstance(spec.workflow_strategy, RandomSearchConfig)
        assert spec.workflow_strategy_kind == RandomSearchConfig.IDENTIFIER
        assert spec.early_stopping == spec.workflow.early_stopping
        assert len(spec.early_stopping) == 1
        assert isinstance(spec.early_stopping[0], MetricEarlyStoppingConfig)

    def test_mapping_early_stopping_file_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/mapping_job_file_early_stopping.yml")
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_component
        assert isinstance(spec.workflow, WorkflowConfig)
        assert spec.workflow.strategy.values == [
            {"lr": 0.001, "loss": "MeanSquaredError"},
            {"lr": 0.1, "loss": "AbsoluteDifference"},
        ]
        assert spec.workflow.concurrency == 2
        assert isinstance(spec.workflow_strategy, MappingConfig)
        assert spec.workflow_strategy_kind == MappingConfig.IDENTIFIER
        assert spec.early_stopping == spec.workflow.early_stopping
        assert len(spec.early_stopping) == 1
        assert isinstance(spec.early_stopping[0], MetricEarlyStoppingConfig)

    def test_tf_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/distributed_tensorflow_file.yml")
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.version == 0.6
        assert spec.log_level == "INFO"
        assert spec.is_component
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.environment.node_selector is None
        assert spec.environment.tolerations is None
        assert spec.environment.node_selector is None
        assert isinstance(spec.environment.affinity, dict)
        assert spec.environment.resources.to_dict() == {
            "requests": {"cpu": 1},
            "limits": {"cpu": 2},
        }

        assert spec.config.workflow.has_tf_job_strategy
        assert spec.config.workflow.strategy.worker.replicas == 5
        assert spec.config.workflow.strategy.worker.termination is not None
        assert (
            spec.config.workflow.strategy.worker.termination.restart_policy
            == "OnFailure"
        )
        assert spec.config.workflow.strategy.worker.environment.resources.to_dict() == {
            "requests": {"memory": "300Mi"},
            "limits": {"memory": "300Mi"},
        }
        assert spec.config.workflow.strategy.ps.replicas == 10
        assert spec.config.workflow.strategy.ps.environment.affinity is None
        assert isinstance(
            spec.config.workflow.strategy.ps.environment.tolerations, list
        )
        assert spec.config.workflow.strategy.ps.environment.resources.to_dict() == {
            "requests": {"cpu": 3, "memory": "256Mi"},
            "limits": {"cpu": 3, "memory": "256Mi"},
        }

    def test_pytorch_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/distributed_pytorch_file.yml")
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.version == 0.6
        assert spec.log_level == "INFO"
        assert spec.is_component
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.environment.node_selector is None
        assert spec.environment.tolerations is None
        assert spec.environment.node_selector is None
        assert isinstance(spec.environment.affinity, dict)
        assert spec.environment.resources.to_dict() == {
            "requests": {"cpu": 1},
            "limits": {"cpu": 2},
        }

        assert spec.config.workflow.has_pytorch_job_strategy
        assert spec.config.workflow.strategy.master.replicas == 5
        assert spec.config.workflow.strategy.master.termination is not None
        assert (
            spec.config.workflow.strategy.master.termination.restart_policy
            == "OnFailure"
        )
        assert spec.config.workflow.strategy.master.environment.resources.to_dict() == {
            "requests": {"memory": "300Mi"},
            "limits": {"memory": "300Mi"},
        }
        assert spec.config.workflow.strategy.worker.replicas == 10
        assert spec.config.workflow.strategy.worker.environment.affinity is None
        assert isinstance(
            spec.config.workflow.strategy.worker.environment.tolerations, list
        )
        assert spec.config.workflow.strategy.worker.environment.resources.to_dict() == {
            "requests": {"cpu": 3, "memory": "256Mi"},
            "limits": {"cpu": 3, "memory": "256Mi"},
        }

    def test_mpi_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/distributed_mpi_file.yml")
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.version == 0.6
        assert spec.log_level == "INFO"
        assert spec.is_component

        assert spec.config.workflow.has_mpi_job_strategy
        assert spec.config.workflow.strategy.launcher.replicas == 1
        assert spec.config.workflow.strategy.launcher.container.to_dict() == {
            "image": "mpioperator/tensorflow-benchmarks:latest",
            "command": ["mpirun", "python", "run.py"],
        }
        assert spec.config.workflow.strategy.launcher.termination is None
        assert spec.config.workflow.strategy.launcher.environment is None

        assert spec.config.workflow.strategy.worker.replicas == 2
        assert spec.config.workflow.strategy.worker.environment.affinity is None
        assert (
            spec.config.workflow.strategy.worker.environment.node_selector is not None
        )
        assert isinstance(
            spec.config.workflow.strategy.worker.environment.tolerations, list
        )
        assert spec.config.workflow.strategy.worker.environment.resources.to_dict() == {
            "limits": {"nvidia.com/gpu": 1}
        }

    def test_specification_with_quotes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/polyaxonfile_with_quotes.yaml")
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.container.image == "continuumio/miniconda3"
        assert spec.container.command == ["python"]
        assert spec.container.args == ["-c \"print('Tweet tweet')\""]
        spec = ComponentSpecification(spec.data)
        spec = spec.apply_context()
        assert spec.container.image == "continuumio/miniconda3"
        assert spec.container.command == ["python"]
        assert spec.container.args == ["-c \"print('Tweet tweet')\""]
