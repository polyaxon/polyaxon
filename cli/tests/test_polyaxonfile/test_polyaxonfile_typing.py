# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

import pytest

from polyaxon.exceptions import PolyaxonfileError
from polyaxon.schemas.ops.container import ContainerConfig
from polyaxon.schemas.ops.io import IOConfig
from polyaxon.schemas.ops.parallel import GridSearchConfig, ParallelConfig
from polyaxon.schemas.ops.parallel.matrix import MatrixChoiceConfig
from polyaxon.schemas.ops.params import get_params_with_refs
from polyaxon.schemas.polyaxonfile import PolyaxonFile


@pytest.mark.polyaxonfile_mark
class TestPolyaxonfileWithTypes(TestCase):
    def test_using_untyped_params_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath("tests/fixtures/typing/untyped_params.yml"))

    def test_no_params_for_required_inputs_outputs_raises(self):
        plx = PolyaxonFile(os.path.abspath("tests/fixtures/typing/required_inputs.yml"))
        with self.assertRaises(PolyaxonfileError):
            plx.specification.apply_context()
        plx = PolyaxonFile(
            os.path.abspath("tests/fixtures/typing/required_outputs.yml")
        )
        with self.assertRaises(PolyaxonfileError):
            plx.specification.apply_context()

    def test_required_inputs_with_params(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/typing/required_inputs.yml")
        )
        spec = plxfile.specification
        with self.assertRaises(PolyaxonfileError):
            spec.apply_context()

        assert spec.config.inputs[0].value is None
        assert spec.config.inputs[1].value is None
        spec.apply_params(params={"loss": "bar", "flag": False})
        assert spec.config.inputs[0].value == "bar"
        assert spec.config.inputs[1].value is False
        spec = spec.apply_context()
        spec = spec.apply_container_contexts()
        assert spec.version == 0.6
        assert spec.tags == ["foo", "bar"]
        assert spec.container.image == "my_image"
        assert spec.container.command == ["/bin/sh", "-c"]
        assert spec.container.args == "video_prediction_train --loss=bar "
        assert spec.environment is None
        assert spec.is_job

        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/typing/required_inputs.yml")
        )
        spec = plxfile.specification
        assert spec.config.inputs[0].value is None
        assert spec.config.inputs[1].value is None
        spec.apply_params(params={"loss": "bar", "flag": True})
        assert spec.config.inputs[0].value == "bar"
        assert spec.config.inputs[1].value is True
        spec = spec.apply_context()
        spec = spec.apply_container_contexts()
        assert spec.version == 0.6
        assert spec.tags == ["foo", "bar"]
        assert spec.container.image == "my_image"
        assert spec.container.command == ["/bin/sh", "-c"]
        assert spec.container.args == "video_prediction_train --loss=bar --flag"
        assert spec.environment is None
        assert spec.is_job

        # Adding extra value raises
        with self.assertRaises(PolyaxonfileError):
            spec.validate_params(params={"loss": "bar", "flag": True, "value": 1.1})
        with self.assertRaises(PolyaxonfileError):
            polyaxonfile = PolyaxonFile(
                os.path.abspath("tests/fixtures/typing/required_inputs.yml")
            )
            polyaxonfile.get_op_specification(params={"loss": "bar", "value": 1.1})

        # Adding non valid params raises
        with self.assertRaises(PolyaxonfileError):
            spec.validate_params(params={"value": 1.1})

    def test_matrix_file_passes_int_float_types(self):
        plxfile = PolyaxonFile(
            os.path.abspath(
                "tests/fixtures/typing/matrix_file_with_int_float_types.yml"
            )
        )
        spec = plxfile.specification
        spec = spec.apply_context()
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
        assert spec.config.inputs[0].value == "MeanSquaredError"
        assert spec.config.inputs[1].value is None
        validated_params = spec.validate_params()
        assert spec.config.inputs[0].value == "MeanSquaredError"
        assert spec.config.inputs[1].value is None
        assert {"loss": "MeanSquaredError", "num_masks": None} == {
            p.name: p.value for p in validated_params
        }
        with self.assertRaises(PolyaxonfileError):
            spec.apply_context()

        validated_params = spec.validate_params(params={"num_masks": 100})
        assert {"loss": "MeanSquaredError", "num_masks": 100} == {
            p.name: p.value for p in validated_params
        }
        assert spec.container.args == [
            "video_prediction_train",
            "--num_masks={{num_masks}}",
            "--loss={{loss}}",
        ]

        with self.assertRaises(
            PolyaxonfileError
        ):  # Applying context before applying params
            spec.apply_context()

        spec.apply_params(params={"num_masks": 100})
        new_spec = spec.apply_context()
        new_spec = new_spec.apply_container_contexts()
        assert new_spec.version == 0.6
        assert new_spec.tags == ["foo", "bar"]
        assert new_spec.is_job
        assert new_spec.environment is None
        container = new_spec.container
        assert isinstance(container, ContainerConfig)
        assert container.image == "my_image"
        assert container.command == ["/bin/sh", "-c"]
        assert container.args == [
            "video_prediction_train",
            "--num_masks=100",
            "--loss=MeanSquaredError",
        ]

    def test_run_with_refs(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/typing/run_with_refs.yml")
        )
        spec = plxfile.specification
        params = {
            "num_masks": 2,
            "model_path": "{{ runs.64332180bfce46eba80a65caf73c5396.outputs.doo }}",
        }
        validated_params = spec.validate_params(params=params)
        assert {
            "num_masks": 2,
            "model_path": "runs.64332180bfce46eba80a65caf73c5396.outputs.doo",
        } == {p.name: p.value for p in validated_params}
        ref_param = get_params_with_refs(validated_params)[0]
        assert ref_param == validated_params[0]
        assert ref_param.name == "model_path"
        assert ref_param.entity == "runs"
        assert ref_param.value == "runs.64332180bfce46eba80a65caf73c5396.outputs.doo"

        with self.assertRaises(PolyaxonfileError):
            spec.apply_params(params=params)

        spec.apply_params(
            params=params,
            context={
                "runs.64332180bfce46eba80a65caf73c5396.outputs.doo": IOConfig(
                    name="model_path",
                    value="model_path",
                    is_optional=True,
                    iotype="path",
                )
            },
        )

        params = {"num_masks": 2, "model_path": "{{ ops.A.outputs.doo }}"}
        validated_params = spec.validate_params(params=params)
        assert {"num_masks": 2, "model_path": "ops.A.outputs.doo"} == {
            p.name: p.value for p in validated_params
        }
        ref_param = get_params_with_refs(validated_params)[0]
        assert ref_param == validated_params[0]
        assert ref_param.name == "model_path"
        assert ref_param.entity == "ops"
        assert ref_param.value == "ops.A.outputs.doo"

        with self.assertRaises(PolyaxonfileError):
            spec.apply_params(params=params)

        spec.apply_params(
            params=params,
            context={
                "ops.A.outputs.doo": IOConfig(
                    name="model_path",
                    value="model_path",
                    is_optional=True,
                    iotype="path",
                )
            },
        )
