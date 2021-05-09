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

import sys

import click

from polyaxon import pkg
from polyaxon.cli.session import set_versions_config
from polyaxon.deploy.operators.pip import PipOperator
from polyaxon.logger import clean_outputs, logger
from polyaxon.utils import indentation
from polyaxon.utils.formatting import Printer, dict_tabulate, dict_to_tabulate
from polyaxon.utils.versions import clean_version_for_check

PROJECT_CLI_NAME = "polyaxon"


def pip_upgrade(project_name=PROJECT_CLI_NAME):
    PipOperator.execute(["install", "--upgrade", project_name], stream=True)
    click.echo("polyaxon upgraded.")


def get_version(package: str, show_error: bool = True):
    import pkg_resources

    try:
        return pkg_resources.get_distribution(package).version
    except pkg_resources.DistributionNotFound:
        if show_error:
            logger.error("`%s` is not installed", package)


def check_old_packages():
    pkg = "polyaxon-cli"
    if get_version(package=pkg, show_error=False):
        Printer.print_error(
            "Legacy package `{pkg}` is installed. Please run `pip uninstall {pkg}`".format(
                pkg=pkg
            ),
            sys_exit=True,
        )


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
            "Your version of Polyaxon CLI ({}) is no longer supported.".format(
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
            "New version of Polyaxon CLI ({}) is now available. To upgrade run:".format(
                config.latest_version
            )
        )
        with indentation.indent(4):
            indentation.puts("pip install -U polyaxon")
    elif LooseVersion(current_version) > LooseVersion(latest_version):
        indentation.puts(
            "Your version of CLI ({}) is ahead of the latest version "
            "supported by Polyaxon server ({}) on your cluster, "
            "and might be incompatible.".format(
                config.current_version, config.latest_version
            )
        )


@click.command()
@click.option(
    "--check", is_flag=True, default=False, help="Check compatibility versions."
)
@clean_outputs
def version(check):
    """Print the current version of the cli and platform."""
    check_old_packages()
    Printer.print_header("Current cli version: {}.".format(pkg.VERSION))
    if check:
        config = set_versions_config()
        Printer.print_header("Platform:")
        config_installation = dict_to_tabulate(
            config.installation,
            humanize_values=True,
            exclude_attrs=["hmac", "auth", "host"],
        )
        dict_tabulate(config_installation)
        Printer.print_header("Compatibility versions:")
        dict_tabulate(config.compatibility)
        check_cli_version(config)


@click.command()
@clean_outputs
def upgrade():
    """Install/Upgrade polyaxon cli."""
    try:
        pip_upgrade(PROJECT_CLI_NAME)
    except Exception as e:
        logger.error(e)
