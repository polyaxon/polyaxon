# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from distutils.version import LooseVersion

import clint
import pip
import pkg_resources
import click
import sys

from polyaxon_client.exceptions import PolyaxonShouldExitError
from polyaxon_schemas.polyaxonfile.logger import logger

from polyaxon_cli.utils.clients import PolyaxonClients

PROJECT_CLI_NAME = "polyaxon-cli"
PROJECT_LIB_NAME = "polyaxon-lib"


def pip_upgrade(project_name=PROJECT_CLI_NAME):
    pip.main(["install", "--upgrade", project_name])


def get_version(pkg):
    try:
        version = pkg_resources.get_distribution(pkg).version
        return version
    except pkg_resources.DistributionNotFound:
        logger.error('`{}` is not installed'.format(pkg))


def check_cli_version():
    """Check if the current cli version satisfies the server requirements"""
    try:
        server_version = PolyaxonClients().version.get_cli_version()
    except PolyaxonShouldExitError as e:
        logger.info(e)
        sys.exit(0)

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
    """Prints the current version of the CLI."""
    version_client = PolyaxonClients().version
    cli = cli or not any([cli, platform, lib])
    if cli:
        server_version = version_client.get_cli_version()
        version = get_version(PROJECT_CLI_NAME)
        click.echo('Current cli version: {}. \n'
                   'supported cli version {}'.format(version, server_version.to_dict()))

    if lib:
        server_version = version_client.get_lib_version()
        version = get_version(PROJECT_LIB_NAME)
        click.echo('Current lib version: {}. \n'
                   'supported lib version {}'.format(version, server_version.to_dict()))

    if platform:
        platform_version = version_client.get_platform_version()
        chart_version = version_client.get_chart_version()
        click.echo('You platform version: {}. \n'
                   'supported lib version {}'.format(chart_version.to_dict(),
                                                     platform_version.to_dict()))


@click.command()
@click.option('--lib', '-a', is_flag=True, default=False,
              help='Upgrade the project, if True upgrade the cli '
                   'otherwise upgrade the polyaxon library.')
def upgrade(lib):
    """Install/Upgrade polyaxon or polyxon-cli."""
    try:
        project_name = PROJECT_LIB_NAME if lib else PROJECT_CLI_NAME
        pip_upgrade(project_name)
    except Exception as e:
        logger.error(e)
