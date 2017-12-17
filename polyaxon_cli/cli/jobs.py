# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys

from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError

from polyaxon_cli.cli.project import get_project_or_local
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import (
    Printer,
    dict_tabulate,
    get_meta_response, list_dicts_to_tabulate)


@click.group()
def job():
    """Commands for jobs."""
    pass


@job.command()
@click.argument('experiment', type=int)
@click.argument('job', type=str)
@click.option('--project', '-p', type=str)
def get(experiment, job, project):
    """Get job by uuid.

    Examples:
    ```
    polyaxon job get 50c62372137940ca8c456d8596946dd7
    ```
    """
    user, project_name = get_project_or_local(project)
    try:
        response = PolyaxonClients().job.get_job(user, project_name, experiment, job)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get job `{}`.'.format(job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    response = response.to_dict()
    Printer.print_header("Job info:")
    dict_tabulate(response)


@job.command()
@click.argument('experiment', type=int)
@click.argument('job', type=str)
@click.option('--project', '-p', type=str)
def statuses(experiment, job, project):
    """Get job status.

    Examples:
    ```
    polyaxon job status 50c62372137940ca8c456d8596946dd7
    ```
    """
    user, project_name = get_project_or_local(project)
    try:
        response = PolyaxonClients().job.get_statuses(user, project_name, experiment, job)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get status for job `{}`.'.format(job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Statuses for Job `{}`.'.format(job))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No statuses found for job `{}`.'.format(job))

    objects = list_dicts_to_tabulate([o.to_dict() for o in response['results']])
    if objects:
        Printer.print_header("Statuses:")
        objects.pop('job')
        dict_tabulate(objects, is_list_dict=True)


@job.command()
@click.argument('experiment', type=int)
@click.argument('job', type=str)
@click.option('--project', '-p', type=str)
def resources(experiment, job, project):
    """Get job resources.

    Examples:
    ```
    polyaxon job resources 50c62372137940ca8c456d8596946dd7
    ```
    """
    user, project_name = get_project_or_local(project)
    try:
        PolyaxonClients().job.resources(user,
                                        project_name,
                                        experiment,
                                        job,
                                        message_handler=lambda x: click.echo)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get resources for job `{}`.'.format(job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


@job.command()
@click.argument('experiment', type=int)
@click.argument('job', type=str)
@click.option('--project', '-p', type=str)
def logs(experiment, job, project):
    """Get job logs.

    Examples:
    ```
    polyaxon job logs 50c62372137940ca8c456d8596946dd7
    ```
    """
    user, project_name = get_project_or_local(project)
    try:
        PolyaxonClients().job.logs(user,
                                   project_name,
                                   experiment,
                                   job,
                                   message_handler=click.echo)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get logs for job `{}`.'.format(job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
