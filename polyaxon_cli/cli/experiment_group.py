# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_cli.cli.project import get_project_or_local
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.experiment_group import GroupManager
from polyaxon_cli.utils import cache
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


def get_group_or_local(_group):
    return _group or GroupManager.get_config_or_raise().id


def get_project_group_or_local(project=None, group=None):  # pylint:disable=redefined-outer-name
    user, project_name = get_project_or_local(project)
    group = get_group_or_local(group)
    return user, project_name, group


def get_group_details(group):  # pylint:disable=redefined-outer-name
    if group.description:
        Printer.print_header("Experiment group description:")
        click.echo('{}\n'.format(group.description))

    response = group.to_light_dict(
        humanize_values=True,
        exclude_attrs=['uuid', 'content', 'project', 'experiments', 'description'])

    Printer.print_header("Experiment group info:")
    dict_tabulate(Printer.add_status_color(response))


@click.group()
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'.")
@click.option('--group', '-g', type=int, help="The group id number.")
@click.pass_context
@clean_outputs
def group(ctx, project, group):  # pylint:disable=redefined-outer-name
    """Commands for experiment groups."""
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project
    ctx.obj['group'] = group


@group.command()
@click.pass_context
@clean_outputs
def get(ctx):
    """Get experiment group by uuid.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon group -g 13 get
    ```
    """
    user, project_name, _group = get_project_group_or_local(ctx.obj['project'], ctx.obj['group'])
    try:
        response = PolyaxonClients().experiment_group.get_experiment_group(
            user, project_name, _group)
        cache.cache(config_manager=GroupManager, response=response)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get experiment group `{}`.'.format(_group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    get_group_details(response)


@group.command()
@click.pass_context
@clean_outputs
def delete(ctx):
    """Delete experiment group.

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user, project_name, _group = get_project_group_or_local(ctx.obj['project'], ctx.obj['group'])

    if not click.confirm("Are sure you want to delete experiment group `{}`".format(_group)):
        click.echo('Existing without deleting experiment group.')
        sys.exit(0)

    try:
        response = PolyaxonClients().experiment_group.delete_experiment_group(
            user, project_name, _group)
        # Purge caching
        GroupManager.purge()
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not delete experiment group `{}`.'.format(_group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Experiment group `{}` was delete successfully".format(_group))


@group.command()
@click.option('--name', type=str,
              help='Name of the group, must be unique within the project, could none.')
@click.option('--description', type=str, help='Description of the group.')
@click.option('--tags', type=str, help='Tags of the group, comma separated values.')
@click.pass_context
@clean_outputs
def update(ctx, name, description, tags):
    """Update experiment group.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon group -g 2 update --description="new description for this group"
    ```

    \b
    ```bash
    $ polyaxon update --tags="foo, bar"
    ```
    """
    user, project_name, _group = get_project_group_or_local(ctx.obj['project'], ctx.obj['group'])
    update_dict = {}

    if name:
        update_dict['name'] = name

    if description:
        update_dict['description'] = description

    if tags:
        update_dict['tags'] = tags.split(',')

    if not update_dict:
        Printer.print_warning('No argument was provided to update the experiment group.')
        sys.exit(0)

    try:
        response = PolyaxonClients().experiment_group.update_experiment_group(
            user, project_name, _group, update_dict)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not update experiment group `{}`.'.format(_group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiment group updated.")
    get_group_details(response)


@group.command()
@click.option('--metrics', '-m', is_flag=True, help='List experiments with their metrics.')
@click.option('--declarations', '-d', is_flag=True,
              help='List experiments with their declarations/params.')
@click.option('--query', '-q', type=str,
              help='To filter the experiments based on this query spec.')
@click.option('--sort', '-s', type=str, help='To change order by of the experiments.')
@click.option('--page', type=int, help='To paginate through the list of experiments.')
@click.pass_context
@clean_outputs
def experiments(ctx, metrics, declarations, query, sort, page):
    """List experiments for this experiment group

    Uses [Caching](/polyaxon_cli/introduction#Caching)
    """
    user, project_name, _group = get_project_group_or_local(ctx.obj['project'], ctx.obj['group'])
    page = page or 1
    try:
        response = PolyaxonClients().experiment_group.list_experiments(username=user,
                                                                       project_name=project_name,
                                                                       group_id=_group,
                                                                       metrics=metrics,
                                                                       declarations=declarations,
                                                                       query=query,
                                                                       sort=sort,
                                                                       page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get experiments for group `{}`.'.format(_group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Experiments for experiment group `{}`.'.format(_group))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No experiments found for experiment group `{}`.'.format(_group))

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
        objects.pop('experiment_group', None)
        objects.pop('experiment_group_name', None)
        objects.pop('project_name', None)
        dict_tabulate(objects, is_list_dict=True)


@group.command()
@click.option('--yes', '-y', is_flag=True, default=False,
              help='Automatic yes to prompts. '
                   'Assume "yes" as answer to all prompts and run non-interactively.')
@click.option('--pending', is_flag=True, default=False,
              help='To stop only pending experiments, i.e. leave currently running one intact.')
@click.pass_context
@clean_outputs
def stop(ctx, yes, pending):
    """Stop experiments in the group.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples: stop only pending experiments

    \b
    ```bash
    $ polyaxon group stop --pending
    ```

    Examples: stop all unfinished

    \b
    ```bash
    $ polyaxon group stop
    ```

    \b
    ```bash
    $ polyaxon group -g 2 stop
    ```
    """
    user, project_name, _group = get_project_group_or_local(ctx.obj['project'], ctx.obj['group'])

    if not yes and not click.confirm("Are sure you want to stop experiments "
                                     "in group `{}`".format(_group)):
        click.echo('Existing without stopping experiments in group.')
        sys.exit(0)

    try:
        PolyaxonClients().experiment_group.stop(user, project_name, _group, pending=pending)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not stop experiments in group `{}`.'.format(_group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiments in group are being stopped.")


@group.command()
@click.option('--page', type=int, help="To paginate through the list of statuses.")
@click.pass_context
@clean_outputs
def statuses(ctx, page):
    """Get experiment group statuses.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon group -g 2 statuses
    ```
    """
    user, project_name, _group = get_project_group_or_local(ctx.obj['project'], ctx.obj['group'])
    page = page or 1
    try:
        response = PolyaxonClients().experiment_group.get_statuses(user,
                                                                   project_name,
                                                                   _group,
                                                                   page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get status for group `{}`.'.format(_group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Statuses for group `{}`.'.format(_group))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No statuses found for group `{}`.'.format(_group))

    objects = list_dicts_to_tabulate(
        [Printer.add_status_color(o.to_light_dict(humanize_values=True), status_key='status')
         for o in response['results']])
    if objects:
        Printer.print_header("Statuses:")
        objects.pop('experiment_group', None)
        dict_tabulate(objects, is_list_dict=True)


@group.command()
@click.pass_context
@clean_outputs
def bookmark(ctx):
    """Bookmark group.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon group bookmark
    ```

    \b
    ```bash
    $ polyaxon group -g 2 bookmark
    ```
    """
    user, project_name, _group = get_project_group_or_local(ctx.obj['project'], ctx.obj['group'])

    try:
        PolyaxonClients().experiment_group.bookmark(user, project_name, _group)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not bookmark group `{}`.'.format(_group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiments group is bookmarked.")


@group.command()
@click.pass_context
@clean_outputs
def unbookmark(ctx):
    """Unbookmark group.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon group unbookmark
    ```

    \b
    ```bash
    $ polyaxon group -g 2 unbookmark
    ```
    """
    user, project_name, _group = get_project_group_or_local(ctx.obj['project'], ctx.obj['group'])

    try:
        PolyaxonClients().experiment_group.unbookmark(user, project_name, _group)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not unbookmark group `{}`.'.format(_group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiments group is unbookmarked.")
