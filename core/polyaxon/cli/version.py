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

from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon import pkg
from polyaxon.cli.errors import handle_cli_error
from polyaxon.client import PolyaxonClient
from polyaxon.deploy.operators.pip import PipOperator
from polyaxon.logger import clean_outputs, logger
from polyaxon.managers.auth import AuthConfigManager
from polyaxon.managers.cli import CliConfigManager
from polyaxon.utils import indentation
from polyaxon.utils.formatting import Printer, dict_tabulate

PROJECT_CLI_NAME = "polyaxon-cli"


def pip_upgrade(project_name=PROJECT_CLI_NAME):
    PipOperator.execute(["install", "--upgrade", project_name], stream=True)
    click.echo("polyaxon-cli upgraded.")


def session_expired():
    AuthConfigManager.purge()
    CliConfigManager.purge()
    click.echo("Session has expired, please try again.")
    sys.exit(1)


def get_version(package):
    import pkg_resources

    try:
        return pkg_resources.get_distribution(package).version
    except pkg_resources.DistributionNotFound:
        logger.error("`%s` is not installed", package)


def get_current_version():
    return pkg.VERSION


def get_server_versions(polyaxon_client=None):
    polyaxon_client = polyaxon_client or PolyaxonClient()
    try:
        return polyaxon_client.versions_v1.get_versions()
    except ApiException as e:
        if e.status == 403:
            session_expired()
            sys.exit(1)
        handle_cli_error(e, message="Could not get cli version.")
        sys.exit(1)
    except HTTPError:
        Printer.print_error("Could not connect to remote server.")
        sys.exit(1)


def get_log_handler(polyaxon_client=None):
    polyaxon_client = polyaxon_client or PolyaxonClient()
    try:
        return polyaxon_client.versions_v1.get_log_handler()
    except ApiException as e:
        if e.status == 403:
            session_expired()
            sys.exit(1)
        handle_cli_error(e, message="Could not get cli version.")
        sys.exit(1)
    except HTTPError:
        Printer.print_error("Could not connect to remote server.")
        sys.exit(1)


def check_cli_version(server_versions=None, current_version=None):
    """Check if the current cli version satisfies the server requirements"""
    if not CliConfigManager.should_check():
        return

    from distutils.version import LooseVersion  # pylint:disable=import-error

    server_versions = server_versions or get_server_versions()
    current_version = current_version or get_current_version()
    cli_config = CliConfigManager.reset(
        current_version=current_version, server_versions=server_versions.to_dict()
    )

    if LooseVersion(current_version) < LooseVersion(cli_config.min_version):
        click.echo(
            """Your version of CLI ({}) is no longer compatible with server.""".format(
                current_version
            )
        )
        if click.confirm(
            "Do you want to upgrade to "
            "version {} now?".format(cli_config.latest_version)
        ):
            pip_upgrade()
            sys.exit(0)
        else:
            indentation.puts("Your can manually run:")
            with indentation.indent(4):
                indentation.puts("pip install -U polyaxon-cli")
            indentation.puts(
                "to upgrade to the latest version `{}`".format(
                    cli_config.latest_version
                )
            )

            sys.exit(0)
    elif LooseVersion(current_version) < LooseVersion(cli_config.latest_version):
        indentation.puts(
            "New version of CLI ({}) is now available. To upgrade run:".format(
                cli_config.latest_version
            )
        )
        with indentation.indent(4):
            indentation.puts("pip install -U polyaxon-cli")
    elif LooseVersion(current_version) > LooseVersion(cli_config.latest_version):
        indentation.puts(
            "Your version of CLI ({}) is ahead of the latest version "
            "supported by Polyaxon Platform ({}) on your cluster, "
            "and might be incompatible.".format(
                current_version, cli_config.latest_version
            )
        )


@click.command()
@click.option("--check", is_flag=True, default=False, help="Check versions.")
@clean_outputs
def version(check):
    """Print the current version of the cli and platform."""
    server_versions = get_server_versions()
    current_version = get_current_version()
    Printer.print_header("Current cli version: {}.".format(current_version))
    Printer.print_header("Supported versions:")
    dict_tabulate(server_versions.to_dict())
    if check:
        check_cli_version(server_versions, current_version)


@click.command()
@clean_outputs
def upgrade():
    """Install/Upgrade polyaxon cli."""
    try:
        pip_upgrade(PROJECT_CLI_NAME)
    except Exception as e:
        logger.error(e)
