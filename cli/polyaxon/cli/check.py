#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

import os
import sys

from collections import OrderedDict

import click

from hestia.list_utils import to_list

from polyaxon.logger import clean_outputs
from polyaxon.polyaxonfile import PolyaxonFile
from polyaxon.run.params import parse_params
from polyaxon.utils import constants
from polyaxon.utils.formatting import Printer, dict_tabulate


def check_polyaxonfile(
    file, params=None, profile=None, log=True  # pylint:disable=redefined-builtin
):
    file = to_list(file)
    exists = [os.path.isfile(f) for f in file]

    parsed_params = None
    if params:
        parsed_params = parse_params(params)

    if not any(exists):
        Printer.print_error(
            "Polyaxonfile is not present, "
            "please run {}".format(constants.INIT_COMMAND)
        )
        sys.exit(1)

    try:
        plx_file = PolyaxonFile(file)
        plx_file = plx_file.get_op_specification(params=parsed_params, profile=profile)
        if log:
            Printer.print_success("Polyaxonfile valid")
        return plx_file
    except Exception as e:
        Printer.print_error("Polyaxonfile is not valid.")
        Printer.print_error("Error message `{}`.".format(e))
        sys.exit(1)


def check_polyaxonfile_kind(specification, kind):
    if specification.kind != kind:
        Printer.print_error(
            "Your polyaxonfile must be of kind: `{}`, "
            "received: `{}`.".format(kind, specification.kind)
        )
        sys.exit(-1)


def get_group_experiments_info(
    search_algorithm, concurrency, early_stopping=False, **kwargs
):
    info = OrderedDict()
    info["Search algorithm"] = search_algorithm.lower()
    info["Concurrency"] = (
        "{} runs".format("sequential")
        if concurrency == 1
        else "{} concurrent runs".format(concurrency)
    )
    info["Early stopping"] = "activated" if early_stopping else "deactivated"
    if "n_experiments" in kwargs:
        info["Experiments to create"] = kwargs["n_experiments"]

    dict_tabulate(info)


@click.command()
@click.option(
    "--file",
    "-f",
    multiple=True,
    type=click.Path(exists=True),
    help="The polyaxon file to check.",
)
@click.option(
    "--version",
    "-v",
    is_flag=True,
    default=False,
    help="Checks and prints the version.",
)
@click.option(
    "--definition",
    "-def",
    is_flag=True,
    default=False,
    help="Checks and prints the file definition.",
)
@click.option(
    "--params",
    "-P",
    metavar="NAME=VALUE",
    multiple=True,
    help="A parameter to override the default params of the run, form -P name=value.",
)
@clean_outputs
def check(file, version, definition, params):  # pylint:disable=redefined-builtin
    """Check a polyaxonfile."""
    file = file or "polyaxonfile.yaml"
    specification = check_polyaxonfile(file, params=params).specification

    if version:
        Printer.decorate_format_value(
            "The version is: {}", specification.version, "yellow"
        )

    if definition:
        job_condition = (
            specification.is_job
            or specification.is_build
            or specification.is_notebook
            or specification.is_tensorboard
        )
        if specification.is_experiment:
            Printer.decorate_format_value(
                "This polyaxon specification has {}", "One experiment", "yellow"
            )
        if job_condition:
            Printer.decorate_format_value(
                "This {} polyaxon specification is valid", specification.kind, "yellow"
            )
        if specification.is_group:
            experiments_def = specification.experiments_def
            click.echo(
                "This polyaxon specification has experiment group with the following definition:"
            )
            get_group_experiments_info(**experiments_def)

    return specification
