#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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
import copy

from collections.abc import Mapping
from typing import Dict, List, Union

from polyaxon import pkg
from polyaxon.env_vars.getters.queue import get_queue_info
from polyaxon.exceptions import PolyaxonfileError
from polyaxon.polyaxonfile.specs import (
    CompiledOperationSpecification,
    OperationSpecification,
    get_specification,
    kinds,
)
from polyaxon.polyflow import V1Component, V1Init, V1Matrix, V1MatrixKind, V1Operation
from polyaxon.schemas import V1PatchStrategy
from polyaxon.utils.bool_utils import to_bool


def get_op_specification(
    config: Union[V1Component, V1Operation] = None,
    hub: str = None,
    params: Dict = None,
    hparams: Dict = None,
    matrix_kind: str = None,
    matrix_concurrency: int = None,
    matrix_num_runs: int = None,
    matrix: V1Matrix = None,
    presets: List[str] = None,
    queue: str = None,
    nocache: bool = None,
    cache: Union[int, str, bool] = None,
    approved: Union[int, str, bool] = None,
    validate_params: bool = True,
    preset_files: List[str] = None,
    git_init: V1Init = None,
) -> V1Operation:
    if cache and nocache:
        raise PolyaxonfileError("Received both 'cache' and 'nocache'")
    op_data = {
        "version": config.version if config else pkg.SCHEMA_VERSION,
        "kind": kinds.OPERATION,
    }
    if params:
        if not isinstance(params, Mapping):
            raise PolyaxonfileError(
                "Params: `{}` must be a valid mapping".format(params)
            )
        op_data["params"] = params
    if hparams:
        if not isinstance(hparams, Mapping):
            raise PolyaxonfileError(
                "Hyper-Params: `{}` must be a valid mapping".format(hparams)
            )
        op_data["matrix"] = {
            "kind": matrix_kind or V1MatrixKind.GRID,
            "concurrency": matrix_concurrency or 1,
            "params": hparams,
        }
        if matrix_num_runs:
            op_data["matrix"]["numRuns"] = matrix_num_runs
    if matrix:
        op_data["matrix"] = (
            matrix if isinstance(matrix, Mapping) else matrix.to_light_dict()
        )
    if presets:
        op_data["presets"] = presets
    if queue:
        # Check only
        get_queue_info(queue)
        op_data["queue"] = queue
    if cache is not None:
        op_data["cache"] = {"disable": not to_bool(cache)}
    if nocache:
        op_data["cache"] = {"disable": True}
    # Handle approval logic
    if approved is not None:
        op_data["isApproved"] = to_bool(approved)

    if config and config.kind == kinds.COMPONENT:
        op_data["component"] = config.to_dict()
        config = get_specification(data=[op_data])
    elif config and config.kind == kinds.OPERATION:
        config = get_specification(data=[config.to_dict(), op_data])
    elif hub:
        op_data["hubRef"] = hub
        config = get_specification(data=[op_data])

    if hub and config.hub_ref is None:
        config.hub_ref = hub

    # Check if there's presets
    for preset_plx_file in preset_files:
        preset_plx_file = OperationSpecification.read(preset_plx_file, is_preset=True)
        config = config.patch(preset_plx_file, strategy=preset_plx_file.patch_strategy)
    # Turn git_init to a pre_merge preset
    if git_init:
        git_preset = V1Operation(
            run_patch={"init": [git_init.to_dict()]}, is_preset=True
        )
        config = config.patch(git_preset, strategy=V1PatchStrategy.PRE_MERGE)

    # Sanity check if params were passed and we are not dealing with a hub component
    params = copy.deepcopy(config.params)
    if validate_params:
        # Avoid in-place patch
        run_config = get_specification(config.to_dict())
        run_config = OperationSpecification.compile_operation(run_config)
        run_config.validate_params(params=params, is_template=False)
        if run_config.is_dag_run:
            CompiledOperationSpecification.apply_operation_contexts(run_config)
    return config
