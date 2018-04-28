# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click
import clint

from polyaxon_cli.cli.check import check_polyaxonfile, check_polyaxonfile_kind
from polyaxon_cli.cli.project import get_project_or_local
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import Printer
from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError
from polyaxon_schemas.plugins import PluginJobConfig


def get_tensorboard_url(user, project_name):
    return "{}/tensorboard/{}/{}/\n".format(PolyaxonClients().auth.http_host, user, project_name)


@click.group()
@click.option('--project', '-p', type=str)
@click.pass_context
@clean_outputs
def tensorboard(ctx, project):
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project


@tensorboard.command()
@click.pass_context
@clean_outputs
def url(ctx):
    """Prints the tensorboard url for this project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon tensorboard url
    ```
    """
    user, project_name = get_project_or_local(ctx.obj['project'])
    try:
        response = PolyaxonClients().project.get_project(user, project_name)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.has_tensorboard:
        click.echo(get_tensorboard_url(user, project_name))
    else:
        Printer.print_warning(
            'This project `{}` does not have a running tensorboard.'.format(project_name))
        click.echo('You can start tensorboard with this command: polyaxon tensorboard start')


@tensorboard.command()
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help='The polyaxon files to run.')
@click.pass_context
@clean_outputs
def start(ctx, file):  # pylint:disable=redefined-builtin
    """Start a tensorboard deployment for this project.

    It will show a tensorboard with all experiments under the project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example: using the default tensorflow image 1.4.1.

    \b
    ```bash
    $ polyaxon tensorboard start
    ```

    Example: with custom image and resources

    \b
    ```bash
    $ polyaxon tensorboard start -f file -f file_override ...
    ```
    """
    specification = None
    plugin_job = None
    if file:
        specification = check_polyaxonfile(file, log=False).specification

    if specification:
        # pylint:disable=protected-access
        check_polyaxonfile_kind(specification=specification, kind=specification._PLUGIN)
        plugin_job = PluginJobConfig(config=specification.parsed_data)

    user, project_name = get_project_or_local(ctx.obj['project'])
    try:
        response = PolyaxonClients().project.start_tensorboard(user, project_name, plugin_job)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not start tensorboard project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 200:
        Printer.print_header("A notebook for this project is already running on:")
        click.echo(get_tensorboard_url(user, project_name))
        sys.exit(0)

    if response.status_code != 201:
        Printer.print_error('Something went wrong, Tensorboard was not created.')
        sys.exit(1)

    Printer.print_success('Tensorboard is being deployed for project `{}`'.format(project_name))
    clint.textui.puts("It may take some time before you can access tensorboard.\n")
    clint.textui.puts("Your tensorboard will be available on:\n")
    with clint.textui.indent(4):
        clint.textui.puts(get_tensorboard_url(user, project_name))


@tensorboard.command()
@click.option('--yes', '-y', is_flag=True, default=False,
              help='Automatic yes to prompts. '
                   'Assume "yes" as answer to all prompts and run non-interactively.')
@click.pass_context
@clean_outputs
def stop(ctx, yes):
    """Stops the tensorboard deployment for this project if it exists.

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user, project_name = get_project_or_local(ctx.obj['project'])

    if not yes and not click.confirm("Are sure you want to stop tensorboard "
                                     "for project `{}/{}`".format(user, project_name)):
        click.echo('Existing without stopping tensorboard.')
        sys.exit(1)

    try:
        PolyaxonClients().project.stop_tensorboard(user, project_name)
        Printer.print_success('Tensorboard is being deleted')
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not stop tensorboard project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
