# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from marshmallow import ValidationError

from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.auth import AuthConfigManager
from polyaxon_cli.managers.project import ProjectManager
from polyaxon_cli.utils import constants
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import (
    Printer,
    dict_tabulate,
    get_experiments_with_metrics,
    get_meta_response,
    list_dicts_to_tabulate
)
from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError
from polyaxon_schemas.project import ProjectConfig


def get_project_info(project):  # pylint:disable=redefined-outer-name
    parts = project.replace('.', '/').split('/')
    if len(parts) == 2:
        user, project_name = parts
    else:
        user = AuthConfigManager.get_value('username')
        project_name = project

    return user, project_name


def get_project_or_local(project=None):  # pylint:disable=redefined-outer-name
    if not project and not ProjectManager.is_initialized():
        Printer.print_error('Please provide a valid project, or init a new project. '
                            ' {}'.format(constants.INIT_COMMAND))
        sys.exit(1)

    if project:
        user, project_name = get_project_info(project)
    else:
        project = ProjectManager.get_config()
        user, project_name = project.user, project.name

    if not all([user, project_name]):
        Printer.print_error('Please provide a valid project, or init a new project.'
                            ' {}'.format(constants.INIT_COMMAND))
        sys.exit(1)
    return user, project_name


def get_project_details(project):  # pylint:disable=redefined-outer-name
    if project.description:
        Printer.print_header("Project description:")
        click.echo('{}\n'.format(project.description))

    response = project.to_light_dict(
        humanize_values=True,
        exclude_attrs=['uuid', 'experiment_groups', 'experiments', 'description'])

    Printer.print_header("Project info:")
    dict_tabulate(response)


@click.group()
@click.option('--project', '-p', type=str)
@click.pass_context
@clean_outputs
def project(ctx, project):  # pylint:disable=redefined-outer-name
    """Commands for projects."""
    if ctx.invoked_subcommand not in ['create', 'list']:
        ctx.obj = ctx.obj or {}
        ctx.obj['project'] = project


@project.command()
@click.option('--name', required=True, type=str,
              help='Name of the project, must be unique for the same user')
@click.option('--description', type=str, help='Description of the project,')
@click.option('--private', is_flag=True, help='Set the visibility of the project to private.')
@clean_outputs
def create(name, description, private):
    """Create a new project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon project create --name=cats-vs-dogs --description="Image Classification with DL"
    ```
    """
    try:
        project_dict = dict(name=name, description=description, is_public=not private)
        project_config = ProjectConfig.from_dict(project_dict)
    except ValidationError:
        Printer.print_error('Project name should contain only alpha numerical, "-", and "_".')
        sys.exit(1)

    try:
        _project = PolyaxonClients().project.create_project(project_config)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not create project `{}`.'.format(name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Project `{}` was created successfully.".format(_project.name))


@project.command()
@click.option('--page', type=int, help='To paginate through the list of projects.')
@clean_outputs
def list(page):  # pylint:disable=redefined-builtin
    """List projects.

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user = AuthConfigManager.get_value('username')
    if not user:
        Printer.print_error('Please login first. `polyaxon login --help`')

    page = page or 1
    try:
        response = PolyaxonClients().project.list_projects(user, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get list of projects.')
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Projects for current user')
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No projects found for current user')

    objects = list_dicts_to_tabulate([o.to_light_dict(humanize_values=True)
                                      for o in response['results']])
    if objects:
        Printer.print_header("Projects:")
        dict_tabulate(objects, is_list_dict=True)


@project.command()
@click.pass_context
@clean_outputs
def get(ctx):
    """Get info for current project, by project_name, or user/project_name.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    To get current project:

    \b
    ```bash
    $ polyaxon project get
    ```

    To get a project by name

    \b
    ```bash
    $ polyaxon project get user/project
    ```
    """
    user, project_name = get_project_or_local(ctx.obj['project'])

    try:
        response = PolyaxonClients().project.get_project(user, project_name)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    get_project_details(response)


@project.command()
@click.pass_context
@clean_outputs
def delete(ctx):
    """Delete project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user, project_name = get_project_or_local(ctx.obj['project'])

    if not click.confirm("Are sure you want to delete project `{}/{}`".format(user, project_name)):
        click.echo('Existing without deleting project.')
        sys.exit(1)

    try:
        response = PolyaxonClients().project.delete_project(user, project_name)
        local_project = ProjectManager.get_config()
        if (user, project_name) == (local_project.user, local_project.name):
            # Purge caching
            ProjectManager.purge()
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not delete project `{}/{}`.'.format(user, project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Project `{}/{}` was delete successfully".format(user, project_name))


@project.command()
@click.option('--name', type=str,
              help='Name of the project, must be unique for the same user,')
@click.option('--description', type=str, help='Description of the project,')
@click.option('--private', type=bool, help='Set the visibility of the project to private/public.')
@click.pass_context
@clean_outputs
def update(ctx, name, description, private):
    """Update project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon update foobar --description="Image Classification with DL using TensorFlow"
    ```

    \b
    ```bash
    $ polyaxon update mike1/foobar --description="Image Classification with DL using TensorFlow"
    ```
    """
    user, project_name = get_project_or_local(ctx.obj['project'])

    update_dict = {}
    if name:
        update_dict['name'] = name

    if description:
        update_dict['description'] = description

    if private is not None:
        update_dict['is_public'] = not private

    if not update_dict:
        Printer.print_warning('No argument was provided to update the project.')
        sys.exit(1)

    try:
        response = PolyaxonClients().project.update_project(user, project_name, update_dict)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not update project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Project updated.")
    get_project_details(response)


@project.command()
@click.option('--page', type=int, help='To paginate through the list of groups.')
@click.pass_context
@clean_outputs
def groups(ctx, page):
    """List experiment groups for this project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user, project_name = get_project_or_local(ctx.obj['project'])

    page = page or 1
    try:
        response = PolyaxonClients().project.list_experiment_groups(user, project_name, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error(
            'Could not get experiment groups for project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Experiment groups for project `{}/{}`.'.format(user, project_name))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No experiment groups found for project `{}/{}`.'.format(
            user, project_name))

    objects = list_dicts_to_tabulate([o.to_light_dict(humanize_values=True)
                                      for o in response['results']])
    if objects:
        Printer.print_header("Experiment groups:")
        objects.pop('project', None)
        objects.pop('user', None)
        dict_tabulate(objects, is_list_dict=True)


@project.command()
@click.option('--page', type=int, help='To paginate through the list of experiments.')
@click.option('--metrics', '-m', is_flag=True, help='List experiments with their metrics.')
@click.pass_context
@clean_outputs
@clean_outputs
def experiments(ctx, page, metrics):
    """List experiments for this project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user, project_name = get_project_or_local(ctx.obj['project'])

    page = page or 1
    try:
        response = PolyaxonClients().project.list_experiments(user, project_name, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get experiments for project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Experiments for project `{}/{}`.'.format(user, project_name))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No experiments found for project `{}/{}`.'.format(user, project_name))

    if metrics:
        objects = get_experiments_with_metrics(response)
    else:
        objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
                   for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Experiments:")
        objects.pop('project_name', None)
        dict_tabulate(objects, is_list_dict=True)


@project.command()
@click.pass_context
@clean_outputs
def clone(ctx):
    pass
