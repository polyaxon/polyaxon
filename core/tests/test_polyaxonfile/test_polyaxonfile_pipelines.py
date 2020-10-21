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

from mock import patch

from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.k8s.k8s_schemas import V1Container
from polyaxon.polyaxonfile import check_polyaxonfile
from polyaxon.polyaxonfile.specs import (
    CompiledOperationSpecification,
    OperationSpecification,
)
from polyaxon.polyflow import V1IO, V1CompiledOperation, V1Component, V1Job, V1RunKind
from polyaxon.polyflow.early_stopping import (
    V1FailureEarlyStopping,
    V1MetricEarlyStopping,
)
from polyaxon.polyflow.matrix import V1GridSearch, V1Hyperband, V1RandomSearch
from polyaxon.polyflow.matrix.params import V1HpChoice, V1HpLinSpace
from polyaxon.polyflow.run import V1Dag
from tests.utils import BaseTestCase


@pytest.mark.polyaxonfile_mark
class TestPolyaxonfileWithPipelines(BaseTestCase):
    def test_pipeline_with_no_ops_raises(self):
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath("tests/fixtures/pipelines/pipeline_with_no_ops.yml"),
                {"kind": "compiled_operation"},
            ]
        )
        with self.assertRaises(PolyaxonSchemaError):
            CompiledOperationSpecification.apply_operation_contexts(run_config)

    def test_pipeline_with_no_components_raises(self):
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath(
                    "tests/fixtures/pipelines/pipeline_with_no_components.yml"
                ),
                {"kind": "compiled_operation"},
            ]
        )
        with self.assertRaises(PolyaxonSchemaError):
            CompiledOperationSpecification.apply_operation_contexts(run_config)

    def test_pipeline_ops_not_corresponding_to_components(self):
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath(
                    "tests/fixtures/pipelines/pipeline_ops_not_corresponding_to_components.yml"
                ),
                {"kind": "compiled_operation"},
            ]
        )
        with self.assertRaises(PolyaxonSchemaError):
            CompiledOperationSpecification.apply_operation_contexts(run_config)

    def test_cyclic_pipeline_raises(self):
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath("tests/fixtures/pipelines/cyclic_pipeline.yml"),
                {"kind": "compiled_operation"},
            ]
        )
        assert run_config.is_dag_run is True
        assert run_config.has_pipeline is True
        with self.assertRaises(PolyaxonSchemaError):
            CompiledOperationSpecification.apply_operation_contexts(run_config)

    def test_cron_pipeline(self):
        plx_file = check_polyaxonfile(
            polyaxonfile=os.path.abspath(
                "tests/fixtures/pipelines/simple_cron_pipeline.yml"
            ),
            is_cli=False,
            to_op=False,
        )
        # Get compiled_operation data
        run_config = OperationSpecification.compile_operation(plx_file)

        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        assert run_config.run is not None
        assert len(run_config.run.operations) == 1
        assert run_config.run.operations[0].name == "cron-task"
        assert run_config.schedule is not None
        assert run_config.schedule.kind == "cron"
        assert run_config.schedule.cron == "0 0 * * *"

    def test_refs_pipeline(self):
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath("tests/fixtures/pipelines/ref_pipeline.yml"),
                {"kind": "compiled_operation"},
            ]
        )
        with patch("polyaxon.config_reader.spec.ConfigSpec.read") as config_read:
            config_read.return_value = V1Component(
                kind="component",
                version=" 1.1",
                inputs=[V1IO(name="str-input", iotype="str")],
                run=V1Job(container=V1Container(name="test")),
            ).to_dict()
            compiled_op = CompiledOperationSpecification.apply_operation_contexts(
                run_config
            )
        assert compiled_op.run is not None
        assert len(compiled_op.run.operations) == 2
        assert compiled_op.run.operations[0].name == "ref-path-op"
        assert compiled_op.run.operations[1].name == "ref-url-op"

    def test_interval_pipeline(self):
        plx_file = check_polyaxonfile(
            polyaxonfile=os.path.abspath(
                "tests/fixtures/pipelines/simple_recurrent_pipeline.yml"
            ),
            is_cli=False,
            to_op=False,
        )
        # Get compiled_operation data
        run_config = OperationSpecification.compile_operation(plx_file)

        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        assert run_config.run is not None
        assert len(run_config.run.operations) == 1
        assert run_config.run.operations[0].name == "recurrent-task"
        assert run_config.schedule is not None
        assert run_config.schedule.kind == "interval"
        assert run_config.schedule.start_at.year == 2019
        assert run_config.schedule.frequency.seconds == 120
        assert run_config.schedule.depends_on_past is True
        assert run_config.schedule is not None

    def test_sequential_pipeline(self):
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath(
                    "tests/fixtures/pipelines/simple_sequential_pipeline.yml"
                ),
                {"kind": "compiled_operation"},
            ]
        )

        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        assert run_config.run is not None
        assert len(run_config.run.operations) == 4
        assert run_config.run.operations[0].name == "job1"
        assert run_config.run.operations[1].name == "job2"
        assert run_config.run.operations[1].dependencies == ["job1"]
        assert run_config.run.operations[2].name == "experiment1"
        assert run_config.run.operations[2].dependencies == ["job2"]
        assert run_config.run.operations[3].name == "experiment2"
        assert run_config.run.operations[3].dependencies == ["experiment1"]
        dag_strategy = run_config.run
        assert dag_strategy.sort_topologically(dag_strategy.dag) == [
            ["job1"],
            ["job2"],
            ["experiment1"],
            ["experiment2"],
        ]
        assert run_config.schedule is None

    def test_parallel_pipeline(self):
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath(
                    "tests/fixtures/pipelines/simple_parallel_pipeline.yml"
                ),
                {"kind": "compiled_operation"},
            ]
        )

        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        assert len(run_config.run.operations) == 4
        assert run_config.run.operations[0].name == "job1"
        assert run_config.run.operations[0].dependencies is None
        assert run_config.run.operations[1].name == "job2"
        assert run_config.run.operations[1].dependencies is None
        assert run_config.run.operations[2].name == "experiment1"
        assert run_config.run.operations[2].dependencies is None
        assert run_config.run.operations[3].name == "experiment2"
        assert run_config.run.operations[3].dependencies is None
        dag_strategy = run_config.run
        assert set(dag_strategy.sort_topologically(dag_strategy.dag)[0]) == {
            "job1",
            "job2",
            "experiment1",
            "experiment2",
        }
        assert run_config.run.concurrency == 2
        assert run_config.schedule is None

    def test_dag_pipeline(self):
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath("tests/fixtures/pipelines/simple_dag_pipeline.yml"),
                {"kind": "compiled_operation"},
            ]
        )

        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        assert len(run_config.run.operations) == 5
        assert run_config.run.operations[0].name == "job1"
        assert run_config.run.operations[1].name == "experiment1"
        assert run_config.run.operations[1].dependencies == ["job1"]
        assert run_config.run.operations[2].name == "experiment2"
        assert run_config.run.operations[2].dependencies == ["job1"]
        assert run_config.run.operations[3].name == "experiment3"
        assert run_config.run.operations[3].dependencies == ["job1"]
        assert run_config.run.operations[4].name == "job2"
        assert run_config.run.operations[4].dependencies == [
            "experiment1",
            "experiment2",
            "experiment3",
        ]
        dag_strategy = run_config.run
        sorted_dag = dag_strategy.sort_topologically(dag_strategy.dag)
        assert sorted_dag[0] == ["job1"]
        assert set(sorted_dag[1]) == {"experiment1", "experiment2", "experiment3"}
        assert sorted_dag[2] == ["job2"]
        assert run_config.run.concurrency == 3
        assert run_config.schedule is None

    def test_build_run_pipeline(self):
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath("tests/fixtures/pipelines/build_run_pipeline.yml"),
                {"kind": "compiled_operation"},
            ]
        )

        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        assert len(run_config.run.operations) == 2
        assert run_config.run.operations[0].name == "build"
        assert run_config.run.operations[1].name == "run"
        assert run_config.is_dag_run is True
        assert run_config.has_pipeline is True
        assert run_config.schedule is None
        assert len(run_config.run.components) == 2
        assert run_config.run.components[0].name == "experiment-template"
        assert run_config.run.components[0].termination.to_dict() == {"maxRetries": 2}
        assert run_config.run.components[0].run.to_dict() == {
            "kind": V1RunKind.JOB,
            "environment": {
                "nodeSelector": {"polyaxon": "experiments"},
                "serviceAccountName": "service",
                "imagePullSecrets": ["secret1", "secret2"],
            },
            "container": {
                "image": "{{ image }}",
                "command": ["python3", "main.py"],
                "args": "--lr={{ lr }}",
                "name": "polyaxon-main",
                "resources": {"requests": {"cpu": 1}},
            },
        }
        assert run_config.run.components[1].name == "build-template"
        assert run_config.run.components[1].run.container.image == "base"
        assert run_config.run.operations[0].name == "build"

        # Create a an op spec
        run_config.run.set_op_component("run")
        assert run_config.run.operations[1].has_component_reference is True
        job_config = run_config.run.get_op_spec_by_index(1)
        assert {p: job_config.params[p].to_dict() for p in job_config.params} == {
            "image": {"value": "outputs.docker-image", "ref": "ops.build"},
            "lr": {"value": 0.001},
        }
        run_config = OperationSpecification.compile_operation(job_config)
        run_config.apply_params({"image": {"value": "foo"}, "lr": {"value": 0.001}})
        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        run_config = CompiledOperationSpecification.apply_runtime_contexts(run_config)
        assert run_config.termination.to_dict() == {"maxRetries": 2}
        assert run_config.run.to_dict() == {
            "kind": V1RunKind.JOB,
            "environment": {
                "nodeSelector": {"polyaxon": "experiments"},
                "serviceAccountName": "service",
                "imagePullSecrets": ["secret1", "secret2"],
            },
            "container": {
                "image": "foo",
                "command": ["python3", "main.py"],
                "args": "--lr=0.001",
                "name": "polyaxon-main",
                "resources": {"requests": {"cpu": 1}},
            },
        }

    def test_matrix_early_stopping_file_passes(self):
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath(
                    "tests/fixtures/pipelines/matrix_file_early_stopping.yml"
                ),
                {"kind": "compiled_operation"},
            ]
        )

        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        assert run_config.run is not None
        assert run_config.is_dag_run is True
        assert run_config.has_pipeline is True
        assert run_config.schedule is None
        assert run_config.run.concurrency == 4
        assert isinstance(run_config.run, V1Dag)
        assert run_config.run.early_stopping[0].kind == "failure_early_stopping"
        assert isinstance(run_config.run.early_stopping[0], V1FailureEarlyStopping)
        assert len(run_config.run.early_stopping) == 1
        assert run_config.run.kind == V1Dag.IDENTIFIER
        assert len(run_config.run.operations) == 2
        assert len(run_config.run.components) == 1
        template_random = run_config.run.operations[1].matrix
        assert isinstance(template_random, V1RandomSearch)
        assert isinstance(template_random.params["lr"], V1HpLinSpace)
        assert isinstance(template_random.params["loss"], V1HpChoice)
        assert template_random.params["lr"].to_dict() == {
            "kind": "linspace",
            "value": {"start": 0.01, "stop": 0.1, "num": 5},
        }
        assert template_random.params["loss"].to_dict() == {
            "kind": "choice",
            "value": ["MeanSquaredError", "AbsoluteDifference"],
        }
        assert template_random.concurrency == 2
        assert template_random.num_runs == 300
        assert template_random.early_stopping[0].kind == "metric_early_stopping"
        assert len(template_random.early_stopping) == 1
        assert isinstance(template_random.early_stopping[0], V1MetricEarlyStopping)

    def test_matrix_file_passess(self):
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath("tests/fixtures/pipelines/matrix_file.yml"),
                {"kind": "compiled_operation"},
            ]
        )
        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        assert run_config.version == 1.1
        assert run_config.is_dag_run is True
        assert run_config.has_pipeline is True
        assert run_config.schedule is None
        assert run_config.run.concurrency == 4
        assert isinstance(run_config.run, V1Dag)
        assert run_config.run.early_stopping is None
        assert run_config.run.kind == V1Dag.IDENTIFIER
        assert len(run_config.run.operations) == 2
        assert len(run_config.run.components) == 1
        template_hyperband = run_config.run.operations[1].matrix
        assert isinstance(template_hyperband.params["lr"], V1HpLinSpace)
        assert isinstance(template_hyperband.params["loss"], V1HpChoice)
        assert template_hyperband.params["lr"].to_dict() == {
            "kind": "linspace",
            "value": {"start": 0.01, "stop": 0.1, "num": 5},
        }
        assert template_hyperband.params["loss"].to_dict() == {
            "kind": "choice",
            "value": ["MeanSquaredError", "AbsoluteDifference"],
        }
        assert template_hyperband.params["normal_rate"].to_dict() == {
            "kind": "normal",
            "value": {"loc": 0, "scale": 0.9},
        }
        assert template_hyperband.params["dropout"].to_dict() == {
            "kind": "qloguniform",
            "value": {"high": 0.8, "low": 0, "q": 0.1},
        }
        assert template_hyperband.params["activation"].to_dict() == {
            "kind": "pchoice",
            "value": [["relu", 0.1], ["sigmoid", 0.8]],
        }
        assert template_hyperband.params["model"].to_dict() == {
            "kind": "choice",
            "value": ["CDNA", "DNA", "STP"],
        }
        assert template_hyperband.concurrency == 2
        assert isinstance(template_hyperband, V1Hyperband)

    def test_matrix_file_passes_int_float_types(self):
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath(
                    "tests/fixtures/pipelines/matrix_file_with_int_float_types.yml"
                ),
                {"kind": "compiled_operation"},
            ]
        )

        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        assert run_config.version == 1.1
        assert run_config.is_dag_run is True
        assert run_config.has_pipeline is True
        assert run_config.schedule is None
        assert run_config.run.concurrency == 4
        assert isinstance(run_config.run, V1Dag)
        assert run_config.run.early_stopping is None
        assert run_config.run.kind == V1Dag.IDENTIFIER
        assert len(run_config.run.operations) == 2
        assert len(run_config.run.components) == 1
        template_grid = run_config.run.operations[1].matrix
        assert isinstance(template_grid, V1GridSearch)
        assert isinstance(template_grid.params["param1"], V1HpChoice)
        assert isinstance(template_grid.params["param2"], V1HpChoice)
        assert template_grid.params["param1"].to_dict() == {
            "kind": "choice",
            "value": [1, 2],
        }
        assert template_grid.params["param2"].to_dict() == {
            "kind": "choice",
            "value": [3.3, 4.4],
        }
        assert template_grid.concurrency == 2
        assert template_grid.early_stopping is None
