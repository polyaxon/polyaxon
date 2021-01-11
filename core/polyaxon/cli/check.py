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

from polyaxon.logger import clean_outputs
from polyaxon.polyaxonfile.check import check_polyaxonfile
from polyaxon.utils.formatting import Printer


@click.command()
@click.option(
    "-f",
    "--file",
    "polyaxonfile",
    multiple=True,
    type=click.Path(exists=True),
    help="The polyaxon file to check.",
)
@click.option(
    "-pm",
    "--python-module",
    type=str,
    help="The python module to run.",
)
@click.option(
    "--version",
    "-v",
    is_flag=True,
    default=False,
    help="Checks and prints the version.",
)
@click.option(
    "--params",
    "-P",
    metavar="NAME=VALUE",
    multiple=True,
    help="A parameter to override the default params of the run, form -P name=value.",
)
@click.option(
    "--lint",
    "-l",
    is_flag=True,
    default=False,
    help="To check the specification only without params validation.",
)
@clean_outputs
def check(polyaxonfile, python_module, version, params, lint):
    """Check a polyaxonfile."""
    specification = check_polyaxonfile(
        polyaxonfile=polyaxonfile,
        python_module=python_module,
        params=params,
        validate_params=not lint,
    )

    if version:
        Printer.decorate_format_value(
            "The version is: {}", specification.version, "yellow"
        )
    return specification
