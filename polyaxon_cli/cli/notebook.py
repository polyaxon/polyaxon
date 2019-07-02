# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_cli.cli.check import check_polyaxonfile, check_polyaxonfile_kind
from polyaxon_cli.cli.project import get_project_or_local
from polyaxon_cli.cli.upload import upload
from polyaxon_cli.client import PolyaxonClient
from polyaxon_cli.client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.schemas import kinds
from polyaxon_cli.utils import indentation
from polyaxon_cli.utils.formatting import Printer
from polyaxon_client.exceptions import PolyaxonClientException


def get_notebook_url(user, project_name):
    return "{}/notebook/{}/{}/\n".format(PolyaxonClient().api_config.http_host, user, project_name)


@click.group()
@click.option('--project', '-p', type=str)
@click.pass_context
@clean_outputs
def notebook(ctx, project):
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project


@notebook.command()
@click.pass_context
@clean_outputs
def url(ctx):
    """Prints the notebook url for this project.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon notebook url
    ```
    """
    user, project_name = get_project_or_local(ctx.obj.get('project'))
    try:
        response = PolyaxonClient().project.get_project(user, project_name)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.has_notebook:
        click.echo(get_notebook_url(user, project_name))
    else:
        Printer.print_warning(
            'This project `{}` does not have a running notebook.'.format(project_name))
        click.echo('You can start a notebook with this command: polyaxon notebook start --help')


@notebook.command()
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help='The polyaxon files to run.')
@click.option('-u', is_flag=True, default=False,
              help='To upload the repo before running.')
@click.pass_context
@clean_outputs
def start(ctx, file, u):  # pylint:disable=redefined-builtin
    """Start a notebook deployment for this project.

    Uses [Caching](/references/polyaxon-cli/#caching)

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
    specification = None
    job_content = None
    if file:
        specification = check_polyaxonfile(file, log=False).specification

    # Check if we need to upload
    if u:
        ctx.invoke(upload, sync=False)

    if specification:
        # pylint:disable=protected-access
        check_polyaxonfile_kind(specification=specification, kind=kinds.NOTEBOOK)
        job_content = specification.raw_data
    user, project_name = get_project_or_local(ctx.obj.get('project'))
    try:
        response = PolyaxonClient().project.start_notebook(
            username=user,
            project_name=project_name,
            content=job_content,
            is_managed=True,
        )
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not start notebook project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 200:
        Printer.print_header("A notebook for this project is already running on:")
        click.echo(get_notebook_url(user, project_name))
        sys.exit(0)

    if response.status_code != 201:
        Printer.print_error('Something went wrong, Notebook was not created.')
        sys.exit(1)

    Printer.print_success('Notebook is being deployed for project `{}`'.format(project_name))
    indentation.puts("It may take some time before you can access the notebook.\n")
    indentation.puts("Your notebook will be available on:\n")
    with indentation.indent(4):
        indentation.puts(get_notebook_url(user, project_name))


@notebook.command()
@click.option('--commit', type=bool,
              help='Commit changes before stopping the notebook.')
@click.option('--yes', '-y', is_flag=True, default=False,
              help='Automatic yes to prompts. '
                   'Assume "yes" as answer to all prompts and run non-interactively.')
@click.pass_context
@clean_outputs
def stop(ctx, commit, yes):
    """Stops the notebook deployment for this project if it exists.

    Uses [Caching](/references/polyaxon-cli/#caching)
    """
    user, project_name = get_project_or_local(ctx.obj.get('project'))

    if not yes and not click.confirm("Are sure you want to stop notebook "
                                     "for project `{}/{}`".format(user, project_name)):
        click.echo('Existing without stopping notebook.')
        sys.exit(1)

    if commit is None:
        commit = True

    try:
        PolyaxonClient().project.stop_notebook(user, project_name, commit)
        Printer.print_success('Notebook is being deleted')
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not stop notebook project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
