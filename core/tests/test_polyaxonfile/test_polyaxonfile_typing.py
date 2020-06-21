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
from polyaxon.k8s import k8s_schemas
from polyaxon.polyaxonfile import check_polyaxonfile
from polyaxon.polyaxonfile.specs import (
    CompiledOperationSpecification,
    OperationSpecification,
)
from polyaxon.polyflow import V1CompiledOperation, V1Hyperband
from polyaxon.polyflow.io import V1IO
from polyaxon.polyflow.matrix import V1GridSearch
from polyaxon.polyflow.matrix.params import V1HpChoice, V1HpLinSpace
from polyaxon.polyflow.params import V1Param


@pytest.mark.polyaxonfile_mark
class TestPolyaxonfileWithTypes(BaseTestCase):
    def test_using_untyped_params_raises(self):
        with self.assertRaises(PolyaxonfileError):
            check_polyaxonfile(
                polyaxonfile=os.path.abspath(
                    "tests/fixtures/typing/untyped_params.yml"
                ),
                is_cli=False,
            )

    def test_no_params_for_required_inputs_outputs_raises(self):
        # Get compiled_operation data
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath("tests/fixtures/typing/required_inputs.yml"),
                {"kind": "compiled_operation"},
            ]
        )

        # Inputs don't have delayed validation by default
        with self.assertRaises(ValidationError):
            CompiledOperationSpecification.apply_operation_contexts(run_config)

        run_config = V1CompiledOperation.read(
            [
                os.path.abspath("tests/fixtures/typing/required_outputs.yml"),
                {"kind": "compiled_operation"},
            ]
        )
        # Outputs have delayed validation by default
        CompiledOperationSpecification.apply_operation_contexts(run_config)

    def test_validation_for_required_inputs_outputs_raises(self):
        # Get compiled_operation data
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath("tests/fixtures/typing/required_inputs.yml"),
                {"kind": "compiled_operation"},
            ]
        )
        # Inputs don't have delayed validation by default
        with self.assertRaises(ValidationError):
            run_config.validate_params(is_template=False, check_runs=True)

        run_config = V1CompiledOperation.read(
            [
                os.path.abspath("tests/fixtures/typing/required_outputs.yml"),
                {"kind": "compiled_operation"},
            ]
        )
        # Outputs have delayed validation by default
        run_config.validate_params(is_template=False, check_runs=True)

    def test_required_inputs_with_params(self):
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath("tests/fixtures/typing/required_inputs.yml"),
                {"kind": "compiled_operation"},
            ]
        )

        with self.assertRaises(ValidationError):
            CompiledOperationSpecification.apply_operation_contexts(run_config)

        assert run_config.inputs[0].value is None
        assert run_config.inputs[1].value is None
        run_config.apply_params(
            params={"loss": {"value": "bar"}, "flag": {"value": False}}
        )
        assert run_config.inputs[0].value == "bar"
        assert run_config.inputs[1].value is False
        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        run_config = CompiledOperationSpecification.apply_runtime_contexts(run_config)
        assert run_config.version == 1.1
        assert run_config.tags == ["foo", "bar"]
        assert run_config.run.container.image == "my_image"
        assert run_config.run.container.command == ["/bin/sh", "-c"]
        assert run_config.run.container.args == "video_prediction_train --loss=bar "

        run_config = V1CompiledOperation.read(
            [
                os.path.abspath("tests/fixtures/typing/required_inputs.yml"),
                {"kind": "compiled_operation"},
            ]
        )

        assert run_config.inputs[0].value is None
        assert run_config.inputs[1].value is None
        run_config.apply_params(
            params={"loss": {"value": "bar"}, "flag": {"value": True}}
        )
        assert run_config.inputs[0].value == "bar"
        assert run_config.inputs[1].value is True
        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        run_config = CompiledOperationSpecification.apply_runtime_contexts(run_config)
        assert run_config.version == 1.1
        assert run_config.tags == ["foo", "bar"]
        assert run_config.run.container.image == "my_image"
        assert run_config.run.container.command == ["/bin/sh", "-c"]
        assert (
            run_config.run.container.args == "video_prediction_train --loss=bar --flag"
        )

        # Adding extra value raises
        with self.assertRaises(ValidationError):
            run_config.validate_params(
                params={
                    "loss": {"value": "bar"},
                    "flag": {"value": True},
                    "value": {"value": 1.1},
                }
            )
        with self.assertRaises(PolyaxonfileError):
            check_polyaxonfile(
                polyaxonfile=os.path.abspath(
                    "tests/fixtures/typing/required_inputs.yml"
                ),
                params={"loss": {"value": "bar"}, "value": {"value": 1.1}},
                is_cli=False,
            )

        # Adding non valid params raises
        with self.assertRaises(ValidationError):
            run_config.validate_params(params={"value": {"value": 1.1}})

    def test_matrix_file_passes_int_float_types(self):
        plxfile = check_polyaxonfile(
            polyaxonfile=os.path.abspath(
                "tests/fixtures/typing/matrix_file_with_int_float_types.yml"
            ),
            is_cli=False,
            to_op=False,
        )
        # Get compiled_operation data
        run_config = OperationSpecification.compile_operation(plxfile)

        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        assert run_config.version == 1.1
        assert run_config.has_pipeline
        assert run_config.is_dag_run is False
        assert isinstance(run_config.matrix.params["param1"], V1HpChoice)
        assert isinstance(run_config.matrix.params["param2"], V1HpChoice)
        assert run_config.matrix.params["param1"].to_dict() == {
            "kind": "choice",
            "value": [1, 2],
        }
        assert run_config.matrix.params["param2"].to_dict() == {
            "kind": "choice",
            "value": [3.3, 4.4],
        }
        assert isinstance(run_config.matrix, V1GridSearch)
        assert run_config.matrix.concurrency == 2
        assert run_config.matrix.kind == V1GridSearch.IDENTIFIER
        assert run_config.matrix.early_stopping is None

    def test_matrix_job_file_passes_int_float_types(self):
        plxfile = check_polyaxonfile(
            polyaxonfile=os.path.abspath(
                "tests/fixtures/typing/matrix_job_file_with_int_float_types.yml"
            ),
            is_cli=False,
            to_op=False,
        )
        # Get compiled_operation data
        run_config = OperationSpecification.compile_operation(plxfile)

        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        assert run_config.version == 1.1
        assert isinstance(run_config.matrix.params["param1"], V1HpChoice)
        assert isinstance(run_config.matrix.params["param2"], V1HpChoice)
        assert run_config.matrix.params["param1"].to_dict() == {
            "kind": "choice",
            "value": [1, 2],
        }
        assert run_config.matrix.params["param2"].to_dict() == {
            "kind": "choice",
            "value": [3.3, 4.4],
        }
        assert isinstance(run_config.matrix, V1GridSearch)
        assert run_config.matrix.concurrency == 2
        assert run_config.matrix.kind == V1GridSearch.IDENTIFIER
        assert run_config.matrix.early_stopping is None

    def test_matrix_file_with_required_inputs_and_wrong_matrix_type_fails(self):
        with self.assertRaises(PolyaxonfileError):
            check_polyaxonfile(
                polyaxonfile=os.path.abspath(
                    "tests/fixtures/typing/matrix_job_required_inputs_file_wrong_matrix_type.yml"
                ),
                is_cli=False,
            )

    def test_matrix_file_with_required_inputs_passes(self):
        plx_file = check_polyaxonfile(
            polyaxonfile=os.path.abspath(
                "tests/fixtures/typing/matrix_job_required_inputs_file.yml"
            ),
            is_cli=False,
        )
        run_config = OperationSpecification.compile_operation(plx_file)
        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        assert run_config.version == 1.1
        assert isinstance(run_config.matrix, V1Hyperband)
        assert isinstance(run_config.matrix.params["lr"], V1HpLinSpace)
        assert isinstance(run_config.matrix.params["loss"], V1HpChoice)
        assert run_config.matrix.params["lr"].to_dict() == {
            "kind": "linspace",
            "value": {"start": 0.01, "stop": 0.1, "num": 5},
        }
        assert run_config.matrix.params["loss"].to_dict() == {
            "kind": "choice",
            "value": ["MeanSquaredError", "AbsoluteDifference"],
        }
        assert run_config.matrix.concurrency == 2
        assert isinstance(run_config.matrix, V1Hyperband)
        assert run_config.matrix.kind == V1Hyperband.IDENTIFIER
        assert run_config.matrix.early_stopping is None

    def test_run_simple_file_passes(self):
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath("tests/fixtures/typing/run_cmd_simple_file.yml"),
                {"kind": "compiled_operation"},
            ]
        )

        assert run_config.inputs[0].value == "MeanSquaredError"
        assert run_config.inputs[1].value is None
        validated_params = run_config.validate_params()
        assert run_config.inputs[0].value == "MeanSquaredError"
        assert run_config.inputs[1].value is None
        assert {
            "loss": V1Param(value="MeanSquaredError"),
            "num_masks": V1Param(value=None),
        } == {p.name: p.param for p in validated_params}
        with self.assertRaises(ValidationError):
            CompiledOperationSpecification.apply_operation_contexts(run_config)

        validated_params = run_config.validate_params(
            params={"num_masks": {"value": 100}}
        )
        assert {
            "loss": V1Param(value="MeanSquaredError"),
            "num_masks": V1Param(value=100),
        } == {p.name: p.param for p in validated_params}
        assert run_config.run.container.args == [
            "video_prediction_train",
            "--num_masks={{num_masks}}",
            "--loss={{loss}}",
        ]

        with self.assertRaises(ValidationError):
            # Applying context before applying params
            CompiledOperationSpecification.apply_operation_contexts(run_config)

        run_config.apply_params(params={"num_masks": {"value": 100}})
        run_config = CompiledOperationSpecification.apply_operation_contexts(run_config)
        run_config = CompiledOperationSpecification.apply_runtime_contexts(run_config)
        assert run_config.version == 1.1
        assert run_config.tags == ["foo", "bar"]
        container = run_config.run.container
        assert isinstance(container, k8s_schemas.V1Container)
        assert container.image == "my_image"
        assert container.command == ["/bin/sh", "-c"]
        assert container.args == [
            "video_prediction_train",
            "--num_masks=100",
            "--loss=MeanSquaredError",
        ]

    def test_run_with_refs(self):
        # Get compiled_operation data
        run_config = V1CompiledOperation.read(
            [
                os.path.abspath("tests/fixtures/typing/run_with_refs.yml"),
                {"kind": "compiled_operation"},
            ]
        )
        params = {
            "num_masks": {"value": 2},
            "model_path": {
                "ref": "runs.64332180bfce46eba80a65caf73c5396",
                "value": "outputs.doo",
            },
        }
        validated_params = run_config.validate_params(params=params)
        param_specs_by_name = {p.name: p.param for p in validated_params}
        assert param_specs_by_name == {
            "num_masks": V1Param(value=2),
            "model_path": V1Param(
                ref="runs.64332180bfce46eba80a65caf73c5396", value="outputs.doo"
            ),
        }
        ref_param = param_specs_by_name["model_path"]
        assert ref_param.to_dict() == params["model_path"]

        with self.assertRaises(ValidationError):
            run_config.apply_params(params=params)

        # Passing correct context
        run_config.apply_params(
            params=params,
            context={
                "runs.64332180bfce46eba80a65caf73c5396.outputs.doo": V1IO(
                    name="model_path",
                    value="model_path",
                    is_optional=True,
                    iotype="path",
                )
            },
        )

        # New params
        params = {
            "num_masks": {"value": 2},
            "model_path": {"ref": "ops.A", "value": "outputs.doo"},
        }
        validated_params = run_config.validate_params(params=params)
        param_specs_by_name = {p.name: p.param for p in validated_params}
        assert param_specs_by_name == {
            "num_masks": V1Param(value=2),
            "model_path": V1Param(ref="ops.A", value="outputs.doo"),
        }

        ref_param = param_specs_by_name["model_path"]
        assert ref_param.to_dict() == params["model_path"]

        with self.assertRaises(ValidationError):
            run_config.apply_params(params=params)

        run_config.apply_params(
            params=params,
            context={
                "ops.A.outputs.doo": V1IO(
                    name="model_path",
                    value="model_path",
                    is_optional=True,
                    iotype="path",
                )
            },
        )
