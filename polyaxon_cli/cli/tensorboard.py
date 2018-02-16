# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys

import clint
from polyaxon_client.exceptions import PolyaxonShouldExitError, PolyaxonHTTPError

from polyaxon_cli.cli.project import get_project_or_local
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import Printer


@click.group()
@click.option('--project', '-p', type=str)
@click.pass_context
def tensorboard(ctx, project):
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project


@tensorboard.command()
@click.pass_context
def start(ctx):
    """Start a tensorboard deployment for this project.

    It will show a tensorboard with all experiments under the project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user, project_name = get_project_or_local(ctx.obj['project'])
    try:
        PolyaxonClients().project.start_tensorboard(user, project_name)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not start tensorboard project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success('Tensorboard is being deployed for project `{}`'.format(project_name))
    clint.textui.puts("It may take some time before you can access the dashboard.\n")
    clint.textui.puts("If you used an ingress, your dashboard will be available on:\n")
    with clint.textui.indent(4):
        clint.textui.puts("{}/tensorboard/{}/{}/\n".format(
            PolyaxonClients().auth.http_host, user, project_name))

    clint.textui.puts("Ohterwise you can use kubectl to get the url.")


@tensorboard.command()
@click.pass_context
def stop(ctx):
    """Stops the tensorboard deployment for this project if it exists.

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user, project_name = get_project_or_local(ctx.obj['project'])

    if not click.confirm("Are sure you want to stop tensorboard for project `{}/{}`".format(
        user, project_name)):
        click.echo('Existing without stopping tensorboard.')
        sys.exit(1)

    try:
        PolyaxonClients().project.stop_tensorboard(user, project_name)
        Printer.print_success('Tensorboard is being deleted')
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not stop tensorboard project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
