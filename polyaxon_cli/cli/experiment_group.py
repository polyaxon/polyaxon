# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys

from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError

from polyaxon_cli.cli.project import get_project_or_local
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import (
    Printer,
    get_meta_response,
    dict_tabulate,
    list_dicts_to_tabulate,
)


@click.group()
def group():
    """Commands for experiment groups."""
    pass


@group.command()
@click.argument('group', type=int)
@click.option('--project', '-p', type=str)
def get(group, project):
    """Get experiment group by uuid.

    Examples:
    ```
    polyaxon group get 13
    ```
    """
    user, project_name = get_project_or_local(project)
    try:
        response = PolyaxonClients().experiment_group.get_experiment_group(
            user, project_name, group)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get experiment group `{}`.'.format(group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    response = response.to_dict()
    Printer.print_header("Experiment group info:")
    dict_tabulate(response)


@group.command()
@click.argument('group', type=int)
@click.option('--project', '-p', type=str)
def delete(group, project):
    """Delete experiment group."""
    user, project_name = get_project_or_local(project)
    if not click.confirm("Are sure you want to delete experiment group `{}`".format(group)):
        click.echo('Existing without deleting experiment group.')
        sys.exit(0)

    try:
        response = PolyaxonClients().experiment_group.delete_experiment_group(
            user, project_name, group)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not delete experiment group `{}`.'.format(group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Experiment group `{}` was delete successfully".format(group))


@group.command()
@click.argument('group', type=int)
@click.option('--project', '-p', type=str)
@click.option('--description', type=str, help='Description of the project,')
def update(group, project, description):
    """Update experiement group.

    Example:

    ```
    polyaxon group update 2 --description="new description for my experiments"
    ```
    """
    user, project_name = get_project_or_local(project)
    update_dict = {}

    if description:
        update_dict['description'] = description

    if not update_dict:
        Printer.print_warning('No argument was provided to update the experiment group.')
        sys.exit(0)

    try:
        response = PolyaxonClients().experiment_group.update_experiment_group(
            user, project_name, group, update_dict)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not update experiment group `{}`.'.format(group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiment group updated.")
    response = response.to_dict()
    Printer.print_header("Experiment group info:")
    dict_tabulate(response)


@group.command()
@click.argument('group', type=int)
@click.option('--project', '-p', type=str)
@click.option('--page', type=int, help='To paginate through the list of experiments.')
def experiments(group, project, page):
    """List experiments for this experiment group"""
    user, project_name = get_project_or_local(project)
    page = page or 1
    try:
        response = PolyaxonClients().experiment_group.list_experiments(
            user, project_name, group, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get experiments for group `{}`.'.format(group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Experiments for experiment group `{}`.'.format(group))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No experiments found for experiment group `{}`.'.format(group))

    objects = list_dicts_to_tabulate([o.to_dict() for o in response['results']])
    if objects:
        Printer.print_header("Experiments:")
        objects.pop('group')
        dict_tabulate(objects, is_list_dict=True)
