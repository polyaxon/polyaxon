# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from distutils.version import LooseVersion

import clint
import pip
import pkg_resources
import click
import sys

from polyaxon_client.exceptions import (
    PolyaxonHTTPError,
    PolyaxonShouldExitError,
    AuthorizationError
)

from polyaxon_cli.logger import logger
from polyaxon_cli.managers.auth import AuthConfigManager
from polyaxon_cli.managers.cli import CliConfigManager
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import Printer, dict_tabulate

PROJECT_CLI_NAME = "polyaxon-cli"
PROJECT_LIB_NAME = "polyaxon-lib"


def pip_upgrade(project_name=PROJECT_CLI_NAME):
    pip.main(["install", "--upgrade", project_name])


def session_expired():
    AuthConfigManager.purge()
    click.echo('Session has expired, please try again.')
    sys.exit(1)


def get_version(pkg):
    try:
        version = pkg_resources.get_distribution(pkg).version
        return version
    except pkg_resources.DistributionNotFound:
        logger.error('`{}` is not installed'.format(pkg))


def check_cli_version():
    """Check if the current cli version satisfies the server requirements"""
    if not CliConfigManager.should_check():
        return
    try:
        server_version = PolyaxonClients().version.get_cli_version()
    except AuthorizationError:
        session_expired()
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get cli version.')
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    current_version = pkg_resources.get_distribution(PROJECT_CLI_NAME).version
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
@click.option('--lib', is_flag=True, default=False, help='Version of the Polyaxon cli.')
def version(cli, platform, lib):
    """Print the current version of the cli, platform, and lib."""

    version_client = PolyaxonClients().version
    cli = cli or not any([cli, platform, lib])
    if cli:
        try:
            server_version = version_client.get_cli_version()
        except AuthorizationError:
            session_expired()
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not get cli version.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        version = get_version(PROJECT_CLI_NAME)
        Printer.print_header('Current cli version: {}.'.format(version))
        Printer.print_header('Supported cli versions:')
        dict_tabulate(server_version.to_dict())

    if lib:
        try:
            server_version = version_client.get_lib_version()
        except AuthorizationError:
            session_expired()
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not get lib version.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        version = get_version(PROJECT_LIB_NAME)
        Printer.print_header('Current lib version: {}.'.format(version))
        Printer.print_header('Supported lib versions:')
        dict_tabulate(server_version.to_dict())

    if platform:
        try:
            platform_version = version_client.get_platform_version()
        except AuthorizationError:
            session_expired()
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not get platform version.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        chart_version = version_client.get_chart_version()
        Printer.print_header('Current platform version: {}.'.format(chart_version.version))
        Printer.print_header('Supported platform versions:')
        dict_tabulate(platform_version.to_dict())


@click.command()
@click.option('--lib', '-a', is_flag=True, default=False,
              help='Upgrade the project, if True upgrade the cli '
                   'otherwise upgrade the polyaxon library.')
def upgrade(lib):
    """Install/Upgrade polyxon-cli or polyaxon-lib."""
    try:
        project_name = PROJECT_LIB_NAME if lib else PROJECT_CLI_NAME
        pip_upgrade(project_name)
    except Exception as e:
        logger.error(e)
