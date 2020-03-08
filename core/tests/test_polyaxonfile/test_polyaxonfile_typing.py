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

from polyaxon.config_reader import reader
from polyaxon.k8s import k8s_schemas
from polyaxon.polyaxonfile import PolyaxonFile
from polyaxon.polyaxonfile.specs import (
    CompiledOperationSpecification,
    OperationSpecification,
)
from polyaxon.polyflow import V1CompiledOperation
from polyaxon.polyflow.io import V1IO
from polyaxon.polyflow.io.params import V1Param
from polyaxon.polyflow.parallel import V1GridSearch
from polyaxon.polyflow.parallel.matrix import V1HpChoice


@pytest.mark.polyaxonfile_mark
class TestPolyaxonfileWithTypes(BaseTestCase):
    def test_using_untyped_params_raises(self):
        with self.assertRaises(ValidationError):
            PolyaxonFile(os.path.abspath("tests/fixtures/typing/untyped_params.yml"))

    def test_no_params_for_required_inputs_outputs_raises(self):
        # Get compiled_operation data
        run_config = V1CompiledOperation.read(
            [
                reader.read(
                    os.path.abspath("tests/fixtures/typing/required_inputs.yml")
                ),
                {"kind": "compiled_operation"},
            ]
        )

        # Inputs don't have delayed validation by default
        with self.assertRaises(ValidationError):
            CompiledOperationSpecification.apply_context(run_config)

        run_config = V1CompiledOperation.read(
            [
                reader.read(
                    os.path.abspath("tests/fixtures/typing/required_outputs.yml")
                ),
                {"kind": "compiled_operation"},
            ]
        )
        # Outputs have delayed validation by default
        CompiledOperationSpecification.apply_context(run_config)

    def test_validation_for_required_inputs_outputs_raises(self):
        # Get compiled_operation data
        run_config = V1CompiledOperation.read(
            [
                reader.read(
                    os.path.abspath("tests/fixtures/typing/required_inputs.yml")
                ),
                {"kind": "compiled_operation"},
            ]
        )
        # Inputs don't have delayed validation by default
        with self.assertRaises(ValidationError):
            run_config.validate_params(is_template=False, check_runs=True)

        run_config = V1CompiledOperation.read(
            [
                reader.read(
                    os.path.abspath("tests/fixtures/typing/required_outputs.yml")
                ),
                {"kind": "compiled_operation"},
            ]
        )
        # Outputs have delayed validation by default
        run_config.validate_params(is_template=False, check_runs=True)

    def test_required_inputs_with_params(self):
        run_config = V1CompiledOperation.read(
            [
                reader.read(
                    os.path.abspath("tests/fixtures/typing/required_inputs.yml")
                ),
                {"kind": "compiled_operation"},
            ]
        )

        with self.assertRaises(ValidationError):
            CompiledOperationSpecification.apply_context(run_config)

        assert run_config.inputs[0].value is None
        assert run_config.inputs[1].value is None
        run_config.apply_params(
            params={"loss": {"value": "bar"}, "flag": {"value": False}}
        )
        assert run_config.inputs[0].value == "bar"
        assert run_config.inputs[1].value is False
        run_config = CompiledOperationSpecification.apply_context(run_config)
        run_config = CompiledOperationSpecification.apply_run_contexts(run_config)
        assert run_config.version == 1.05
        assert run_config.tags == ["foo", "bar"]
        assert run_config.run.container.image == "my_image"
        assert run_config.run.container.command == ["/bin/sh", "-c"]
        assert run_config.run.container.args == "video_prediction_train --loss=bar "

        run_config = V1CompiledOperation.read(
            [
                reader.read(
                    os.path.abspath("tests/fixtures/typing/required_inputs.yml")
                ),
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
        run_config = CompiledOperationSpecification.apply_context(run_config)
        run_config = CompiledOperationSpecification.apply_run_contexts(run_config)
        assert run_config.version == 1.05
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
        with self.assertRaises(ValidationError):
            polyaxonfile = PolyaxonFile(
                os.path.abspath("tests/fixtures/typing/required_inputs.yml")
            )
            polyaxonfile.get_op_specification(
                params={"loss": {"value": "bar"}, "value": {"value": 1.1}},
            )

        # Adding non valid params raises
        with self.assertRaises(ValidationError):
            run_config.validate_params(params={"value": {"value": 1.1}})

    def test_matrix_file_passes_int_float_types(self):
        plxfile = PolyaxonFile(
            os.path.abspath(
                "tests/fixtures/typing/matrix_file_with_int_float_types.yml"
            )
        )
        # Get compiled_operation data
        run_config = OperationSpecification.compile_operation(plxfile.config)

        run_config = CompiledOperationSpecification.apply_context(run_config)
        assert run_config.version == 1.05
        assert run_config.has_pipeline
        assert run_config.is_dag_run is False
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
        assert isinstance(run_config.parallel, V1GridSearch)
        assert run_config.parallel.concurrency == 2
        assert run_config.parallel.kind == V1GridSearch.IDENTIFIER
        assert run_config.parallel.early_stopping is None

    def test_matrix_job_file_passes_int_float_types(self):
        plxfile = PolyaxonFile(
            os.path.abspath(
                "tests/fixtures/typing/matrix_job_file_with_int_float_types.yml"
            )
        )
        op_config = plxfile.config
        # Get compiled_operation data
        run_config = OperationSpecification.compile_operation(op_config)

        run_config = CompiledOperationSpecification.apply_context(run_config)
        assert run_config.version == 1.05
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
        assert isinstance(run_config.parallel, V1GridSearch)
        assert run_config.parallel.concurrency == 2
        assert run_config.parallel.kind == V1GridSearch.IDENTIFIER
        assert run_config.parallel.early_stopping is None

    def test_run_simple_file_passes(self):
        run_config = V1CompiledOperation.read(
            [
                reader.read(
                    os.path.abspath("tests/fixtures/typing/run_cmd_simple_file.yml")
                ),
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
            CompiledOperationSpecification.apply_context(run_config)

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
            CompiledOperationSpecification.apply_context(run_config)

        run_config.apply_params(params={"num_masks": {"value": 100}})
        run_config = CompiledOperationSpecification.apply_context(run_config)
        run_config = CompiledOperationSpecification.apply_run_contexts(run_config)
        assert run_config.version == 1.05
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
                reader.read(os.path.abspath("tests/fixtures/typing/run_with_refs.yml")),
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
