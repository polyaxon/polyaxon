# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

import click
import click_completion

from marshmallow import ValidationError

from polyaxon import settings
from polyaxon.cli.admin import admin
from polyaxon.cli.auth import login, logout, whoami
from polyaxon.cli.bookmark import bookmark
from polyaxon.cli.check import check
from polyaxon.cli.cluster import cluster
from polyaxon.cli.completion import completion
from polyaxon.cli.config import config
from polyaxon.cli.dashboard import dashboard
from polyaxon.cli.deploy import deploy, teardown
from polyaxon.cli.init import init
from polyaxon.cli.projects import projects
from polyaxon.cli.run import run
from polyaxon.cli.runs import runs
from polyaxon.cli.upload import upload
from polyaxon.cli.user import user
from polyaxon.cli.version import check_cli_version, upgrade, version
from polyaxon.logger import clean_outputs, configure_logger
from polyaxon.managers.client import ClientConfigManager

click_completion.init()


@click.group()
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Turn on debug logging"
)
@click.option(
    "--offline",
    is_flag=True,
    default=False,
    help="Run command in offline mode if supported. "
    "Currently used for run command in --local mode.",
)
@click.pass_context
@clean_outputs
def cli(context, verbose, offline):
    """ Polyaxon CLI tool to:

        * Parse, Validate, and Check Polyaxonfiles.

        * Interact with Polyaxon server.

        * Run and Monitor experiments.

    Check the help available for each command listed below.
    """

    try:
        configure_logger(verbose or ClientConfigManager.get_value("debug"))
    except ValidationError:
        ClientConfigManager.purge()
    non_check_cmds = [
        "completion",
        "config",
        "version",
        "login",
        "logout",
        "deploy",
        "admin",
        "teardown",
    ]
    context.obj = context.obj or {}
    context.obj["offline"] = offline
    if offline:
        os.environ["POLYAXON_IS_OFFLINE"] = "true"
        settings.CLIENT_CONFIG.is_offline = True
    if not (context.invoked_subcommand in non_check_cmds or offline):
        check_cli_version()


cli.add_command(login)
cli.add_command(logout)
cli.add_command(whoami)
cli.add_command(user)
cli.add_command(upgrade)
cli.add_command(version)
cli.add_command(config)
cli.add_command(check)
cli.add_command(init)
cli.add_command(cluster)
cli.add_command(projects)
cli.add_command(runs)
cli.add_command(upload)
cli.add_command(run)
cli.add_command(dashboard)
cli.add_command(bookmark)
cli.add_command(admin)
cli.add_command(deploy)
cli.add_command(teardown)
cli.add_command(completion)
