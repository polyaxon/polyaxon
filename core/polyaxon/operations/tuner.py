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

from polyaxon import types
from polyaxon.auxiliaries import get_default_tuner_container
from polyaxon.k8s.k8s_schemas import V1Container
from polyaxon.polyflow import (
    V1IO,
    V1Bayes,
    V1Component,
    V1Hyperband,
    V1Hyperopt,
    V1Join,
    V1Matrix,
    V1Operation,
    V1Param,
    V1Plugins,
    V1Tuner,
)
from polyaxon.polypod.common.containers import patch_container


def get_tuner(
    name: str,
    container: V1Container,
    matrix: V1Matrix,
    join: V1Join,
    iteration: int,
    bracket_iteration: int = None,
) -> V1Operation:
    params = {
        "matrix": V1Param(value=matrix.to_dict()),
        "join": V1Param(value=join.to_dict()),
        "iteration": V1Param(value=iteration),
    }
    inputs = [
        V1IO(name="matrix", type=types.DICT, is_list=False, is_optional=True),
        V1IO(name="join", type=types.DICT, is_list=False, is_optional=True),
        V1IO(name="iteration", type=types.INT, is_list=False, is_optional=True),
    ]
    if bracket_iteration is not None:
        params["bracket_iteration"] = V1Param(value=bracket_iteration)
        inputs.append(
            V1IO(
                name="bracket_iteration",
                type=types.INT,
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
                    type=types.DICT,
                    is_list=True,
                    is_optional=False,
                ),
            ],
            run=V1Tuner(
                container=container,
            ),
        ),
    )


def get_container(
    tuner_container: V1Container, container: V1Container = None
) -> V1Container:
    if container:
        return patch_container(
            container=container,
            name=container.name,
            image=tuner_container.image,
            image_pull_policy=tuner_container.image_pull_policy,
            command=tuner_container.command,
            args=tuner_container.args,
            env=tuner_container.env,
            env_from=tuner_container.env_from,
            volume_mounts=tuner_container.volume_mounts,
            resources=tuner_container.resources,
        )
    return tuner_container


def get_bo_tuner(
    matrix: V1Bayes,
    join: V1Join,
    iteration: int,
) -> V1Operation:
    iteration = matrix.create_iteration(iteration)
    return get_tuner(
        name="bayesian-tuner",
        container=get_container(
            tuner_container=get_default_tuner_container(["polyaxon", "tuner", "bayes"]),
            container=matrix.container,
        ),
        matrix=matrix,
        join=join,
        iteration=iteration,
    )


def get_hyperband_tuner(
    matrix: V1Hyperband,
    join: V1Join,
    iteration: int,
    bracket_iteration: int,
) -> V1Operation:
    matrix.set_tuning_params()
    iteration, bracket_iteration = matrix.create_iteration(iteration, bracket_iteration)
    return get_tuner(
        name="hyperband-tuner",
        container=get_container(
            tuner_container=get_default_tuner_container(
                ["polyaxon", "tuner", "hyperband"],
                bracket_iteration=bracket_iteration,
            ),
            container=matrix.container,
        ),
        matrix=matrix,
        join=join,
        iteration=iteration,
        bracket_iteration=bracket_iteration,
    )


def get_hyperopt_tuner(
    matrix: V1Hyperopt,
    join: V1Join,
    iteration: int,
) -> V1Operation:
    iteration = matrix.create_iteration(iteration)
    return get_tuner(
        name="hyperopt-tuner",
        container=get_container(
            tuner_container=get_default_tuner_container(
                ["polyaxon", "tuner", "hyperopt"]
            ),
            container=matrix.container,
        ),
        matrix=matrix,
        join=join,
        iteration=iteration,
    )
