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
    list_dicts_to_tabulate,
    get_experiments_with_declarations
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
              help='Name of the project, must be unique for the same user.')
@click.option('--description', type=str, help='Description of the project.')
@click.option('--tags', type=str, help='Tags, comma separated values, of the project.')
@click.option('--private', is_flag=True, help='Set the visibility of the project to private.')
@clean_outputs
def create(name, description, tags, private):
    """Create a new project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon project create --name=cats-vs-dogs --description="Image Classification with DL"
    ```
    """
    try:
        tags = tags.split(',') if tags else None
        project_dict = dict(name=name, description=description, is_public=not private, tags=tags)
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

    objects = list_dicts_to_tabulate(
        [o.to_light_dict(
            humanize_values=True,
            exclude_attrs=['uuid', 'experiment_groups', 'experiments', 'description',
                           'num_experiments', 'num_independent_experiments',
                           'num_experiment_groups', 'num_jobs', 'num_builds', 'unique_name'])
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
              help='Name of the project, must be unique for the same user.')
@click.option('--description', type=str, help='Description of the project.')
@click.option('--tags', type=str, help='Tags, comma separated values, of the project.')
@click.option('--private', type=bool, help='Set the visibility of the project to private/public.')
@click.pass_context
@clean_outputs
def update(ctx, name, description, tags, private):
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

    \b
    ```bash
    $ polyaxon update --tags="foo, bar"
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

    if tags:
        update_dict['tags'] = tags.split(',')

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
@click.option('--query', '-q', type=str,
              help='To filter the groups based on this query spec.')
@click.option('--sort', '-s', type=str, help='To change order by of the groups.')
@click.option('--page', type=int, help='To paginate through the list of groups.')
@click.pass_context
@clean_outputs
def groups(ctx, query, sort, page):
    """List experiment groups for this project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    Get all groups:

    \b
    ```bash
    $ polyaxon project groups
    ```

    Get all groups with with status {created or running}, and
    creation date between 2018-01-01 and 2018-01-02,
    and search algorithm not in {grid or random search}

    \b
    ```bash
    $ polyaxon project groups \
      -q "status:created|running, started_at:2018-01-01..2018-01-02, search_algorithm:~grid|random"
    ```

    Get all groups sorted by update date

    \b
    ```bash
    $ polyaxon project groups -s "-updated_at"
    ```
    """
    user, project_name = get_project_or_local(ctx.obj['project'])

    page = page or 1
    try:
        response = PolyaxonClients().project.list_experiment_groups(username=user,
                                                                    project_name=project_name,
                                                                    query=query,
                                                                    sort=sort,
                                                                    page=page)
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

    objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
               for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Experiment groups:")
        objects.pop('project', None)
        objects.pop('user', None)
        dict_tabulate(objects, is_list_dict=True)


@project.command()
@click.option('--query', '-q', type=str,
              help='To filter the jobs based on this query spec.')
@click.option('--sort', '-s', type=str, help='To change order by of the jobs.')
@click.option('--page', type=int, help='To paginate through the list of jobs.')
@click.pass_context
@clean_outputs
@clean_outputs
def jobs(ctx, query, sort, page):
    """List jobs for this project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    Get all jobs:

    \b
    ```bash
    $ polyaxon project jobs
    ```

    Get all jobs with with status not in {created or running}

    \b
    ```bash
    $ polyaxon project jobs -q "status:~created|running"
    ```

    Get all jobs with with status failed

    \b
    ```bash
    $ polyaxon project jobs -q "status:failed"
    ```

    Get all jobs sorted by update date

    \b
    ```bash
    $ polyaxon project jobs -s "-updated_at"
    ```
    """
    user, project_name = get_project_or_local(ctx.obj['project'])

    page = page or 1
    try:
        response = PolyaxonClients().project.list_jobs(username=user,
                                                       project_name=project_name,
                                                       query=query,
                                                       sort=sort,
                                                       page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get jobs for project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Jobs for project `{}/{}`.'.format(user, project_name))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No jobs found for project `{}/{}`.'.format(user, project_name))

    objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
               for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Jobs:")
        objects.pop('project_name', None)
        dict_tabulate(objects, is_list_dict=True)


@project.command()
@click.option('--metrics', '-m', is_flag=True, help='List experiments with their metrics.')
@click.option('--declarations', '-d', is_flag=True,
              help='List experiments with their declarations/params.')
@click.option('--independent', '-i', is_flag=True, help='To return only independent experiments.')
@click.option('--group', '-g', type=int, help='To filter experiments for a specific group.')
@click.option('--query', '-q', type=str,
              help='To filter the experiments based on this query spec.')
@click.option('--sort', '-s', type=str, help='To change order by of the experiments.')
@click.option('--page', type=int, help='To paginate through the list of experiments.')
@click.pass_context
@clean_outputs
@clean_outputs
def experiments(ctx, metrics, declarations, independent, group, query, sort, page):
    """List experiments for this project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    Get all experiments:

    \b
    ```bash
    $ polyaxon project experiments
    ```

    Get all experiments with with status {created or running}, and
    creation date between 2018-01-01 and 2018-01-02, and declarations activation equal to sigmoid
    and metric loss less or equal to 0.2

    \b
    ```bash
    $ polyaxon project experiments \
      -q "status:created|running, started_at:2018-01-01..2018-01-02, \
          declarations.activation:sigmoid, metric.loss:<=0.2"
    ```

    Get all experiments sorted by update date

    \b
    ```bash
    $ polyaxon project experiments -s "-updated_at"
    ```
    """
    user, project_name = get_project_or_local(ctx.obj['project'])

    page = page or 1
    try:
        response = PolyaxonClients().project.list_experiments(username=user,
                                                              project_name=project_name,
                                                              independent=independent,
                                                              group=group,
                                                              metrics=metrics,
                                                              declarations=declarations,
                                                              query=query,
                                                              sort=sort,
                                                              page=page)
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
    elif declarations:
        objects = get_experiments_with_declarations(response)
    else:
        objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
                   for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Experiments:")
        objects.pop('project_name', None)
        dict_tabulate(objects, is_list_dict=True)


@project.command()
@click.option('--page', type=int, help='To paginate through the list of build builds.')
@click.option('--query', '-q', type=str,
              help='To filter the builds based on this query spec.')
@click.option('--sort', '-s', type=str, help='To change order by of the builds.')
@click.pass_context
@clean_outputs
def builds(ctx, query, sort, page):
    """List build jobs for this project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    Get all builds:

    \b
    ```bash
    $ polyaxon project builds
    ```

    Get all builds with with status not in {created or running}

    \b
    ```bash
    $ polyaxon project builds -q "status:~created"
    ```

    Get all builds with with status failed

    \b
    ```bash
    $ polyaxon project builds -q "status:failed"
    ```

    Get all builds sorted by update date

    \b
    ```bash
    $ polyaxon project builds -s "-updated_at"
    ```
    """
    user, project_name = get_project_or_local(ctx.obj['project'])

    page = page or 1
    try:
        response = PolyaxonClients().project.list_builds(username=user,
                                                         project_name=project_name,
                                                         query=query,
                                                         sort=sort,
                                                         page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get builds for project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Builds for project `{}/{}`.'.format(user, project_name))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No builds found for project `{}/{}`.'.format(user, project_name))

    objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
               for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Builds:")
        objects.pop('project_name', None)
        dict_tabulate(objects, is_list_dict=True)


@project.command()
@click.option('--page', type=int, help='To paginate through the list of tensorboard jobs.')
@click.option('--query', '-q', type=str,
              help='To filter the tensorboard jobs based on this query spec.')
@click.option('--sort', '-s', type=str, help='To change order by of the tensorboard jobss.')
@click.pass_context
@clean_outputs
def tensorboards(ctx, query, sort, page):
    """List tensorboard jobs for this project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user, project_name = get_project_or_local(ctx.obj['project'])

    page = page or 1
    try:
        response = PolyaxonClients().project.list_tensorboards(username=user,
                                                               project_name=project_name,
                                                               query=query,
                                                               sort=sort,
                                                               page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get tensorboards for project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Tensorboards for project `{}/{}`.'.format(user, project_name))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No tensorboards found for project `{}/{}`.'.format(user,
                                                                                 project_name))

    objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
               for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Tensorboards:")
        objects.pop('project_name', None)
        dict_tabulate(objects, is_list_dict=True)


@project.command()
@click.pass_context
@clean_outputs
def download(ctx):
    """Download code of the current project."""
    user, project_name = get_project_or_local(ctx.obj['project'])
    try:
        PolyaxonClients().project.download_repo(user, project_name)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not download code for project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
    Printer.print_success('Files downloaded.')


@project.command()
@click.pass_context
@clean_outputs
def bookmark(ctx):
    """Bookmark project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user, project_name = get_project_or_local(ctx.obj['project'])

    try:
        PolyaxonClients().project.bookmark(user, project_name)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not bookmark project `{}/{}`.'.format(user, project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Project `{}/{}` is bookmarked.".format(user, project_name))


@project.command()
@click.pass_context
@clean_outputs
def unbookmark(ctx):
    """Unbookmark project.

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user, project_name = get_project_or_local(ctx.obj['project'])

    try:
        PolyaxonClients().project.unbookmark(user, project_name)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not unbookmark project `{}/{}`.'.format(user, project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Project `{}/{}` is unbookmarked.".format(user, project_name))
