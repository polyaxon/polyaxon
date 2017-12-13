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
def job():
    """Commands for jobs."""
    pass


@job.command()
@click.argument('job', type=str)
def get(job):
    """Get job by uuid.

    Examples:
    ```
    polyaxon job get 50c62372137940ca8c456d8596946dd7
    ```
    """
    try:
        response = PolyaxonClients().job.get_job(job)
        PolyaxonClients.handle_response(
            response, error_message='no job was found with `{}`'.format(job))
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    response = response.to_dict()
    Printer.print_header("Job info:")
    dict_tabulate(response)


@job.command()
@click.argument('job', type=str)
def status(job):
    """Get job status.

    Examples:
    ```
    polyaxon job status 50c62372137940ca8c456d8596946dd7
    ```
    """
    try:
        response = PolyaxonClients().job.get_status(job)
        PolyaxonClients.handle_response(
            response, error_message='no job was found for `{}`'.format(job))
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    response = response.to_dict()
    Printer.print_header("Job status:")
    dict_tabulate(response)


@job.command()
@click.argument('job', type=str)
def resources(job):
    """Get job resources.

    Examples:
    ```
    polyaxon job resources 50c62372137940ca8c456d8596946dd7
    ```
    """
    try:
        PolyaxonClients().job.resources(job)
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)


@job.command()
@click.argument('job', type=str)
def logs(job):
    """Get job logs.

    Examples:
    ```
    polyaxon job logs 50c62372137940ca8c456d8596946dd7
    ```
    """
    try:
        PolyaxonClients().job.logs(job)
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)
