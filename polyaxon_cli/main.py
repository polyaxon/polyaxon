# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys
import pkg_resources

from distutils.version import LooseVersion

from polyaxon_schemas.polyaxonfile.logger import configure_logger

from polyaxon_cli.cli.init import init
from polyaxon_cli.cli.check import check
from polyaxon_cli.cli.auth import login, logout
from polyaxon_cli.cli.config import config
from polyaxon_cli.cli.logs import logs
from polyaxon_cli.cli.run import run
from polyaxon_cli.cli.status import status
from polyaxon_cli.cli.stop import stop
from polyaxon_cli.cli.version import version, upgrade
from polyaxon_cli.client.version import VersionClient
from polyaxon_cli.managers.config import GlobalConfigManager


@click.group()
@click.option('-v', '--verbose', help='Turn on debug logging')
def cli(verbose):
    """ Polyaxon CLI tool for
        * parsing Polyaxonfiles,
        * interacting with hub.Polyaxon server
        * executing commands.
    Check the help available for each command listed below.
    """
    configure_logger(verbose or GlobalConfigManager.get_value('verbose'))
    # check_cli_version()


def check_cli_version():
    """Check if the current cli version satisfies the server requirements"""
    server_version = VersionClient().get_cli_version()
    current_version = pkg_resources.get_distribution('polyaxon-cli').version
    if LooseVersion(current_version) < LooseVersion(server_version.min_version):
        click.echo("""Your version of CLI ({}) is no longer compatible with server.""".format(
            current_version))
        if click.confirm("Do you want to upgrade to "
                         "version {} now?".format(server_version.latest_version)):
            from polyaxon_cli.cli.version import pip_upgrade
            pip_upgrade()
            sys.exit(0)
        else:
            click.echo("""Your can manually run:
    pip install -U polyaxon-cli
to upgrade to the latest version `{}`)""".format(server_version.latest_version))
            sys.exit(0)
    elif LooseVersion(current_version) < LooseVersion(server_version.latest_version):
        click.echo("""New version of CLI (%s) is now available. To upgrade run:
    pip install -U polyaxon-cli""".format(server_version.latest_version))


cli.add_command(login)
cli.add_command(logout)
cli.add_command(run)
cli.add_command(stop)
cli.add_command(status)
cli.add_command(logs)
cli.add_command(upgrade)
cli.add_command(version)
cli.add_command(config)
cli.add_command(check)
cli.add_command(init)
