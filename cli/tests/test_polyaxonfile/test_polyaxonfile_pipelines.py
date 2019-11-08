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

from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.polyaxonfile import PolyaxonFile
from polyaxon.schemas.polyflow.init.build_context import (
    POLYAXON_DOCKER_SHELL,
    POLYAXON_DOCKER_WORKDIR,
    POLYAXON_DOCKERFILE_NAME,
)
from polyaxon.schemas.polyflow.workflows import (
    DagConfig,
    GridSearchConfig,
    HyperbandConfig,
    RandomSearchConfig,
    WorkflowConfig,
)
from polyaxon.schemas.polyflow.workflows.early_stopping_policies import (
    FailureEarlyStoppingConfig,
    MetricEarlyStoppingConfig,
)
from polyaxon.schemas.polyflow.workflows.matrix import (
    MatrixChoiceConfig,
    MatrixLinSpaceConfig,
)
from polyaxon.specs import OpSpecification, get_specification


@pytest.mark.polyaxonfile_mark
class TestPolyaxonfileWithPipelines(TestCase):
    def test_pipeline_with_no_ops_raises(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/pipeline_with_no_ops.yml")
        )
        with self.assertRaises(PolyaxonSchemaError):
            plx_file.specification.apply_context()

    def test_pipeline_with_no_components_raises(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/pipeline_with_no_components.yml")
        )
        with self.assertRaises(PolyaxonSchemaError):
            plx_file.specification.apply_context()

    def test_pipeline_ops_not_corresponding_to_components(self):
        plx_file = PolyaxonFile(
            os.path.abspath(
                "tests/fixtures/pipelines/pipeline_ops_not_corresponding_to_components.yml"
            )
        )
        with self.assertRaises(PolyaxonSchemaError):
            plx_file.specification.apply_context()

    def test_cyclic_pipeline_raises(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/cyclic_pipeline.yml")
        )
        assert plx_file.specification.has_dag is True
        assert plx_file.specification.has_pipeline is True
        with self.assertRaises(PolyaxonSchemaError):
            plx_file.specification.apply_context()

    def test_cron_pipeline(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/simple_cron_pipeline.yml")
        )
        spec = plx_file.specification
        spec = spec.apply_context()
        assert spec.config.workflow is not None
        assert len(spec.config.workflow.strategy.ops) == 1
        assert spec.config.workflow.strategy.ops[0].name == "cron-task"
        assert spec.config.schedule is not None
        assert spec.config.schedule.kind == "cron"
        assert spec.config.schedule.cron == "0 0 * * *"
        assert spec.schedule is not None
        assert spec.schedule_kind == "cron"
        assert spec.schedule_cron == "0 0 * * *"

    def test_interval_pipeline(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/simple_recurrent_pipeline.yml")
        )
        spec = plx_file.specification
        spec = spec.apply_context()
        assert spec.config.workflow is not None
        assert len(spec.config.workflow.strategy.ops) == 1
        assert spec.config.workflow.strategy.ops[0].name == "recurrent-task"
        assert spec.config.schedule is not None
        assert spec.config.schedule.kind == "interval"
        assert spec.config.schedule.start_at.year == 2019
        assert spec.config.schedule.frequency == 120
        assert spec.config.schedule.depends_on_past is True
        assert spec.schedule is not None
        assert spec.schedule_kind == "interval"
        assert spec.schedule_start_at.year == 2019
        assert spec.schedule_frequency == 120
        assert spec.schedule_depends_on_past is True

    def test_sequential_pipeline(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/simple_sequential_pipeline.yml")
        )
        spec = plx_file.specification
        spec = spec.apply_context()
        assert spec.config.workflow is not None
        assert len(spec.config.workflow.strategy.ops) == 4
        assert spec.config.workflow.strategy.ops[0].name == "job1"
        assert spec.config.workflow.strategy.ops[1].name == "job2"
        assert spec.config.workflow.strategy.ops[1].dependencies == ["job1"]
        assert spec.config.workflow.strategy.ops[2].name == "experiment1"
        assert spec.config.workflow.strategy.ops[2].dependencies == ["job2"]
        assert spec.config.workflow.strategy.ops[3].name == "experiment2"
        assert spec.config.workflow.strategy.ops[3].dependencies == ["experiment1"]
        dag_strategy = spec.config.workflow.strategy
        assert dag_strategy.sort_topologically(dag_strategy.dag) == [
            ["job1"],
            ["job2"],
            ["experiment1"],
            ["experiment2"],
        ]
        assert spec.config.schedule is None

    def test_parallel_pipeline(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/simple_parallel_pipeline.yml")
        )
        spec = plx_file.specification
        spec = spec.apply_context()
        assert len(spec.config.workflow.strategy.ops) == 4
        assert spec.config.workflow.strategy.ops[0].name == "job1"
        assert spec.config.workflow.strategy.ops[0].dependencies is None
        assert spec.config.workflow.strategy.ops[1].name == "job2"
        assert spec.config.workflow.strategy.ops[1].dependencies is None
        assert spec.config.workflow.strategy.ops[2].name == "experiment1"
        assert spec.config.workflow.strategy.ops[2].dependencies is None
        assert spec.config.workflow.strategy.ops[3].name == "experiment2"
        assert spec.config.workflow.strategy.ops[3].dependencies is None
        dag_strategy = spec.config.workflow.strategy
        assert set(dag_strategy.sort_topologically(dag_strategy.dag)[0]) == {
            "job1",
            "job2",
            "experiment1",
            "experiment2",
        }
        assert spec.config.workflow.concurrency == 2
        assert spec.config.schedule is None
        assert spec.concurrency == 2
        assert spec.schedule is None

    def test_dag_pipeline(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/simple_dag_pipeline.yml")
        )
        spec = plx_file.specification
        spec = spec.apply_context()
        assert len(spec.config.workflow.strategy.ops) == 5
        assert spec.config.workflow.strategy.ops[0].name == "job1"
        assert spec.config.workflow.strategy.ops[1].name == "experiment1"
        assert spec.config.workflow.strategy.ops[1].dependencies == ["job1"]
        assert spec.config.workflow.strategy.ops[2].name == "experiment2"
        assert spec.config.workflow.strategy.ops[2].dependencies == ["job1"]
        assert spec.config.workflow.strategy.ops[3].name == "experiment3"
        assert spec.config.workflow.strategy.ops[3].dependencies == ["job1"]
        assert spec.config.workflow.strategy.ops[4].name == "job2"
        assert spec.config.workflow.strategy.ops[4].dependencies == [
            "experiment1",
            "experiment2",
            "experiment3",
        ]
        dag_strategy = spec.config.workflow.strategy
        sorted_dag = dag_strategy.sort_topologically(dag_strategy.dag)
        assert sorted_dag[0] == ["job1"]
        assert set(sorted_dag[1]) == {"experiment1", "experiment2", "experiment3"}
        assert sorted_dag[2] == ["job2"]
        assert spec.config.workflow.concurrency == 3
        assert spec.config.schedule is None
        assert spec.concurrency == 3
        assert spec.schedule is None

    def test_build_run_pipeline(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/build_run_pipeline.yml")
        )
        spec = plx_file.specification
        spec = spec.apply_context()
        assert len(spec.workflow_strategy.ops) == 2
        assert spec.workflow_strategy.ops[0].name == "build"
        assert spec.workflow_strategy.ops[1].name == "run"
        assert spec.config.workflow is not None
        assert spec.has_dag is True
        assert spec.has_pipeline is True
        assert spec.config.schedule is None
        assert len(spec.workflow_strategy.components) == 2
        assert spec.workflow_strategy.components[0].name == "experiment-template"
        assert spec.workflow_strategy.components[0].container.to_dict() == {
            "image": "{{ image }}",
            "command": ["python3", "main.py"],
            "args": "--lr={{ lr }}",
        }
        assert spec.workflow_strategy.components[1].name == "build-template"
        assert spec.workflow_strategy.components[1].container.to_light_dict() == {
            "image": "base"
        }
        assert spec.workflow_strategy.components[1].init.build.to_light_dict() == {
            "image": "base",
            "env": "{{ env_vars }}",
            "name": POLYAXON_DOCKERFILE_NAME,
            "workdir": POLYAXON_DOCKER_WORKDIR,
            "shell": POLYAXON_DOCKER_SHELL,
        }

        # Create a an op spec
        spec.workflow_strategy.set_op_component("run")
        assert spec.workflow_strategy.ops[1].component is not None
        job_spec = OpSpecification(spec.workflow_strategy.ops[1].to_dict())
        assert job_spec.config.params == {
            "image": "{{ ops.build.outputs.docker-image }}",
            "lr": 0.001,
        }
        op_spec = get_specification(job_spec.generate_run_data())
        assert op_spec.is_component is True
        op_spec.apply_params({"image": "foo", "lr": 0.001})
        op_spec = op_spec.apply_context()
        op_spec = op_spec.apply_container_contexts()
        assert op_spec.config.container.to_dict() == {
            "image": "foo",
            "command": ["python3", "main.py"],
            "args": "--lr=0.001",
        }

    def test_matrix_early_stopping_file_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/matrix_file_early_stopping.yml")
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.config.workflow is not None
        assert spec.has_dag is True
        assert spec.has_pipeline is True
        assert spec.config.schedule is None
        assert spec.workflow.concurrency == 4
        assert spec.concurrency == 4
        assert isinstance(spec.workflow, WorkflowConfig)
        assert isinstance(spec.workflow.strategy, DagConfig)
        assert spec.workflow.early_stopping[0].kind == "failure_early_stopping"
        assert isinstance(spec.early_stopping[0], FailureEarlyStoppingConfig)
        assert len(spec.early_stopping) == 1
        assert spec.workflow_strategy_kind == DagConfig.IDENTIFIER
        assert len(spec.workflow.strategy.ops) == 2
        assert len(spec.workflow.strategy.components) == 1
        template_workflow = spec.workflow.strategy.components[0].workflow
        template_random = template_workflow.strategy
        assert isinstance(template_random, RandomSearchConfig)
        assert isinstance(template_random.matrix["lr"], MatrixLinSpaceConfig)
        assert isinstance(template_random.matrix["loss"], MatrixChoiceConfig)
        assert template_random.matrix["lr"].to_dict() == {
            "kind": "linspace",
            "value": {"start": 0.01, "stop": 0.1, "num": 5},
        }
        assert template_random.matrix["loss"].to_dict() == {
            "kind": "choice",
            "value": ["MeanSquaredError", "AbsoluteDifference"],
        }
        assert template_workflow.concurrency == 2
        assert template_random.n_experiments == 300
        assert template_workflow.early_stopping[0].kind == "metric_early_stopping"
        assert len(template_workflow.early_stopping) == 1
        assert isinstance(
            template_workflow.early_stopping[0], MetricEarlyStoppingConfig
        )

    def test_matrix_file_passess(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/matrix_file.yml")
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_component is True
        assert spec.has_dag is True
        assert spec.has_pipeline is True
        assert spec.config.schedule is None
        assert spec.workflow.concurrency == 4
        assert spec.concurrency == 4
        assert isinstance(spec.workflow, WorkflowConfig)
        assert isinstance(spec.workflow.strategy, DagConfig)
        assert spec.workflow.early_stopping is None
        assert spec.early_stopping == []
        assert spec.workflow_strategy_kind == DagConfig.IDENTIFIER
        assert len(spec.workflow.strategy.ops) == 2
        assert len(spec.workflow.strategy.components) == 1
        template_workflow = spec.workflow.strategy.components[0].workflow
        template_hyperband = template_workflow.strategy
        assert isinstance(template_hyperband.matrix["lr"], MatrixLinSpaceConfig)
        assert isinstance(template_hyperband.matrix["loss"], MatrixChoiceConfig)
        assert template_hyperband.matrix["lr"].to_dict() == {
            "kind": "linspace",
            "value": {"start": 0.01, "stop": 0.1, "num": 5},
        }
        assert template_hyperband.matrix["loss"].to_dict() == {
            "kind": "choice",
            "value": ["MeanSquaredError", "AbsoluteDifference"],
        }
        assert template_hyperband.matrix["normal_rate"].to_dict() == {
            "kind": "normal",
            "value": {"loc": 0, "scale": 0.9},
        }
        assert template_hyperband.matrix["dropout"].to_dict() == {
            "kind": "qloguniform",
            "value": {"high": 0.8, "low": 0, "q": 0.1},
        }
        assert template_hyperband.matrix["activation"].to_dict() == {
            "kind": "pchoice",
            "value": [["relu", 0.1], ["sigmoid", 0.8]],
        }
        assert template_hyperband.matrix["model"].to_dict() == {
            "kind": "choice",
            "value": ["CDNA", "DNA", "STP"],
        }
        assert template_workflow.concurrency == 2
        assert isinstance(template_hyperband, HyperbandConfig)

    def test_matrix_file_passes_int_float_types(self):
        plxfile = PolyaxonFile(
            os.path.abspath(
                "tests/fixtures/pipelines/matrix_file_with_int_float_types.yml"
            )
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_component is True
        assert spec.has_dag is True
        assert spec.has_pipeline is True
        assert spec.config.schedule is None
        assert spec.workflow.concurrency == 4
        assert spec.concurrency == 4
        assert isinstance(spec.workflow, WorkflowConfig)
        assert isinstance(spec.workflow.strategy, DagConfig)
        assert spec.workflow.early_stopping is None
        assert spec.early_stopping == []
        assert spec.workflow_strategy_kind == DagConfig.IDENTIFIER
        assert len(spec.workflow.strategy.ops) == 2
        assert len(spec.workflow.strategy.components) == 1
        template_workflow = spec.workflow.strategy.components[0].workflow
        template_grid = template_workflow.strategy
        assert isinstance(template_grid, GridSearchConfig)
        assert isinstance(template_grid.matrix["param1"], MatrixChoiceConfig)
        assert isinstance(template_grid.matrix["param2"], MatrixChoiceConfig)
        assert template_grid.matrix["param1"].to_dict() == {
            "kind": "choice",
            "value": [1, 2],
        }
        assert template_grid.matrix["param2"].to_dict() == {
            "kind": "choice",
            "value": [3.3, 4.4],
        }
        assert template_workflow.concurrency == 2
        assert template_workflow.early_stopping is None
