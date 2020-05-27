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
from typing import Dict, List

from polyaxon import types
from polyaxon.containers.containers import get_default_tuner_container
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
    V1Plugins,
    V1Termination,
    V1Tuner,
)


def get_tuner(
    name: str,
    container: V1Container,
    matrix: V1Matrix,
    configs: List[Dict],
    metrics: List[float],
    iteration: int,
) -> V1Operation:
    return V1Operation(
        params={
            "configs": V1Param(value=configs),
            "metrics": V1Param(value=metrics),
            "matrix": V1Param(value=matrix),
            "iteration": V1Param(value=iteration),
        },
        termination=V1Termination(max_retries=3),
        component=V1Component(
            name=name,
            plugins=V1Plugins(
                auth=True,
                collect_logs=False,
                collect_artifacts=False,
                collect_resources=False,
                sync_statuses=True,
            ),
            inputs=[
                V1IO(
                    name="configs", iotype=types.DICT, is_list=True, is_optional=False
                ),
                V1IO(
                    name="metrics", iotype=types.FLOAT, is_list=True, is_optional=False
                ),
                V1IO(
                    name="iteration", iotype=types.INT, is_list=True, is_optional=True
                ),
            ],
            outputs=[
                V1IO(
                    name="suggestions",
                    iotype=types.DICT,
                    is_list=True,
                    is_optional=False,
                ),
            ],
            run=V1Tuner(container=container,),
        ),
    )


def get_bo_tuner(
    matrix: V1Bayes,
    configs: List[Dict],
    metrics: List[float],
    iteration: int,
    container: V1Container = None,
) -> V1Operation:
    container = container or get_default_tuner_container(["polyaxon", "tuner", "bo"])
    return get_tuner(
        name="bayesian-tuner",
        container=container,
        matrix=matrix,
        configs=configs,
        metrics=metrics,
        iteration=iteration,
    )


def get_hyperband_tuner(
    matrix: V1Hyperband,
    configs: List[Dict],
    metrics: List[float],
    iteration: int,
    container: V1Container = None,
) -> V1Operation:
    container = container or get_default_tuner_container(
        ["polyaxon", "tuner", "hyperband"]
    )
    return get_tuner(
        name="hyperband-tuner",
        container=container,
        matrix=matrix,
        configs=configs,
        metrics=metrics,
        iteration=iteration,
    )


def get_hyperopt_tuner(
    matrix: V1Hyperopt,
    configs: List[Dict],
    metrics: List[float],
    iteration: int,
    container: V1Container = None,
) -> V1Operation:
    container = container or get_default_tuner_container(
        ["polyaxon", "tuner", "hyperopt"]
    )
    return get_tuner(
        name="hyperopt-tuner",
        container=container,
        matrix=matrix,
        configs=configs,
        metrics=metrics,
        iteration=iteration,
    )
