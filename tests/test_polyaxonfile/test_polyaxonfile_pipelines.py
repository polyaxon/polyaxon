# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

import pytest

from polyaxon_schemas.exceptions import PolyaxonSchemaError
from polyaxon_schemas.polyaxonfile import PolyaxonFile
from polyaxon_schemas.specs import OperationSpecification, get_specification


@pytest.mark.polyaxonfile_mark
class TestPolyaxonfileWithPipelines(TestCase):
    def test_pipeline_with_no_ops_raises(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/pipeline_with_no_ops.yml")
        )
        with self.assertRaises(PolyaxonSchemaError):
            plx_file.specification.apply_context()

    def test_pipeline_with_no_templates_raises(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/pipeline_with_no_templates.yml")
        )
        with self.assertRaises(PolyaxonSchemaError):
            plx_file.specification.apply_context()

    def test_pipeline_ops_not_corresponding_to_templates(self):
        plx_file = PolyaxonFile(
            os.path.abspath(
                "tests/fixtures/pipelines/pipeline_ops_not_corresponding_to_templates.yml"
            )
        )
        with self.assertRaises(PolyaxonSchemaError):
            plx_file.specification.apply_context()

    def test_cyclic_pipeline_raises(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/cyclic_pipeline.yml")
        )
        with self.assertRaises(PolyaxonSchemaError):
            plx_file.specification.apply_context()

    def test_cron_pipeline(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/simple_cron_pipeline.yml")
        )
        spec = plx_file.specification
        spec = spec.apply_context()
        assert len(spec.config.ops) == 1
        assert spec.config.ops[0].name == "cron-task"
        assert spec.config.parallel is None
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
        assert len(spec.config.ops) == 1
        assert spec.config.ops[0].name == "recurrent-task"
        assert spec.config.parallel is None
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
        assert len(spec.config.ops) == 4
        assert spec.config.ops[0].name == "job1"
        assert spec.config.ops[1].name == "job2"
        assert spec.config.ops[1].dependencies == ["job1"]
        assert spec.config.ops[2].name == "experiment1"
        assert spec.config.ops[2].dependencies == ["job2"]
        assert spec.config.ops[3].name == "experiment2"
        assert spec.config.ops[3].dependencies == ["experiment1"]
        assert spec.config.sort_topologically(spec.config.dag) == [
            ["job1"],
            ["job2"],
            ["experiment1"],
            ["experiment2"],
        ]
        assert spec.config.parallel is None
        assert spec.config.schedule is None

    def test_parallel_pipeline(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/simple_parallel_pipeline.yml")
        )
        spec = plx_file.specification
        spec = spec.apply_context()
        assert len(spec.config.ops) == 4
        assert spec.config.ops[0].name == "job1"
        assert spec.config.ops[0].dependencies is None
        assert spec.config.ops[1].name == "job2"
        assert spec.config.ops[1].dependencies is None
        assert spec.config.ops[2].name == "experiment1"
        assert spec.config.ops[2].dependencies is None
        assert spec.config.ops[3].name == "experiment2"
        assert spec.config.ops[3].dependencies is None
        assert set(spec.config.sort_topologically(spec.config.dag)[0]) == {
            "job1",
            "job2",
            "experiment1",
            "experiment2",
        }
        assert spec.config.parallel.concurrency == 2
        assert spec.config.schedule is None
        assert spec.concurrency == 2
        assert spec.schedule is None

    def test_dag_pipeline(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/simple_dag_pipeline.yml")
        )
        spec = plx_file.specification
        spec = spec.apply_context()
        assert len(spec.config.ops) == 5
        assert spec.config.ops[0].name == "job1"
        assert spec.config.ops[1].name == "experiment1"
        assert spec.config.ops[1].dependencies == ["job1"]
        assert spec.config.ops[2].name == "experiment2"
        assert spec.config.ops[2].dependencies == ["job1"]
        assert spec.config.ops[3].name == "experiment3"
        assert spec.config.ops[3].dependencies == ["job1"]
        assert spec.config.ops[4].name == "job2"
        assert spec.config.ops[4].dependencies == [
            "experiment1",
            "experiment2",
            "experiment3",
        ]
        srorted_dag = spec.config.sort_topologically(spec.config.dag)
        assert srorted_dag[0] == ["job1"]
        assert set(srorted_dag[1]) == {"experiment1", "experiment2", "experiment3"}
        assert srorted_dag[2] == ["job2"]
        assert spec.config.parallel.concurrency == 3
        assert spec.config.schedule is None
        assert spec.concurrency == 3
        assert spec.schedule is None

    def test_build_run_pipeline(self):
        plx_file = PolyaxonFile(
            os.path.abspath("tests/fixtures/pipelines/build_run_pipeline.yml")
        )
        spec = plx_file.specification
        spec = spec.apply_context()
        assert len(spec.config.ops) == 2
        assert spec.config.ops[0].name == "build"
        assert spec.config.ops[1].name == "run"
        assert spec.config.parallel is None
        assert spec.config.schedule is None
        assert len(spec.config.ops) == 2
        assert spec.config.templates[0].name == "experiment-template"
        assert spec.config.templates[0].container.to_dict() == {
            "image": "{{ image }}",
            "command": ["python3", "main.py"],
            "args": "--lr={{ lr }}",
        }
        assert spec.config.templates[1].name == "build-template"
        assert spec.config.templates[1].container.to_light_dict() == {"image": "base"}
        assert spec.config.templates[1].init.build.to_light_dict() == {
            "image": "base",
            "env_vars": "{{ env_vars }}",
        }

        # Create a an op spec
        spec.config.set_op_template("run")
        assert spec.config.ops[1]._template is not None
        op_spec = OperationSpecification(spec.config.ops[1].to_dict())
        assert op_spec.config.params == {
            "image": "{{ ops.build.outputs.docker-image }}",
            "lr": 0.001,
        }
        job_spec = get_specification(op_spec.generate_run_data())
        assert job_spec.is_job is True
        job_spec.apply_params({"image": "foo", "lr": 0.001})
        job_spec = job_spec.apply_context()
        assert job_spec.config.container.to_dict() == {
            "image": "foo",
            "command": ["python3", "main.py"],
            "args": "--lr=0.001",
        }
