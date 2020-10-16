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

import sys

import click

from polyaxon import pkg
from polyaxon.cli.session import set_versions_config
from polyaxon.deploy.operators.pip import PipOperator
from polyaxon.logger import logger
from polyaxon.utils import indentation
from polyaxon.utils.formatting import Printer, dict_tabulate
from polyaxon.utils.versions import clean_version_for_check

PROJECT_CLI_NAME = "polyaxon-cli"


def pip_upgrade(project_name=PROJECT_CLI_NAME):
    PipOperator.execute(["install", "--upgrade", project_name], stream=True)
    click.echo("polyaxon-cli upgraded.")


def get_version(package):
    import pkg_resources

    try:
        return pkg_resources.get_distribution(package).version
    except pkg_resources.DistributionNotFound:
        logger.error("`%s` is not installed", package)


def get_current_version():
    return pkg.VERSION


def check_cli_version(config, is_cli: bool = True):
    """Check if the current cli version satisfies the server requirements"""
    from distutils.version import LooseVersion  # pylint:disable=import-error

    min_version = clean_version_for_check(config.min_version)
    latest_version = clean_version_for_check(config.latest_version)
    current_version = clean_version_for_check(config.current_version)
    if not min_version or not latest_version or not current_version:
        if is_cli:
            Printer.print_error(
                "Could not get the min/latest versions from compatibility API.",
                sys_exit=True,
            )
        else:
            return
    if LooseVersion(current_version) < LooseVersion(min_version):
        click.echo(
            """Your version of CLI ({}) is no longer compatible with server.""".format(
                config.current_version
            )
        )
        if click.confirm(
            "Do you want to upgrade to " "version {} now?".format(config.latest_version)
        ):
            pip_upgrade()
            sys.exit(0)
        else:
            indentation.puts("Your can manually run:")
            with indentation.indent(4):
                indentation.puts("pip install -U polyaxon")
            indentation.puts(
                "to upgrade to the latest version `{}`".format(config.latest_version)
            )

            sys.exit(0)
    elif LooseVersion(current_version) < LooseVersion(latest_version):
        indentation.puts(
            "New version of CLI ({}) is now available. To upgrade run:".format(
                config.latest_version
            )
        )
        with indentation.indent(4):
            indentation.puts("pip install -U polyaxon")
    elif LooseVersion(current_version) > LooseVersion(latest_version):
        indentation.puts(
            "Your version of CLI ({}) is ahead of the latest version "
            "supported by Polyaxon Platform ({}) on your cluster, "
            "and might be incompatible.".format(
                config.current_version, config.latest_version
            )
        )


@click.command()
@click.option(
    "--check", is_flag=True, default=False, help="Check compatibility versions."
)
def version(check):
    """Print the current version of the cli and platform."""
    Printer.print_header("Current cli version: {}.".format(pkg.VERSION))
    if check:
        config = set_versions_config()
        Printer.print_header("Platform:")
        dict_tabulate(config.installation)
        Printer.print_header("compatibility versions:")
        dict_tabulate(config.compatibility)
        check_cli_version(config)


@click.command()
def upgrade():
    """Install/Upgrade polyaxon cli."""
    try:
        pip_upgrade(PROJECT_CLI_NAME)
    except Exception as e:
        logger.error(e)
