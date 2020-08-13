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

import click

from polyaxon.utils.formatting import Printer


@click.group()
def tuner():
    pass


def log_suggestions(suggestions: List[Dict]):
    from polyaxon import settings
    from polyaxon.client import RunClient
    from polyaxon.env_vars.getters import get_run_info
    from polyaxon.exceptions import PolyaxonClientException, PolyaxonContainerException

    if not settings.CLIENT_CONFIG.no_api:
        try:
            owner, project, run_uuid = get_run_info()
        except PolyaxonClientException as e:
            raise PolyaxonContainerException(e)

        RunClient(owner=owner, project=project, run_uuid=run_uuid).log_outputs(
            suggestions=suggestions
        )


@tuner.command()
@click.option(
    "--matrix",
    help="A string representing the matrix configuration for bayesian optimzation.",
)
@click.option(
    "--configs",
    help="A string representing the list of dict representing the configs to use for tuning.",
)
@click.option(
    "--metrics", help="A string representing the list metrics to use for tuning."
)
def bayesian(matrix, configs, metrics):
    """Create suggestions based on bayesian optimization."""
    from polyaxon.polyflow import V1Bayes
    from polyaxon.polytune.search_managers.bayesian_optimization.manager import (
        BayesSearchManager,
    )

    matrix = V1Bayes.read(matrix)

    suggestions = BayesSearchManager(config=matrix).get_suggestions(
        configs=configs, metrics=metrics
    )
    log_suggestions(suggestions)

    Printer.print_success("Suggestions generated with bayesian optimization")


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
    from polyaxon.polytune.search_managers.hyperband.manager import HyperbandManager

    matrix = V1Hyperband.read(matrix)

    suggestions = HyperbandManager(config=matrix).get_suggestions(
        configs=configs,
        metrics=metrics,
        bracket_iteration=bracket_iteration,
        iteration=iteration,
    )
    log_suggestions(suggestions)

    Printer.print_success("Suggestions generated with hyperband")


@tuner.command()
@click.option(
    "--matrix", help="A string representing the matrix configuration for hyperopt."
)
@click.option(
    "--configs",
    help="A string representing the list of dict representing the configs to use for tuning.",
)
@click.option(
    "--metrics", help="A string representing the list metrics to use for tuning."
)
def hyperopt(matrix, configs, metrics):
    """Create suggestions based on hyperopt."""
    from polyaxon.polyflow import V1Hyperopt
    from polyaxon.polytune.search_managers.hyperopt.manager import HyperoptManager

    matrix = V1Hyperopt.read(matrix)

    suggestions = HyperoptManager(config=matrix).get_suggestions(
        configs=configs, metrics=metrics
    )
    log_suggestions(suggestions)

    Printer.print_success("Suggestions generated with hyperopt")
