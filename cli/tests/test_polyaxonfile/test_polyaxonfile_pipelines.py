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
from polyaxon.schemas.polyflow.early_stopping import (
    FailureEarlyStoppingConfig,
    MetricEarlyStoppingConfig,
)
from polyaxon.schemas.polyflow.init.build_context import (
    POLYAXON_DOCKER_SHELL,
    POLYAXON_DOCKER_WORKDIR,
    POLYAXON_DOCKERFILE_NAME,
)
from polyaxon.schemas.polyflow.parallel import (
    GridSearchConfig,
    HyperbandConfig,
    RandomSearchConfig,
)
from polyaxon.schemas.polyflow.parallel.matrix import (
    MatrixChoiceConfig,
    MatrixLinSpaceConfig,
)
from polyaxon.schemas.polyflow.run import DagConfig
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
        assert plx_file.specification.has_dag_run is True
        assert plx_file.specification.has_pipeline is True
        assert plx_file.specification.meta_info.to_dict() == {
            "service": False,
            "concurrency": None,
            "run_kind": "dag",
            "parallel_kind": None,
        }
        with self.assertRaises(PolyaxonSchemaError):
            plx_file.specification.apply_context()

    def test_cron_pipeline(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/simple_cron_pipeline.yml")
        )
        spec = plx_file.specification
        spec = spec.apply_context()
        assert spec.config.run is not None
        assert len(spec.config.run.ops) == 1
        assert spec.config.run.ops[0].name == "cron-task"
        assert spec.config.schedule is not None
        assert spec.config.schedule.kind == "cron"
        assert spec.config.schedule.cron == "0 0 * * *"
        assert spec.schedule is not None
        assert spec.schedule_kind == "cron"
        assert spec.schedule_cron == "0 0 * * *"
        assert plx_file.specification.meta_info.to_dict() == {
            "service": False,
            "concurrency": None,
            "run_kind": "dag",
            "parallel_kind": None,
        }

    def test_interval_pipeline(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/simple_recurrent_pipeline.yml")
        )
        spec = plx_file.specification
        spec = spec.apply_context()
        assert spec.config.run is not None
        assert len(spec.config.run.ops) == 1
        assert spec.config.run.ops[0].name == "recurrent-task"
        assert spec.config.schedule is not None
        assert spec.config.schedule.kind == "interval"
        assert spec.config.schedule.start_at.year == 2019
        assert spec.config.schedule.frequency.seconds == 120
        assert spec.config.schedule.depends_on_past is True
        assert spec.schedule is not None
        assert spec.schedule_kind == "interval"
        assert spec.schedule_start_at.year == 2019
        assert spec.schedule_frequency.seconds == 120
        assert spec.schedule_depends_on_past is True

    def test_sequential_pipeline(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/simple_sequential_pipeline.yml")
        )
        spec = plx_file.specification
        spec = spec.apply_context()
        assert spec.config.run is not None
        assert len(spec.config.run.ops) == 4
        assert spec.config.run.ops[0].name == "job1"
        assert spec.config.run.ops[1].name == "job2"
        assert spec.config.run.ops[1].dependencies == ["job1"]
        assert spec.config.run.ops[2].name == "experiment1"
        assert spec.config.run.ops[2].dependencies == ["job2"]
        assert spec.config.run.ops[3].name == "experiment2"
        assert spec.config.run.ops[3].dependencies == ["experiment1"]
        dag_strategy = spec.config.run
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
        assert len(spec.config.run.ops) == 4
        assert spec.config.run.ops[0].name == "job1"
        assert spec.config.run.ops[0].dependencies is None
        assert spec.config.run.ops[1].name == "job2"
        assert spec.config.run.ops[1].dependencies is None
        assert spec.config.run.ops[2].name == "experiment1"
        assert spec.config.run.ops[2].dependencies is None
        assert spec.config.run.ops[3].name == "experiment2"
        assert spec.config.run.ops[3].dependencies is None
        dag_strategy = spec.config.run
        assert set(dag_strategy.sort_topologically(dag_strategy.dag)[0]) == {
            "job1",
            "job2",
            "experiment1",
            "experiment2",
        }
        assert spec.config.run.concurrency == 2
        assert spec.config.schedule is None
        assert spec.run_concurrency == 2
        assert spec.schedule is None

    def test_dag_pipeline(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/simple_dag_pipeline.yml")
        )
        spec = plx_file.specification
        spec = spec.apply_context()
        assert len(spec.config.run.ops) == 5
        assert spec.config.run.ops[0].name == "job1"
        assert spec.config.run.ops[1].name == "experiment1"
        assert spec.config.run.ops[1].dependencies == ["job1"]
        assert spec.config.run.ops[2].name == "experiment2"
        assert spec.config.run.ops[2].dependencies == ["job1"]
        assert spec.config.run.ops[3].name == "experiment3"
        assert spec.config.run.ops[3].dependencies == ["job1"]
        assert spec.config.run.ops[4].name == "job2"
        assert spec.config.run.ops[4].dependencies == [
            "experiment1",
            "experiment2",
            "experiment3",
        ]
        dag_strategy = spec.config.run
        sorted_dag = dag_strategy.sort_topologically(dag_strategy.dag)
        assert sorted_dag[0] == ["job1"]
        assert set(sorted_dag[1]) == {"experiment1", "experiment2", "experiment3"}
        assert sorted_dag[2] == ["job2"]
        assert spec.config.run.concurrency == 3
        assert spec.config.schedule is None
        assert spec.run_concurrency == 3
        assert spec.schedule is None

    def test_build_run_pipeline(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/build_run_pipeline.yml")
        )
        spec = plx_file.specification
        spec = spec.apply_context()
        assert len(spec.run.ops) == 2
        assert spec.run.ops[0].name == "build"
        assert spec.run.ops[1].name == "run"
        assert spec.has_dag_run is True
        assert spec.has_pipeline is True
        assert spec.config.schedule is None
        assert len(spec.run.components) == 2
        assert spec.run.components[0].name == "experiment-template"
        assert spec.run.components[0].run.to_dict() == {
            "kind": "container",
            "image": "{{ image }}",
            "command": ["python3", "main.py"],
            "args": "--lr={{ lr }}",
        }
        assert spec.run.components[1].name == "build-template"
        assert spec.run.components[1].run.to_light_dict() == {
            "kind": "container",
            "image": "base",
        }
        assert spec.run.components[1].init.build.to_light_dict() == {
            "image": "base",
            "env": "{{ env_vars }}",
            "name": POLYAXON_DOCKERFILE_NAME,
            "workdir": POLYAXON_DOCKER_WORKDIR,
            "shell": POLYAXON_DOCKER_SHELL,
        }

        # Create a an op spec
        spec.run.set_op_component("run")
        assert spec.run.ops[1].component is not None
        job_spec = OpSpecification(spec.run.ops[1].to_dict())
        assert job_spec.config.params == {
            "image": "{{ ops.build.outputs.docker-image }}",
            "lr": 0.001,
        }
        op_spec = get_specification(job_spec.generate_run_data())
        assert op_spec.is_component is True
        op_spec.apply_params({"image": "foo", "lr": 0.001})
        op_spec = op_spec.apply_context()
        op_spec = op_spec.apply_run_contexts()
        assert op_spec.config.run.to_dict() == {
            "kind": "container",
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
        assert spec.config.run is not None
        assert spec.has_dag_run is True
        assert spec.has_pipeline is True
        assert spec.config.schedule is None
        assert spec.run.concurrency == 4
        assert spec.run_concurrency == 4
        assert isinstance(spec.run, DagConfig)
        assert spec.run.early_stopping[0].kind == "failure_early_stopping"
        assert isinstance(spec.run_early_stopping[0], FailureEarlyStoppingConfig)
        assert len(spec.run_early_stopping) == 1
        assert spec.run_kind == DagConfig.IDENTIFIER
        assert len(spec.run.ops) == 2
        assert len(spec.run.components) == 1
        template_random = spec.run.components[0].parallel
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
        assert template_random.concurrency == 2
        assert template_random.n_runs == 300
        assert template_random.early_stopping[0].kind == "metric_early_stopping"
        assert len(template_random.early_stopping) == 1
        assert isinstance(template_random.early_stopping[0], MetricEarlyStoppingConfig)

    def test_matrix_file_passess(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/matrix_file.yml")
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.version == 1.0
        assert spec.is_component is True
        assert spec.has_dag_run is True
        assert spec.has_pipeline is True
        assert spec.config.schedule is None
        assert spec.run.concurrency == 4
        assert spec.run_concurrency == 4
        assert isinstance(spec.run, DagConfig)
        assert spec.run.early_stopping is None
        assert spec.run_early_stopping == []
        assert spec.run_kind == DagConfig.IDENTIFIER
        assert len(spec.run.ops) == 2
        assert len(spec.run.components) == 1
        template_hyperband = spec.run.components[0].parallel
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
        assert template_hyperband.concurrency == 2
        assert isinstance(template_hyperband, HyperbandConfig)

    def test_matrix_file_passes_int_float_types(self):
        plxfile = PolyaxonFile(
            os.path.abspath(
                "tests/fixtures/pipelines/matrix_file_with_int_float_types.yml"
            )
        )
        spec = plxfile.specification
        spec = spec.apply_context()
        assert spec.version == 1.0
        assert spec.is_component is True
        assert spec.has_dag_run is True
        assert spec.has_pipeline is True
        assert spec.config.schedule is None
        assert spec.run.concurrency == 4
        assert spec.run_concurrency == 4
        assert isinstance(spec.run, DagConfig)
        assert spec.run.early_stopping is None
        assert spec.run_early_stopping == []
        assert spec.run_kind == DagConfig.IDENTIFIER
        assert len(spec.run.ops) == 2
        assert len(spec.run.components) == 1
        template_grid = spec.run.components[0].parallel
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
        assert template_grid.concurrency == 2
        assert template_grid.early_stopping is None
