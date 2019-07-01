# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_deploy.operators.pip import PipOperator

from polyaxon_cli import pkg
from polyaxon_cli.client import PolyaxonClient
from polyaxon_cli.client.exceptions import (
    AuthorizationError,
    PolyaxonHTTPError,
    PolyaxonShouldExitError
)
from polyaxon_cli.logger import clean_outputs, logger
from polyaxon_cli.managers.auth import AuthConfigManager
from polyaxon_cli.managers.cli import CliConfigManager
from polyaxon_cli.utils import indentation
from polyaxon_cli.utils.formatting import Printer, dict_tabulate
from polyaxon_client.exceptions import PolyaxonClientException

PROJECT_CLI_NAME = "polyaxon-cli"


def pip_upgrade(project_name=PROJECT_CLI_NAME):
    PipOperator.execute(['install', '--upgrade', project_name], stream=True)
    click.echo('polyaxon-cli upgraded.')


def session_expired():
    AuthConfigManager.purge()
    CliConfigManager.purge()
    click.echo('Session has expired, please try again.')
    sys.exit(1)


def get_version(package):
    import pkg_resources

    try:
        return pkg_resources.get_distribution(package).version
    except pkg_resources.DistributionNotFound:
        logger.error('`%s` is not installed', package)


def get_current_version():
    return pkg.VERSION


def get_server_version():
    try:
        return PolyaxonClient().version.get_cli_version()
    except AuthorizationError:
        session_expired()
        sys.exit(1)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get cli version.')
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


def get_log_handler():
    try:
        return PolyaxonClient().version.get_log_handler()
    except AuthorizationError:
        session_expired()
        sys.exit(1)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get cli version.')
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


def check_cli_version():
    """Check if the current cli version satisfies the server requirements"""
    if not CliConfigManager.should_check():
        return

    from distutils.version import LooseVersion  # pylint:disable=import-error

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
            indentation.puts("Your can manually run:")
            with indentation.indent(4):
                indentation.puts("pip install -U polyaxon-cli")
            indentation.puts(
                "to upgrade to the latest version `{}`".format(server_version.latest_version))

            sys.exit(0)
    elif LooseVersion(current_version) < LooseVersion(server_version.latest_version):
        indentation.puts("New version of CLI ({}) is now available. To upgrade run:".format(
            server_version.latest_version
        ))
        with indentation.indent(4):
            indentation.puts("pip install -U polyaxon-cli")
    elif LooseVersion(current_version) > LooseVersion(server_version.latest_version):
        indentation.puts("You version of CLI ({}) is ahead of the latest version "
                         "supported by Polyaxon Platform ({}) on your cluster, "
                         "and might be incompatible.".format(current_version,
                                                             server_version.latest_version))


@click.command()
@click.option('--cli', is_flag=True, default=False, help='Version of the Polyaxon cli.')
@click.option('--platform', is_flag=True, default=False, help='Version of the Polyaxon platform.')
@clean_outputs
def version(cli, platform):
    """Print the current version of the cli and platform."""
    version_client = PolyaxonClient().version
    cli = cli or not any([cli, platform])
    if cli:
        try:
            server_version = version_client.get_cli_version()
        except AuthorizationError:
            session_expired()
            sys.exit(1)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get cli version.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        cli_version = get_current_version()
        Printer.print_header('Current cli version: {}.'.format(cli_version))
        Printer.print_header('Supported cli versions:')
        dict_tabulate(server_version.to_dict())

    if platform:
        try:
            platform_version = version_client.get_platform_version()
        except AuthorizationError:
            session_expired()
            sys.exit(1)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
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
