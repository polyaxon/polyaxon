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

import click

from polyaxon.logger import logger


@click.group()
def tuner():
    pass


@tuner.command()
@click.option(
    "--matrix",
    help="A string representing the matrix configuration for bayesian optimzation.",
)
@click.option("--iteration", type=int, help="The current iteration.")
@click.option(
    "--configs",
    help="A string representing the list of dict representing the configs to use for tuning.",
)
@click.option(
    "--metrics", help="A string representing the list metrics to use for tuning."
)
def bayes(matrix, iteration, configs, metrics):
    """Create suggestions based on bayesian optimization."""
    from polyaxon.polyflow import V1Bayes
    from polyaxon.polytune.iteration_lineage import handle_iteration
    from polyaxon.polytune.search_managers.bayesian_optimization.manager import (
        BayesSearchManager,
    )

    retry = 1
    error = None
    suggestions = None
    while retry < 3:
        try:
            suggestions = BayesSearchManager(config=V1Bayes.read(matrix)).get_suggestions(
                configs=configs, metrics=metrics
            )
            error = None
            break
        except Exception as e:
            retry += 1
            error = "Polyaxon tuner failed creating suggestions retrying, error %s" % e
            logger.warning(error)

    handle_iteration(iteration=iteration, suggestions=suggestions, error=error)


@tuner.command()
@click.option(
    "--matrix", help="A string representing the matrix configuration for hyperband."
)
@click.option("--iteration", type=int, help="The current hyperband iteration.")
@click.option(
    "--bracket-iteration", type=int, help="The current hyperband bracket iteration."
)
@click.option(
    "--configs",
    help="A string representing the list of dict representing the configs to use for tuning.",
)
@click.option(
    "--metrics", help="A string representing the list metrics to use for tuning."
)
def hyperband(matrix, iteration, bracket_iteration, configs, metrics):
    """Create suggestions based on hyperband."""
    from polyaxon.polyflow import V1Hyperband
    from polyaxon.polytune.iteration_lineage import handle_iteration
    from polyaxon.polytune.search_managers.hyperband.manager import HyperbandManager

    retry = 1
    error = None
    suggestions = None
    while retry < 3:
        try:
            suggestions = HyperbandManager(config=V1Hyperband.read(matrix)).get_suggestions(
                configs=configs,
                metrics=metrics,
                bracket_iteration=bracket_iteration,
                iteration=iteration,
            )
            error = None
            break
        except Exception as e:
            retry += 1
            error = "Polyaxon tuner failed creating suggestions retrying, error %s" % e
            logger.warning(error)

    handle_iteration(iteration=iteration, suggestions=suggestions, error=error)


@tuner.command()
@click.option(
    "--matrix", help="A string representing the matrix configuration for hyperopt."
)
@click.option("--iteration", type=int, help="The current iteration.")
@click.option(
    "--configs",
    help="A string representing the list of dict representing the configs to use for tuning.",
)
@click.option(
    "--metrics", help="A string representing the list metrics to use for tuning."
)
def hyperopt(matrix, iteration, configs, metrics):
    """Create suggestions based on hyperopt."""
    from polyaxon.polyflow import V1Hyperopt
    from polyaxon.polytune.iteration_lineage import handle_iteration
    from polyaxon.polytune.search_managers.hyperopt.manager import HyperoptManager

    retry = 1
    error = None
    suggestions = None
    while retry < 3:
        try:
            suggestions = HyperoptManager(config=V1Hyperopt.read(matrix)).get_suggestions(
                configs=configs, metrics=metrics
            )
            error = None
            break
        except Exception as e:
            retry += 1
            error = "Polyaxon tuner failed creating suggestions retrying, error %s" % e
            logger.warning(error)

    handle_iteration(iteration=iteration, suggestions=suggestions, error=error)
