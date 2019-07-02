# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import click_completion

from marshmallow import ValidationError

from polyaxon_cli.cli.admin import admin
from polyaxon_cli.cli.auth import login, logout, whoami
from polyaxon_cli.cli.bookmark import bookmark
from polyaxon_cli.cli.build import build
from polyaxon_cli.cli.check import check
from polyaxon_cli.cli.cluster import cluster
from polyaxon_cli.cli.completion import completion
from polyaxon_cli.cli.config import config
from polyaxon_cli.cli.dashboard import dashboard
from polyaxon_cli.cli.deploy import deploy, teardown
from polyaxon_cli.cli.experiment import experiment
from polyaxon_cli.cli.experiment_group import group
from polyaxon_cli.cli.init import init
from polyaxon_cli.cli.job import job
from polyaxon_cli.cli.notebook import notebook
from polyaxon_cli.cli.project import project
from polyaxon_cli.cli.run import run
from polyaxon_cli.cli.superuser import superuser
from polyaxon_cli.cli.tensorboard import tensorboard
from polyaxon_cli.cli.upload import upload
from polyaxon_cli.cli.user import user
from polyaxon_cli.cli.version import check_cli_version, upgrade, version
from polyaxon_cli.logger import clean_outputs, configure_logger
from polyaxon_cli.managers.config import GlobalConfigManager

click_completion.init()


@click.group()
@click.option('-v', '--verbose', is_flag=True, default=False, help='Turn on debug logging')
@click.pass_context
@clean_outputs
def cli(context, verbose):
    """ Polyaxon CLI tool to:

        * Parse, Validate, and Check Polyaxonfiles.

        * Interact with Polyaxon server.

        * Run and Monitor experiments.

    Check the help available for each command listed below.
    """

    try:
        configure_logger(verbose or GlobalConfigManager.get_value('verbose'))
    except ValidationError:
        GlobalConfigManager.purge()
    non_check_cmds = [
        'completion', 'config', 'version', 'login', 'logout', 'deploy', 'admin', 'teardown'
    ]
    if context.invoked_subcommand not in non_check_cmds:
        check_cli_version()


cli.add_command(login)
cli.add_command(logout)
cli.add_command(whoami)
cli.add_command(user)
cli.add_command(superuser)
cli.add_command(upgrade)
cli.add_command(version)
cli.add_command(config)
cli.add_command(check)
cli.add_command(init)
cli.add_command(cluster)
cli.add_command(project)
cli.add_command(build)
cli.add_command(tensorboard)
cli.add_command(notebook)
cli.add_command(group)
cli.add_command(experiment)
cli.add_command(job)
cli.add_command(upload)
cli.add_command(run)
cli.add_command(dashboard)
cli.add_command(bookmark)
cli.add_command(admin)
cli.add_command(deploy)
cli.add_command(teardown)
cli.add_command(completion)
