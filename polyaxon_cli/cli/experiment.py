# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys
from polyaxon_client.exceptions import PolyaxonShouldExitError

from polyaxon_cli.logger import logger
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import (
    Printer,
    dict_tabulate,
    get_meta_response,
    list_dicts_to_tabulate,
)


@click.group()
def experiment():
    """Commands for experiments."""
    pass


@experiment.command()
@click.argument('experiment', type=str)
def get(experiment):
    """Get experiment by uuid.

    Examples:
    ```
    polyaxon experiment get 50c62372137940ca8c456d8596946dd7
    ```
    """
    try:
        response = PolyaxonClients().experiment.get_experiment(experiment)
        PolyaxonClients.handle_response(
            response, error_message='no experiment was found with `{}`'.format(experiment))
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    response = response.to_dict()
    Printer.print_header("Experiment info:")
    dict_tabulate(response)


@experiment.command()
@click.argument('experiment', type=str)
def delete(experiment):
    """Delete experiment group."""
    if not click.confirm("Are sure you want to delete experiment `{}`".format(experiment)):
        click.echo('Existing without deleting experiment.')
        sys.exit(0)

    try:
        response = PolyaxonClients().experiment.delete_experiment(experiment)
        PolyaxonClients.handle_response(
            experiment, error_message='The experiment was not deleted.')
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    if response.status_code == 204:
        Printer.print_success("Experiment `{}` was delete successfully".format(experiment))


@experiment.command()
@click.argument('experiment', type=str)
def stop(experiment):
    """Get experiment by uuid.

    Examples:
    ```
    polyaxon group stop 50c62372137940ca8c456d8596946dd7
    ```
    """
    if not click.confirm("Are sure you want to stop experiment `{}`".format(experiment)):
        click.echo('Existing without stopping experiment.')
        sys.exit(0)

    try:
        response = PolyaxonClients().experiment.stop(experiment)
        PolyaxonClients.handle_response(
            response, error_message='no experiment was found with `{}`'.format(experiment))
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    Printer.print_success("Experiment is being stopped.")


@experiment.command()
@click.argument('experiment', type=str)
def restart(experiment):
    """Delete experiment group."""
    try:
        response = PolyaxonClients().experiment.restart(experiment)
        PolyaxonClients.handle_response(
            experiment, error_message='The experiment was not restarted.')
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    response = response.to_dict()
    Printer.print_header("Experiment info:")
    dict_tabulate(response)


@experiment.command()
@click.argument('experiment', type=str)
@click.option('--page', type=int, help='To paginate through the list of experiments.')
def jobs(experiment, page):
    """List jobs for this experiment"""
    page = page or 1
    try:
        response = PolyaxonClients().experiment.list_jobs(experiment, page=page)
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Jobs for experiment `{}`.'.format(experiment))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No jobs found for experiment `{}`.'.format(experiment))

    objects = list_dicts_to_tabulate([o.to_dict() for o in response['results']])
    if objects:
        Printer.print_header("Jobs:")
        objects.pop('experiment')
        dict_tabulate(objects, is_list_dict=True)


@experiment.command()
@click.argument('experiment', type=str)
def status(experiment):
    """Get experiment status.

    Examples:
    ```
    polyaxon experiment status 50c62372137940ca8c456d8596946dd7
    ```
    """
    try:
        response = PolyaxonClients().experiment.get_status(experiment)
        PolyaxonClients.handle_response(
            response, error_message='no experiment was found for `{}`'.format(experiment))
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    response = response.to_dict()
    Printer.print_header("Experiment status:")
    dict_tabulate(response)


@experiment.command()
@click.argument('experiment', type=str)
def resources(experiment):
    """Get experiment resources.

    Examples:
    ```
    polyaxon experiment resources 50c62372137940ca8c456d8596946dd7
    ```
    """
    try:
        response = PolyaxonClients().experiment.resources(experiment)
        PolyaxonClients.handle_response(
            response, error_message='no resources for experiment `{}`'.format(experiment))
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    response = response.to_dict()
    Printer.print_header("Streaming experiment status:")
    dict_tabulate(response)


@experiment.command()
@click.argument('experiment', type=str)
def logs(experiment):
    """Get experiment logs.

    Examples:
    ```
    polyaxon experiment logs 50c62372137940ca8c456d8596946dd7
    ```
    """
    try:
        response = PolyaxonClients().experiment.logs(experiment)
        PolyaxonClients.handle_response(
            response, error_message='no logs for experiment `{}`'.format(experiment))
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    response = response.to_dict()
    Printer.print_header("Streamin experiment logs:")
    dict_tabulate(response)
