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

from polyaxon.polyflow import (
    V1Bayes,
    V1Hyperband,
    V1Hyperopt,
    V1Join,
    V1Matrix,
    V1Operation,
    V1Param,
    V1Tuner,
)


def get_tuner(
    tuner: V1Tuner,
    matrix: V1Matrix,
    join: V1Join,
    iteration: int,
    bracket_iteration: int = None,
) -> V1Operation:
    params = {
        "matrix": V1Param(value=matrix.to_light_dict()),
        "iteration": V1Param(value=iteration),
    }
    if bracket_iteration is not None:
        params["bracket_iteration"] = V1Param(value=bracket_iteration)

    if tuner.params:
        params.update(tuner.params)

    return V1Operation(
        queue=tuner.queue,
        joins=[join],
        params=params,
        hub_ref=tuner.hub_ref,
        presets=tuner.presets,
    )


def get_bo_tuner(
    matrix: V1Bayes,
    join: V1Join,
    iteration: int,
    tuner: V1Tuner = None,
) -> V1Operation:
    tuner = tuner or V1Tuner()
    tuner.hub_ref = tuner.hub_ref or "bayes-tuner"
    iteration = matrix.create_iteration(iteration)
    return get_tuner(
        tuner=tuner,
        matrix=matrix,
        join=join,
        iteration=iteration,
    )


def get_hyperband_tuner(
    matrix: V1Hyperband,
    join: V1Join,
    iteration: int,
    bracket_iteration: int,
    tuner: V1Tuner = None,
) -> V1Operation:
    tuner = tuner or V1Tuner()
    tuner.hub_ref = tuner.hub_ref or "hyperband-tuner"
    matrix.set_tuning_params()
    iteration, bracket_iteration = matrix.create_iteration(iteration, bracket_iteration)
    return get_tuner(
        tuner=tuner,
        matrix=matrix,
        join=join,
        iteration=iteration,
        bracket_iteration=bracket_iteration,
    )


def get_hyperopt_tuner(
    matrix: V1Hyperopt,
    join: V1Join,
    iteration: int,
    tuner: V1Tuner = None,
) -> V1Operation:
    tuner = tuner or V1Tuner()
    tuner.hub_ref = tuner.hub_ref or "hyperopt-tuner"
    iteration = matrix.create_iteration(iteration)
    return get_tuner(
        tuner=tuner,
        matrix=matrix,
        join=join,
        iteration=iteration,
    )
