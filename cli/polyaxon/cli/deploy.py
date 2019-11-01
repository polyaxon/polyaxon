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

import click

from polyaxon.logger import clean_outputs
from polyaxon.utils.formatting import Printer


@click.command()
@click.option(
    "--file",
    "-f",
    type=click.Path(exists=True),
    help="The polyaxon deployment config file(s) to check.",
)
@click.option(
    "--manager_path",
    type=click.Path(exists=True),
    help="The path of the deployment manager, e.g. local chart.",
)
@click.option(
    "--check",
    is_flag=True,
    default=False,
    help="Check if deployment file and other requirements are met.",
)
@click.option(
    "--upgrade", is_flag=True, default=False, help="Upgrade a Polyaxon deployment."
)
@clean_outputs
def deploy(file, manager_path, check, upgrade):  # pylint:disable=redefined-builtin
    if upgrade:
        Printer.print_warning(
            "The command `polyaxon deploy [-f] --upgrade` is deprecated, "
            "please use `polyaxon admin upgrade [-f]`."
        )
    elif check:
        Printer.print_warning(
            "The command `polyaxon deploy [-f] --check` is deprecated, "
            "please use `polyaxon admin deploy [-f] --check`."
        )
    else:
        Printer.print_warning(
            "The command `polyaxon deploy [-f]` is deprecated, "
            "please use `polyaxon admin deploy [-f]`."
        )


@click.command()
@click.option(
    "--file",
    "-f",
    type=click.Path(exists=True),
    help="The polyaxon deployment config file(s) to check.",
)
@clean_outputs
def teardown(file):  # pylint:disable=redefined-builtin
    Printer.print_warning(
        "The command `polyaxon teardown [-f]` is deprecated, "
        "please use `polyaxon admin teardown [-f]`."
    )
