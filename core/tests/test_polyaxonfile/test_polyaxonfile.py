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

from polyaxon.exceptions import PolyaxonfileError
from polyaxon.polyaxonfile import PolyaxonFile
from polyaxon.polyaxonfile.specs import (
    CompiledOperationSpecification,
    OperationSpecification,
)
from polyaxon.polyflow import V1CompiledOperation, V1Plugins, V1RunKind
from polyaxon.polyflow.early_stopping import V1MetricEarlyStopping
from polyaxon.polyflow.environment import V1Environment
from polyaxon.polyflow.parallel import (
    V1GridSearch,
    V1Hyperband,
    V1Mapping,
    V1RandomSearch,
)
from polyaxon.polyflow.parallel.matrix import V1HpChoice, V1HpLinSpace
from polyaxon.polyflow.termination import V1Termination


@pytest.mark.polyaxonfile_mark
class TestPolyaxonfiles(BaseTestCase):
    def test_missing_version_raises(self):
        with self.assertRaises(ValidationError):
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
        run_config = CompiledOperationSpecification.read(
            [
                os.path.abspath("tests/fixtures/plain/simple_job.yml"),
                {"kind": "compiled_operation"},
            ]
        )

        run_config = CompiledOperationSpecification.apply_context(run_config)
        assert run_config.version == 1.05
        assert run_config.tags is None
        assert len(run_config.run.volumes) == 1
        assert run_config.run.to_dict()["volumes"][0] == {
            "name": "foo",
            "secret": {"secretName": "mysecret"},
        }
        assert run_config.run.container.image == "python-with-boto3"
        assert run_config.run.container.command == "python download-s3-bucket"
        assert run_config.run.container.resources == {
            "requests": {"nvidia.com/gpu": 1},
            "limits": {"nvidia.com/gpu": 1},
        }
        assert run_config.run.container.volume_mounts == [
            {"name": "foo", "mount_path": "~/.aws/credentials", "readOnly": True}
        ]

    def test_passing_params_to_no_io_overrides_polyaxonfiles_raises(self):
        polyaxonfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/simple_job.yml")
        )
        with self.assertRaises(ValidationError):
            polyaxonfile.get_op_specification(
                params={"flag": True, "loss": "some-loss"}
            )

    def test_passing_params_overrides_polyaxonfiles(self):
        run_config = CompiledOperationSpecification.read(
            [
                os.path.abspath("tests/fixtures/typing/required_inputs.yml"),
                {"kind": "compiled_operation"},
            ]
        )

        with self.assertRaises(ValidationError):
            CompiledOperationSpecification.apply_context(run_config)
        assert run_config.inputs[0].value is None
        assert run_config.inputs[1].value is None
        run_config.apply_params(
            params={"flag": {"value": True}, "loss": {"value": "some-loss"}}
        )
        assert run_config.inputs[0].value == "some-loss"
        assert run_config.inputs[1].value is True
        run_config = CompiledOperationSpecification.apply_context(run_config)
        run_config = CompiledOperationSpecification.apply_run_contexts(run_config)
        assert run_config.version == 1.05
        assert run_config.tags == ["foo", "bar"]
        assert run_config.run.container.image == "my_image"
        assert run_config.run.container.command == ["/bin/sh", "-c"]
        assert (
            run_config.run.container.args
            == "video_prediction_train --loss=some-loss --flag"
        )

    def test_passing_wrong_params_raises(self):
        with self.assertRaises(PolyaxonfileError):
            polyaxonfile = PolyaxonFile(
                os.path.abspath("tests/fixtures/plain/simple_job.yml")
            )
            polyaxonfile.get_op_specification(params="foo")

    def test_job_file_with_init_passes(self):
        run_config = CompiledOperationSpecification.read(
            [
                os.path.abspath("tests/fixtures/plain/job_file_with_init.yml"),
                {"kind": "compiled_operation"},
            ]
        )
        run_config = CompiledOperationSpecification.apply_context(run_config)
        assert run_config.version == 1.05
        assert isinstance(run_config.plugins, V1Plugins)
        assert run_config.plugins.log_level == "INFO"
        assert run_config.plugins.auth is True
        assert run_config.plugins.shm is True
        assert run_config.plugins.docker is True
        assert run_config.plugins.collect_artifacts is True
        assert run_config.plugins.collect_logs is None
        assert isinstance(run_config.run.environment, V1Environment)
        assert run_config.run.environment.labels == {"key": "value"}
        assert isinstance(run_config.run.init, list)
        assert len(run_config.run.connections) == 2
        assert run_config.run.connections == ["data1", "data2"]
        assert len(run_config.run.volumes) == 2
        assert run_config.run.volumes[0].name == "my_ssh_secret"
        assert run_config.run.volumes[0].secret == {"secretName": "mysecret"}
        assert run_config.run.volumes[1].name == "config_map"
        assert run_config.run.volumes[1].config_map == {"configName": "config_map2"}

    def test_job_file_with_termination_passes(self):
        run_config = CompiledOperationSpecification.read(
            [
                os.path.abspath("tests/fixtures/plain/job_file_with_termination.yml"),
                {"kind": "compiled_operation"},
            ]
        )
        run_config = CompiledOperationSpecification.apply_context(run_config)
        assert run_config.version == 1.05
        assert isinstance(run_config.termination, V1Termination)
        assert run_config.termination.max_retries == 5
        assert run_config.termination.timeout == 500
        assert run_config.termination.ttl == 400
        assert run_config.run.environment.restart_policy == "never"

    def test_job_file_with_environment_passes(self):
        run_config = CompiledOperationSpecification.read(
            [
                os.path.abspath("tests/fixtures/plain/job_file_with_environment.yml"),
                {"kind": "compiled_operation"},
            ]
        )
        run_config = CompiledOperationSpecification.apply_context(run_config)
        assert run_config.version == 1.05
        assert isinstance(run_config.run.environment, V1Environment)
        assert run_config.run.environment.node_selector == {"polyaxon.com": "core"}
        assert run_config.run.container.resources == {
            "requests": {"cpu": 1, "memory": 200},
            "limits": {"cpu": 2, "memory": 200},
        }
        assert run_config.run.environment.affinity.node_affinity == {
            "requiredDuringSchedulingIgnoredDuringExecution": {}
        }
        assert run_config.run.environment.tolerations[0].key == "key"
        assert run_config.run.environment.tolerations[0].operator == "Exists"
        assert run_config.run.environment.labels == {
            "label_key1": "val1",
            "label_key2": "val2",
        }
        assert run_config.run.environment.annotations == {
            "annotation_key1": "val1",
            "annotation_key2": "val2",
        }
        assert run_config.run.environment.service_account_name == "new_sa"
        assert run_config.run.environment.image_pull_secrets == ["secret1", "secret2"]
        assert run_config.run.environment.security_context.run_as_user == 1000
        assert run_config.run.environment.security_context.run_as_group == 3000
        assert isinstance(run_config.plugins, V1Plugins)
        assert run_config.plugins.log_level == "DEBUG"

    def test_matrix_file_passes(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/matrix_job_file.yml")
        )
        run_config = OperationSpecification.compile_operation(plx_file.config)
        run_config = CompiledOperationSpecification.apply_context(run_config)
        assert run_config.version == 1.05
        assert isinstance(run_config.parallel, V1Hyperband)
        assert isinstance(run_config.parallel.params["lr"], V1HpLinSpace)
        assert isinstance(run_config.parallel.params["loss"], V1HpChoice)
        assert run_config.parallel.params["lr"].to_dict() == {
            "kind": "linspace",
            "value": {"start": 0.01, "stop": 0.1, "num": 5},
        }
        assert run_config.parallel.params["loss"].to_dict() == {
            "kind": "choice",
            "value": ["MeanSquaredError", "AbsoluteDifference"],
        }
        assert run_config.parallel.params["normal_rate"].to_dict() == {
            "kind": "normal",
            "value": {"loc": 0, "scale": 0.9},
        }
        assert run_config.parallel.params["dropout"].to_dict() == {
            "kind": "qloguniform",
            "value": {"high": 0.8, "low": 0, "q": 0.1},
        }
        assert run_config.parallel.params["activation"].to_dict() == {
            "kind": "pchoice",
            "value": [["relu", 0.1], ["sigmoid", 0.8]],
        }
        assert run_config.parallel.params["model"].to_dict() == {
            "kind": "choice",
            "value": ["CDNA", "DNA", "STP"],
        }
        assert run_config.parallel.concurrency == 2
        assert isinstance(run_config.parallel, V1Hyperband)
        assert run_config.parallel.kind == V1Hyperband.IDENTIFIER
        assert run_config.parallel.early_stopping is None

    def test_matrix_file_passes_int_float_types(self):
        plx_file = PolyaxonFile(
            os.path.abspath(
                "tests/fixtures/plain/matrix_job_file_with_int_float_types.yml"
            )
        )
        # Get compiled_operation data
        run_config = OperationSpecification.compile_operation(plx_file.config)

        run_config = CompiledOperationSpecification.apply_context(run_config)
        assert run_config.version == 1.05
        assert isinstance(run_config.parallel, V1GridSearch)
        assert isinstance(run_config.parallel.params["param1"], V1HpChoice)
        assert isinstance(run_config.parallel.params["param2"], V1HpChoice)
        assert run_config.parallel.params["param1"].to_dict() == {
            "kind": "choice",
            "value": [1, 2],
        }
        assert run_config.parallel.params["param2"].to_dict() == {
            "kind": "choice",
            "value": [3.3, 4.4],
        }
        assert run_config.parallel.concurrency == 2
        assert isinstance(run_config.parallel, V1GridSearch)
        assert run_config.parallel.kind == V1GridSearch.IDENTIFIER
        assert run_config.parallel.early_stopping is None

    def test_matrix_early_stopping_file_passes(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/matrix_job_file_early_stopping.yml")
        )
        # Get compiled_operation data
        run_config = OperationSpecification.compile_operation(plx_file.config)

        run_config = CompiledOperationSpecification.apply_context(run_config)
        assert run_config.version == 1.05
        assert isinstance(run_config.parallel, V1RandomSearch)
        assert isinstance(run_config.parallel.params["lr"], V1HpLinSpace)
        assert isinstance(run_config.parallel.params["loss"], V1HpChoice)
        assert run_config.parallel.params["lr"].to_dict() == {
            "kind": "linspace",
            "value": {"start": 0.01, "stop": 0.1, "num": 5},
        }
        assert run_config.parallel.params["loss"].to_dict() == {
            "kind": "choice",
            "value": ["MeanSquaredError", "AbsoluteDifference"],
        }
        assert run_config.parallel.concurrency == 2
        assert run_config.parallel.num_runs == 300
        assert isinstance(run_config.parallel, V1RandomSearch)
        assert run_config.parallel.kind == V1RandomSearch.IDENTIFIER
        assert len(run_config.parallel.early_stopping) == 1
        assert isinstance(run_config.parallel.early_stopping[0], V1MetricEarlyStopping)

    def test_mapping_early_stopping_file_passes(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/mapping_job_file_early_stopping.yml")
        )
        # Get compiled_operation data
        config_run = OperationSpecification.compile_operation(plx_file.config)

        config_run = CompiledOperationSpecification.apply_context(config_run)
        assert config_run.version == 1.05
        assert isinstance(config_run.parallel, V1Mapping)
        assert config_run.parallel.values == [
            {"lr": 0.001, "loss": "MeanSquaredError"},
            {"lr": 0.1, "loss": "AbsoluteDifference"},
        ]
        assert config_run.parallel.concurrency == 2
        assert isinstance(config_run.parallel, V1Mapping)
        assert config_run.parallel.kind == V1Mapping.IDENTIFIER
        assert len(config_run.parallel.early_stopping) == 1
        assert isinstance(config_run.parallel.early_stopping[0], V1MetricEarlyStopping)

    def test_tf_passes(self):
        run_config = CompiledOperationSpecification.read(
            [
                os.path.abspath("tests/fixtures/plain/distributed_tensorflow_file.yml"),
                {"kind": "compiled_operation"},
            ]
        )

        run_config = CompiledOperationSpecification.apply_context(run_config)
        assert run_config.version == 1.05
        assert run_config.termination is not None
        assert run_config.termination.ttl == 12
        assert run_config.is_tf_job_run
        assert run_config.run.worker.replicas == 5
        assert run_config.run.worker.environment.affinity is not None
        assert run_config.run.worker.environment.restart_policy == "OnFailure"
        assert run_config.run.worker.container.resources == {
            "requests": {"memory": "300Mi"},
            "limits": {"memory": "300Mi"},
        }
        assert run_config.run.ps.replicas == 10
        assert run_config.run.ps.environment.affinity is None
        assert isinstance(run_config.run.ps.environment.tolerations, list)
        assert run_config.run.ps.environment.restart_policy == "OnFailure"
        assert run_config.run.ps.container.resources == {
            "requests": {"cpu": 3, "memory": "256Mi"},
            "limits": {"cpu": 3, "memory": "256Mi"},
        }

    def test_pytorch_passes(self):
        run_config = CompiledOperationSpecification.read(
            [
                os.path.abspath("tests/fixtures/plain/distributed_pytorch_file.yml"),
                {"kind": "compiled_operation"},
            ]
        )
        run_config = CompiledOperationSpecification.apply_context(run_config)
        assert run_config.version == 1.05

        assert run_config.termination is not None
        assert run_config.termination.ttl == 12

        assert run_config.is_pytorch_job_run
        assert run_config.run.master.replicas == 5
        assert run_config.run.master.environment.to_dict() == {
            "restartPolicy": "OnFailure",
            "nodeName": "foo",
            "serviceAccountName": "sa1",
        }
        assert run_config.run.master.container.image == "my_image"
        assert run_config.run.master.container.resources == {
            "requests": {"memory": "300Mi"},
            "limits": {"memory": "300Mi"},
        }
        assert run_config.run.worker.replicas == 10
        assert run_config.run.worker.environment.affinity is None
        assert run_config.run.worker.environment.restart_policy == "OnFailure"
        assert isinstance(run_config.run.worker.environment.tolerations, list)
        assert run_config.run.worker.container.resources == {
            "requests": {"cpu": 3, "memory": "256Mi"},
            "limits": {"cpu": 3, "memory": "256Mi"},
        }

    def test_mpi_passes(self):
        run_config = CompiledOperationSpecification.read(
            [
                os.path.abspath("tests/fixtures/plain/distributed_mpi_file.yml"),
                {"kind": "compiled_operation"},
            ]
        )

        run_config = CompiledOperationSpecification.apply_context(run_config)
        assert run_config.version == 1.05
        assert run_config.is_mpi_job_run
        assert run_config.termination is None
        assert run_config.run.launcher.replicas == 1
        assert run_config.run.launcher.to_dict() == {
            "replicas": 1,
            "container": {
                "name": "polyaxon-main",
                "image": "mpioperator/tensorflow-benchmarks:latest",
                "command": ["mpirun", "python", "run.py"],
            },
        }
        assert run_config.run.launcher.environment is None

        assert run_config.run.worker.replicas == 2
        assert run_config.run.worker.environment.affinity is None
        assert run_config.run.worker.environment.node_selector is not None
        assert isinstance(run_config.run.worker.environment.tolerations, list)
        assert run_config.run.worker.to_dict()["container"] == {
            "name": "polyaxon-main",
            "image": "mpioperator/tensorflow-benchmarks:latest",
            "command": ["mpirun", "python", "run.py"],
            "resources": {"limits": {"nvidia.com/gpu": 1}},
        }

    def test_specification_with_quotes(self):
        run_config = CompiledOperationSpecification.read(
            [
                os.path.abspath("tests/fixtures/plain/polyaxonfile_with_quotes.yaml"),
                {"kind": "compiled_operation"},
            ]
        )

        run_config = CompiledOperationSpecification.apply_context(run_config)
        expected_run = {
            "kind": V1RunKind.JOB,
            "container": {
                "image": "continuumio/miniconda3",
                "command": ["python"],
                "args": ["-c \"print('Tweet tweet')\""],
                "name": "polyaxon-main",
            },
        }
        assert run_config.run.to_dict() == expected_run
        run_config = V1CompiledOperation.read(run_config.to_dict())
        run_config = CompiledOperationSpecification.apply_context(run_config)
        assert run_config.run.to_dict() == expected_run
