# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

import pytest

from polyaxon_schemas.exceptions import PolyaxonfileError
from polyaxon_schemas.ops.container import ContainerConfig
from polyaxon_schemas.ops.parallel import GridSearchConfig, ParallelConfig
from polyaxon_schemas.ops.parallel.matrix import MatrixChoiceConfig
from polyaxon_schemas.polyaxonfile import PolyaxonFile


@pytest.mark.polyaxonfile_mark
class TestPolyaxonfileWithTypes(TestCase):
    def test_using_untyped_params_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath("tests/fixtures/typing/untyped_params.yml"))

    def test_no_params_for_required_inputs_outputs_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath("tests/fixtures/typing/required_inputs.yml"))

        PolyaxonFile(os.path.abspath("tests/fixtures/typing/required_outputs.yml"))

    def test_required_inputs_with_params(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/typing/required_inputs.yml"),
            params={"loss": "bar", "flag": False},
        )
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 0.6
        assert spec.tags == {"foo": "bar"}
        assert spec.params == {"loss": "bar", "flag": ""}
        assert spec.container.image == "my_image"
        assert spec.container.command == ["/bin/sh", "-c"]
        assert spec.container.args == "video_prediction_train --loss=bar "
        assert spec.environment is None
        assert spec.is_job

        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/typing/required_inputs.yml"),
            params={"loss": "bar", "flag": True},
        )
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 0.6
        assert spec.tags == {"foo": "bar"}
        assert spec.params == {"loss": "bar", "flag": "--flag"}
        assert spec.container.image == "my_image"
        assert spec.container.command == ["/bin/sh", "-c"]
        assert spec.container.args == "video_prediction_train --loss=bar --flag"
        assert spec.environment is None
        assert spec.is_job

        # Adding extra value raises
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(
                os.path.abspath("tests/fixtures/typing/required_inputs.yml"),
                params={"loss": "bar", "value": 1.1},
            )

        # Adding non valid params raises
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(
                os.path.abspath("tests/fixtures/typing/required_inputs.yml"),
                params={"value": 1.1},
            )

    def test_matrix_file_passes_int_float_types(self):
        plxfile = PolyaxonFile(
            os.path.abspath(
                "tests/fixtures/typing/matrix_file_with_int_float_types.yml"
            )
        )
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_job
        assert isinstance(spec.parallel.algorithm.matrix["param1"], MatrixChoiceConfig)
        assert isinstance(spec.parallel.algorithm.matrix["param2"], MatrixChoiceConfig)
        assert spec.parallel.algorithm.matrix["param1"].to_dict() == {
            "kind": "choice",
            "value": [1, 2],
        }
        assert spec.parallel.algorithm.matrix["param2"].to_dict() == {
            "kind": "choice",
            "value": [3.3, 4.4],
        }
        assert isinstance(spec.parallel, ParallelConfig)
        assert spec.concurrency == 2
        assert isinstance(spec.parallel_algorithm, GridSearchConfig)
        assert spec.parallel_algorithm_kind == GridSearchConfig.IDENTIFIER
        assert spec.parallel.early_stopping is None
        assert spec.early_stopping == []

        # TODO
        # spec = spec.get_experiment_spec(matrix_declaration=get_matrix_declaration_test(spec))
        # spec.apply_context()
        # assert spec.environment is None
        # assert spec.framework is None
        # assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        # assert (
        #     spec.run.cmd
        #     == "train --param1={param1} --param2={param2} --param3=23423".format(
        #         **spec.params
        #     )
        # )

    def test_run_simple_file_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/typing/run_cmd_simple_file.yml")
        )
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 0.6
        assert spec.tags == {"foo": "bar"}
        assert spec.is_job
        assert spec.environment is None
        container = spec.container
        assert isinstance(container, ContainerConfig)
        assert container.image == "my_image"
        assert container.command == ["/bin/sh", "-c"]
        assert container.args == [
            "video_prediction_train",
            "--num_masks=2",
            "--loss=MeanSquaredError",
        ]

    def test_run_with_refs(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/typing/run_with_refs.yml")
        )
        spec = plxfile.specification
        required_refs = spec.raw_config.get_params_with_refs()
        assert len(required_refs) == 1
        assert required_refs[0].name == "model_path"
        assert required_refs[0].value == "runs.64332180bfce46eba80a65caf73c5396.outputs.doo"
        spec.apply_context(
            context={"runs__64332180bfce46eba80a65caf73c5396__outputs__doo": "model_path"}
        )
        assert spec.version == 0.6
        assert spec.tags == {"foo": "bar"}
        assert spec.is_job
        container = spec.container
        assert isinstance(container, ContainerConfig)
        assert container.image == "my_image"
        assert container.command == ["/bin/sh", "-c"]
        assert container.args == [
            "video_prediction_train",
            "--num_masks=2",
            "--model_path=model_path",
        ]
