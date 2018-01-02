# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys

from marshmallow import ValidationError

from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError
from polyaxon_schemas.project import ProjectConfig

from polyaxon_cli.managers.auth import AuthConfigManager
from polyaxon_cli.managers.project import ProjectManager
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils import constants
from polyaxon_cli.utils.formatting import (
    Printer,
    get_meta_response,
    list_dicts_to_tabulate,
    dict_tabulate
)


def get_project_info(project):
    parts = project.replace('.', '/').split('/')
    if len(parts) == 2:
        user, project_name = parts
    else:
        user = AuthConfigManager.get_value('username')
        project_name = project

    return user, project_name


def equal_projects(project1, project2):
    project1_info = get_project_info(project1)
    project2_info = get_project_info(project2)
    return project1_info == project2_info


def get_project_or_local(project=None):
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


@click.group()
@click.option('--project', '-p', type=str)
@click.pass_context
def project(ctx, project):
    """Commands for projects."""
    user, project_name = get_project_or_local(project)
    ctx.obj = ctx.obj or {}
    ctx.obj['user'] = user
    ctx.obj['project_name'] = project_name


@project.command()
@click.option('--name', required=True, type=str,
              help='Name of the project, must be unique for the same user')
@click.option('--description', type=str, help='Description of the project,')
@click.option('--private', is_flag=True, help='Set the visibility of the project to private.')
def create(name, description, private):
    """Create a new project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon project create --name=cats-vs-dogs --description="Image Classification with Deep Learning"
    ```
    """
    try:
        project_dict = dict(name=name, description=description, is_public=not private)
        project_config = ProjectConfig.from_dict(project_dict)
    except ValidationError:
        Printer.print_error('Project name should contain only alpha numerical, "-", and "_".')
        sys.exit(1)

    try:
        project = PolyaxonClients().project.create_project(project_config)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not create project `{}`.'.format(name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Project `{}` was created successfully.".format(project.name))


@project.command()
@click.option('--page', type=int, help='To paginate through the list of projects.')
def list(page):
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
        objects.pop('user', None)
        Printer.print_header("Projects:")
        dict_tabulate(objects, is_list_dict=True)


@project.command()
@click.pass_context
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
    user, project_name = ctx.obj['user'], ctx.obj['project_name']

    try:
        response = PolyaxonClients().project.get_project(user, project_name)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get project `{}`.'.format(project))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    response = response.to_light_dict(humanize_values=True)
    Printer.print_header("Project info:")
    dict_tabulate(response)


@project.command()
@click.pass_context
def delete(ctx):
    """Delete project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user, project_name = ctx.obj['user'], ctx.obj['project_name']

    if not click.confirm("Are sure you want to delete project `{}/{}`".format(user, project_name)):
        click.echo('Existing without deleting project.')
        sys.exit(1)

    try:
        response = PolyaxonClients().project.delete_project(user, project_name)
        # Purge caching
        ProjectManager.purge()
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not delete project `{}`.'.format(project))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Project `{}` was delete successfully".format(project))


@project.command()
@click.option('--name', type=str,
              help='Name of the project, must be unique for the same user,')
@click.option('--description', type=str, help='Description of the project,')
@click.option('--private', type=bool, help='Set the visibility of the project to private/public.')
@click.pass_context
def update(ctx, name, description, private):
    """Update project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon update foobar --description="Image Classification with Deep Learning using TensorFlow"
    ```

    \b
    ```bash
    $ polyaxon update mike1/foobar --description="Image Classification with Deep Learning using TensorFlow"
    ```
    """
    user, project_name = ctx.obj['user'], ctx.obj['project_name']

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
        Printer.print_error('Could not update project `{}`.'.format(project))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Project updated.")
    response = response.to_light_dict(humanize_values=True)
    Printer.print_header("Project info:")
    dict_tabulate(response)


@project.command()
@click.option('--page', type=int, help='To paginate through the list of groups.')
@click.pass_context
def groups(ctx, page):
    """List experiment groups for this project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user, project_name = ctx.obj['user'], ctx.obj['project_name']

    page = page or 1
    try:
        response = PolyaxonClients().project.list_experiment_groups(user, project_name, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get experiment groups for project `{}`.'.format(project))
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
@click.pass_context
def experiments(ctx, page):
    """List experiments for this project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user, project_name = ctx.obj['user'], ctx.obj['project_name']

    page = page or 1
    try:
        response = PolyaxonClients().project.list_experiments(user, project_name, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get experiments for project `{}`.'.format(project))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Experiments for project `{}/{}`.'.format(user, project_name))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No experiments found for project `{}/{}`.'.format(user, project_name))

    objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
               for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Experiments:")
        dict_tabulate(objects, is_list_dict=True)


@project.command()
@click.pass_context
def clone(ctx):
    pass


@project.command()
@click.pass_context
def tensorboard(ctx):
    pass


@project.command()
@click.pass_context
def notebook(ctx):
    pass
