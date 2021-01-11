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

import click

from polyaxon.logger import logger


@click.group()
def tuner():
    pass


@tuner.command()
@click.option(
    "--matrix",
    help="A string representing the matrix configuration for bayesian optimization.",
)
@click.option(
    "--join", help="A string representing the join to fetch configs and metrics."
)
@click.option("--iteration", type=int, help="The current iteration.")
def bayes(matrix, join, iteration):
    """Create suggestions based on bayesian optimization."""
    from polyaxon.client import RunClient
    from polyaxon.polyflow import V1Bayes, V1Join
    from polyaxon.polytune.iteration_lineage import (
        get_iteration_definition,
        handle_iteration,
        handle_iteration_failure,
    )
    from polyaxon.polytune.search_managers.bayesian_optimization.manager import (
        BayesSearchManager,
    )

    matrix = V1Bayes.read(matrix)
    join = V1Join.read(join)
    client = RunClient()
    values = get_iteration_definition(
        client=client,
        iteration=iteration,
        join=join,
        optimization_metric=matrix.metric.name,
    )
    if not values:
        return
    run_uuids, configs, metrics = values

    retry = 1
    exp = None
    suggestions = None
    while retry < 3:
        try:
            suggestions = BayesSearchManager(
                config=matrix,
            ).get_suggestions(configs=configs, metrics=metrics)
            exp = None
            break
        except Exception as exp:
            retry += 1
            logger.warning(exp)

    if exp:
        handle_iteration_failure(client=client, exp=exp)
        return

    handle_iteration(
        client=client,
        iteration=iteration,
        suggestions=suggestions,
    )


@tuner.command()
@click.option(
    "--matrix", help="A string representing the matrix configuration for hyperband."
)
@click.option(
    "--join", help="A string representing the join to fetch configs and metrics."
)
@click.option("--iteration", type=int, help="The current hyperband iteration.")
@click.option(
    "--bracket-iteration", type=int, help="The current hyperband bracket iteration."
)
def hyperband(matrix, join, iteration, bracket_iteration):
    """Create suggestions based on hyperband."""
    from polyaxon.client import RunClient
    from polyaxon.polyflow import V1Hyperband, V1Join
    from polyaxon.polytune.iteration_lineage import (
        get_iteration_definition,
        handle_iteration,
        handle_iteration_failure,
    )
    from polyaxon.polytune.search_managers.hyperband.manager import HyperbandManager

    matrix = V1Hyperband.read(matrix)
    matrix.set_tuning_params()
    join = V1Join.read(join)
    client = RunClient()
    values = get_iteration_definition(
        client=client,
        iteration=iteration,
        join=join,
        optimization_metric=matrix.metric.name,
        name="in-iteration-{}-{}".format(iteration, bracket_iteration),
    )
    if not values:
        return
    run_uuids, configs, metrics = values

    retry = 1
    exp = None
    suggestions = None
    while retry < 3:
        try:
            suggestions = HyperbandManager(config=matrix).get_suggestions(
                configs=configs,
                metrics=metrics,
                bracket_iteration=bracket_iteration,
                iteration=iteration,
            )
            exp = None
            break
        except Exception as exp:
            retry += 1
            logger.warning(exp)

    if exp:
        handle_iteration_failure(client=client, exp=exp)
        return

    handle_iteration(
        client=client,
        iteration=iteration,
        suggestions=suggestions,
        summary={"bracket_iteration": bracket_iteration},
        name="out-iteration-{}-{}".format(iteration, bracket_iteration),
    )


@tuner.command()
@click.option(
    "--matrix", help="A string representing the matrix configuration for hyperopt."
)
@click.option(
    "--join", help="A string representing the join to fetch configs and metrics."
)
@click.option("--iteration", type=int, help="The current iteration.")
def hyperopt(matrix, join, iteration):
    """Create suggestions based on hyperopt."""
    from polyaxon.client import RunClient
    from polyaxon.polyflow import V1Hyperopt, V1Join
    from polyaxon.polytune.iteration_lineage import (
        get_iteration_definition,
        handle_iteration,
        handle_iteration_failure,
    )
    from polyaxon.polytune.search_managers.hyperopt.manager import HyperoptManager

    matrix = V1Hyperopt.read(matrix)
    join = V1Join.read(join)
    client = RunClient()
    values = get_iteration_definition(
        client=client,
        iteration=iteration,
        join=join,
        optimization_metric=matrix.metric.name,
    )
    if not values:
        return
    run_uuids, configs, metrics = values

    retry = 1
    exp = None
    suggestions = None
    while retry < 3:
        try:
            suggestions = HyperoptManager(config=matrix).get_suggestions(
                configs=configs, metrics=metrics
            )
            exp = None
            break
        except Exception as exp:
            retry += 1
            logger.warning(exp)

    if exp:
        handle_iteration_failure(client=client, exp=exp)
        return

    handle_iteration(
        client=client,
        iteration=iteration,
        suggestions=suggestions,
    )
