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

import os
import sys

import click

from polyaxon.cli.errors import handle_cli_error
from polyaxon.logger import clean_outputs
from polyaxon.managers.deploy import DeployManager
from polyaxon.utils.formatting import Printer
from polyaxon.utils.list_utils import to_list


def read_deployment_config(filepaths):
    from polyaxon.deploy import reader

    if not filepaths:
        return None

    filepaths = to_list(filepaths)
    for filepath in filepaths:
        if not os.path.isfile(filepath):
            Printer.print_error("`{}` must be a valid file".format(filepath))
            sys.exit(1)
    try:
        deployment_config = reader.read(filepaths)
    except Exception as e:
        handle_cli_error(e, message="Polyaxon deployment file is not valid.")
        sys.exit(1)

    return deployment_config


@click.group()
@clean_outputs
def admin():
    """Commands for admin management."""


@admin.command()
@click.option(
    "-f",
    "--file",
    "config_file",
    type=click.Path(exists=True),
    help="The polyaxon deployment config file(s) to check.",
)
@click.option(
    "--manager-path",
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
    "--dry_run",
    "--dry-run",
    is_flag=True,
    default=False,
    help="Dry run the configuration and generate a debuggable output.",
)
@clean_outputs
def deploy(config_file, manager_path, check, dry_run):
    """Deploy polyaxon."""
    config = read_deployment_config(config_file)
    manager = DeployManager(
        config=config, filepath=config_file, manager_path=manager_path, dry_run=dry_run
    )
    exception = None
    Printer.print_success(
        "Polyaxon `{}` deployment file is valid.".format(config.deployment_chart)
    )
    if check:
        try:
            manager.check()
        except Exception as e:
            handle_cli_error(e, message="Polyaxon deployment manager error.")
            sys.exit(1)

    else:
        try:
            manager.install()
        except Exception as e:
            Printer.print_error("Polyaxon could not be installed.")
            exception = e

    if exception:
        Printer.print_error("Error message: {}.".format(exception))


@admin.command()
@click.option(
    "-f",
    "--file",
    "config_file",
    type=click.Path(exists=True),
    help="The polyaxon deployment config file(s) to check.",
)
@click.option(
    "--manager-path",
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
    "--dry_run",
    "--dry-run",
    is_flag=True,
    default=False,
    help="Dry run the configuration and generate a debuggable output.",
)
@clean_outputs
def upgrade(config_file, manager_path, check, dry_run):
    """Upgrade a Polyaxon deployment."""
    config = read_deployment_config(config_file)
    manager = DeployManager(
        config=config, filepath=config_file, manager_path=manager_path, dry_run=dry_run
    )
    exception = None
    Printer.print_success(
        "Polyaxon `{}` deployment file is valid.".format(config.deployment_chart)
    )
    if check:
        try:
            manager.check()
        except Exception as e:
            handle_cli_error(e, message="Polyaxon deployment manager error.")
            sys.exit(1)
    else:
        try:
            manager.upgrade()
        except Exception as e:
            Printer.print_error("Polyaxon could not upgrade the deployment.")
            exception = e

    if exception:
        Printer.print_error("Error message: {}.".format(exception))


@admin.command()
@click.option(
    "-f",
    "--file",
    "config_file",
    type=click.Path(exists=True),
    help="The polyaxon deployment config file(s) to check.",
)
@clean_outputs
def teardown(config_file):
    """Teardown a polyaxon deployment given a config file."""
    config = read_deployment_config(config_file)
    manager = DeployManager(config=config, filepath=config_file)
    exception = None
    try:
        if click.confirm("Would you like to execute pre-delete hooks?", default=True):
            manager.teardown(hooks=True)
        else:
            manager.teardown(hooks=False)
    except Exception as e:
        Printer.print_error("Polyaxon could not teardown the deployment.")
        exception = e

    if exception:
        Printer.print_error("Error message: {}.".format(exception))
