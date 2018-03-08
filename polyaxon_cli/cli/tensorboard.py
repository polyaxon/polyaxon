# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys

import clint
from polyaxon_client.exceptions import PolyaxonShouldExitError, PolyaxonHTTPError
from polyaxon_schemas.plugins import PluginJobConfig

from polyaxon_cli.cli.check import check_polyaxonfile
from polyaxon_cli.cli.project import get_project_or_local, equal_projects
from polyaxon_cli.managers.project import ProjectManager
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
        click.echo("{}/tensorboard/{}/{}/\n".format(
            PolyaxonClients().auth.http_host, user, project_name))
    else:
        Printer.print_warning(
            'This project `{}` does not have a running tensorboard.'.format(project_name))
        click.echo('You can start tensorboard with this command: polyaxon tensorboard start')


@tensorboard.command()
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help='The polyaxon files to run.')
@click.pass_context
def start(ctx, file):
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
    plx_file = None
    plugin_job = None
    if file:
        plx_file = check_polyaxonfile(file, log=False, is_plugin=True)

    if plx_file:
        project = ProjectManager.get_config_or_raise()
        if not equal_projects(plx_file.project.name, project.unique_name):
            Printer.print_error('Your polyaxonfile defined a different project '
                                'than the one set in this repo.')
            sys.exit(1)

        plugin_job = PluginJobConfig(content=plx_file._data,
                                     config=plx_file.parsed_data)

    user, project_name = get_project_or_local(ctx.obj['project'])
    try:
        PolyaxonClients().project.start_tensorboard(user, project_name, plugin_job)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not start tensorboard project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success('Tensorboard is being deployed for project `{}`'.format(project_name))
    clint.textui.puts("It may take some time before you can access tensorboard.\n")
    clint.textui.puts("Your tensorboard will be available on:\n")
    with clint.textui.indent(4):
        clint.textui.puts("{}/tensorboard/{}/{}/\n".format(
            PolyaxonClients().auth.http_host, user, project_name))


@tensorboard.command()
@click.option('--yes', '-y', is_flag=True, default=False,
              help='Automatic yes to prompts. '
                   'Assume "yes" as answer to all prompts and run non-interactively.')
@click.pass_context
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
