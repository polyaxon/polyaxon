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
PROJECT_NAME = "polyaxon"


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

    current_version = pkg_resources.get_distribution('polyaxon-cli').version
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
@click.option('--all', '-a', is_flag=True, default=False,
              help='Version of the project, if True the version of the cli '
                   'otherwise the version the polyaxon library.')
def version(all):
    """Prints the current version of the CLI."""
    project_name = PROJECT_NAME if all else PROJECT_CLI_NAME
    version = get_version(project_name)
    logger.info(version)


@click.command()
@click.option('--all', '-a', is_flag=True, default=False,
              help='Upgrade the project, if True upgrade the cli '
                   'otherwise upgrade the polyaxon library.')
def upgrade(all):
    """Install/Upgrade polyaxon or polyxon-cli."""
    try:
        project_name = PROJECT_NAME if all else PROJECT_CLI_NAME
        pip_upgrade(project_name)
    except Exception as e:
        logger.error(e)
