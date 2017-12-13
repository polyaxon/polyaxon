# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys
from polyaxon_client.exceptions import PolyaxonShouldExitError

from polyaxon_cli.logger import logger
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
@click.argument('group', type=str)
def get(group):
    """Get experiment group by uuid.

    Examples:
    ```
    polyaxon group get 50c62372137940ca8c456d8596946dd7
    ```
    """
    try:
        response = PolyaxonClients().experiment_group.get_experiment_group(group)
        PolyaxonClients.handle_response(
            response, error_message='no project was found with `{}`'.format(group))
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    response = response.to_dict()
    Printer.print_header("Experiment group info:")
    dict_tabulate(response)


@group.command()
@click.argument('group', type=str)
def delete(group):
    """Delete experiment group."""
    if not click.confirm("Are sure you want to delete experiment group `{}`".format(group)):
        click.echo('Existing without deleting experiment group.')
        sys.exit(0)

    try:
        response = PolyaxonClients().experiment_group.delete_experiment_group(group)
        PolyaxonClients.handle_response(
            group, error_message='The experiment group was not deleted.')
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    if response.status_code == 204:
        Printer.print_success("Experiment group `{}` was delete successfully".format(group))


@group.command()
@click.argument('group', type=str)
@click.option('--name', type=str,
              help='Name of the project, must be unique for the same user,')
@click.option('--description', type=str, help='Description of the project,')
def update(group, name, description):
    """Update experiement group.

    Example:

    ```
    polyaxon group update 50c62372137940ca8c456d8596946dd7 --description=new description for my experiments
    ```
    """
    update_dict = {}
    if name:
        update_dict['name'] = name

    if description:
        update_dict['description'] = description

    if not update_dict:
        Printer.print_warning('No argument was provided to update the experiment group.')
        sys.exit(0)

    try:
        response = PolyaxonClients().experiment_group.update_experiment_group(group, update_dict)
        PolyaxonClients.handle_response(
            group, error_message='The experiment group was not updated.')
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    Printer.print_success("Experiment group updated.")
    response = response.to_dict()
    Printer.print_header("Experiment group info:")
    dict_tabulate(response)


@group.command()
@click.argument('group', type=str)
@click.option('--page', type=int, help='To paginate through the list of experiments.')
def experiments(group, page):
    """List experiments for this experiment group"""
    page = page or 1
    try:
        response = PolyaxonClients().experiment_group.list_experiments(group, page=page)
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

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
        objects.pop('experiment_group')
        dict_tabulate(objects, is_list_dict=True)
