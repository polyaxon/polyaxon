# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys

import clint
from polyaxon_client.exceptions import PolyaxonShouldExitError, PolyaxonHTTPError
from polyaxon_schemas.plugins import PluginJobConfig

from polyaxon_cli.cli.check import check_polyaxonfile
from polyaxon_cli.cli.project import get_project_or_local, equal_projects
from polyaxon_cli.cli.upload import upload
from polyaxon_cli.managers.project import ProjectManager
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import Printer


@click.group()
@click.option('--project', '-p', type=str)
@click.pass_context
def notebook(ctx, project):
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project


@notebook.command()
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help='The polyaxon files to run.')
@click.option('-u', is_flag=True, default=False,
              help='To upload the repo before running.')
@click.pass_context
def start(ctx, file, u):
    """Start a notebook deployment for this project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon notebook start -f file -f file_override ...
    ```

    Example: upload before running

    \b
    ```bash
    $ polyaxon -p user12/mnist notebook start -f file -u
    ```
    """
    plx_file = None
    plugin_job = None
    if file:
        plx_file = check_polyaxonfile(file, log=False, is_plugin=True)

    # Check if we need to upload
    if u:
        ctx.invoke(upload)

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
        PolyaxonClients().project.start_notebook(user, project_name, plugin_job)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not start notebook project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success('Notebook is being deployed for project `{}`'.format(project_name))
    clint.textui.puts("It may take some time before you can access the dashboard.\n")
    clint.textui.puts("If you used an ingress, your dashboard will be available on:\n")
    with clint.textui.indent(4):
        clint.textui.puts("{}/notebook/{}/{}/\n".format(
            PolyaxonClients().auth.http_host, user, project_name))

    clint.textui.puts("Ohterwise you can use kubectl to get the url.")


@notebook.command()
@click.pass_context
def stop(ctx):
    """Stops the notebook deployment for this project if it exists.

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user, project_name = get_project_or_local(ctx.obj['project'])

    if not click.confirm("Are sure you want to stop notebook for project `{}/{}`".format(
        user, project_name)):
        click.echo('Existing without stopping notebook.')
        sys.exit(1)

    try:
        PolyaxonClients().project.stop_notebook(user, project_name)
        Printer.print_success('Notebook is being deleted')
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not stop notebook project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
