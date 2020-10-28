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

from polyaxon import types
from polyaxon.auxiliaries import get_default_tuner_container
from polyaxon.k8s.k8s_schemas import V1Container
from polyaxon.polyflow import (
    V1IO,
    V1Bayes,
    V1Component,
    V1Hyperband,
    V1Hyperopt,
    V1Matrix,
    V1Operation,
    V1Param,
    V1ParamSearch,
    V1Plugins,
    V1Termination,
    V1Tuner,
)


def get_tuner(
    name: str,
    container: V1Container,
    matrix: V1Matrix,
    search: V1ParamSearch,
    iteration: int,
    bracket_iteration: int = None,
) -> V1Operation:
    params = {
        "matrix": V1Param(value=matrix.to_dict()),
        "search": V1Param(value=search.to_dict()),
        "iteration": V1Param(value=iteration),
    }
    inputs = [
        V1IO(name="matrix", iotype=types.DICT, is_list=False, is_optional=True),
        V1IO(name="search", iotype=types.DICT, is_list=False, is_optional=True),
        V1IO(name="iteration", iotype=types.INT, is_list=False, is_optional=True),
    ]
    if bracket_iteration is not None:
        params["bracket_iteration"] = V1Param(value=bracket_iteration)
        inputs.append(
            V1IO(
                name="bracket_iteration",
                iotype=types.INT,
                is_list=False,
                is_optional=True,
            )
        )
    return V1Operation(
        params=params,
        component=V1Component(
            name=name,
            plugins=V1Plugins(
                auth=True,
                collect_logs=True,
                collect_artifacts=True,
                collect_resources=False,
                sync_statuses=False,
            ),
            inputs=inputs,
            outputs=[
                V1IO(
                    name="suggestions",
                    iotype=types.DICT,
                    is_list=True,
                    is_optional=False,
                ),
            ],
            run=V1Tuner(
                container=container,
            ),
        ),
    )


def get_bo_tuner(
    matrix: V1Bayes,
    search: V1ParamSearch,
    iteration: int,
    container: V1Container = None,
) -> V1Operation:
    iteration = matrix.create_iteration(iteration)
    container = container or get_default_tuner_container(["polyaxon", "tuner", "bayes"])
    return get_tuner(
        name="bayesian-tuner",
        container=container,
        matrix=matrix,
        search=search,
        iteration=iteration,
    )


def get_hyperband_tuner(
    matrix: V1Hyperband,
    search: V1ParamSearch,
    iteration: int,
    bracket_iteration: int,
    container: V1Container = None,
) -> V1Operation:
    matrix.set_tuning_params()
    iteration, bracket_iteration = matrix.create_iteration(iteration, bracket_iteration)
    container = container or get_default_tuner_container(
        ["polyaxon", "tuner", "hyperband"],
        bracket_iteration=bracket_iteration,
    )
    return get_tuner(
        name="hyperband-tuner",
        container=container,
        matrix=matrix,
        search=search,
        iteration=iteration,
        bracket_iteration=bracket_iteration,
    )


def get_hyperopt_tuner(
    matrix: V1Hyperopt,
    search: V1ParamSearch,
    iteration: int,
    container: V1Container = None,
) -> V1Operation:
    iteration = matrix.create_iteration(iteration)
    container = container or get_default_tuner_container(
        ["polyaxon", "tuner", "hyperopt"]
    )
    return get_tuner(
        name="hyperopt-tuner",
        container=container,
        matrix=matrix,
        search=search,
        iteration=iteration,
    )
