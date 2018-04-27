# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from distutils.version import LooseVersion  # pylint:disable=import-error

import click
import clint
import pip
import pkg_resources

from polyaxon_cli.logger import clean_outputs, logger
from polyaxon_cli.managers.auth import AuthConfigManager
from polyaxon_cli.managers.cli import CliConfigManager
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import Printer, dict_tabulate
from polyaxon_client.exceptions import (
    AuthorizationError,
    PolyaxonHTTPError,
    PolyaxonShouldExitError
)

PROJECT_CLI_NAME = "polyaxon-cli"


def pip_upgrade(project_name=PROJECT_CLI_NAME):
    pip.main(["install", "--upgrade", project_name])


def session_expired():
    AuthConfigManager.purge()
    CliConfigManager.purge()
    click.echo('Session has expired, please try again.')
    sys.exit(1)


def get_version(pkg):
    try:
        return pkg_resources.get_distribution(pkg).version
    except pkg_resources.DistributionNotFound:
        logger.error('`%s` is not installed', pkg)


def get_current_version():
    return pkg_resources.get_distribution(PROJECT_CLI_NAME).version


def get_server_version():
    try:
        return PolyaxonClients().version.get_cli_version()
    except AuthorizationError:
        session_expired()
        sys.exit(1)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get cli version.')
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


def get_log_handler():
    try:
        return PolyaxonClients().version.get_log_handler()
    except AuthorizationError:
        session_expired()
        sys.exit(1)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get cli version.')
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


def check_cli_version():
    """Check if the current cli version satisfies the server requirements"""
    if not CliConfigManager.should_check():
        return

    server_version = get_server_version()
    current_version = get_current_version()
    CliConfigManager.reset(current_version=current_version,
                           min_version=server_version.min_version)

    if LooseVersion(current_version) < LooseVersion(server_version.min_version):
        click.echo("""Your version of CLI ({}) is no longer compatible with server.""".format(
            current_version))
        if click.confirm("Do you want to upgrade to "
                         "version {} now?".format(server_version.latest_version)):
            pip_upgrade()
            sys.exit(0)
        else:
            clint.textui.puts("Your can manually run:")
            with clint.textui.indent(4):
                clint.textui.puts("pip install -U polyaxon-cli")
            clint.textui.puts(
                "to upgrade to the latest version `{}`".format(server_version.latest_version))

            sys.exit(0)
    elif LooseVersion(current_version) < LooseVersion(server_version.latest_version):
        clint.textui.puts("New version of CLI ({}) is now available. To upgrade run:".format(
            server_version.latest_version
        ))
        with clint.textui.indent(4):
            clint.textui.puts("pip install -U polyaxon-cli")


@click.command()
@click.option('--cli', is_flag=True, default=False, help='Version of the Polyaxon cli.')
@click.option('--platform', is_flag=True, default=False, help='Version of the Polyaxon cli.')
@clean_outputs
def version(cli, platform):
    """Print the current version of the cli and platform."""
    version_client = PolyaxonClients().version
    cli = cli or not any([cli, platform])
    if cli:
        try:
            server_version = version_client.get_cli_version()
        except AuthorizationError:
            session_expired()
            sys.exit(1)
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not get cli version.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        cli_version = get_version(PROJECT_CLI_NAME)
        Printer.print_header('Current cli version: {}.'.format(cli_version))
        Printer.print_header('Supported cli versions:')
        dict_tabulate(server_version.to_dict())

    if platform:
        try:
            platform_version = version_client.get_platform_version()
        except AuthorizationError:
            session_expired()
            sys.exit(1)
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not get platform version.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        chart_version = version_client.get_chart_version()
        Printer.print_header('Current platform version: {}.'.format(chart_version.version))
        Printer.print_header('Supported platform versions:')
        dict_tabulate(platform_version.to_dict())


@click.command()
@clean_outputs
def upgrade():
    """Install/Upgrade polyaxon-cli."""
    try:
        pip_upgrade(PROJECT_CLI_NAME)
    except Exception as e:
        logger.error(e)
