# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json

import click
import sys

from collections import deque

from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError

from polyaxon_cli.cli.project import get_project_or_local
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
@click.argument('experiment', type=int)
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'")
def get(experiment, project):
    """Get experiment by uuid.

    Examples:
    ```
    polyaxon experiment get 1
    ```

    ```
    polyaxon experiment get 1 --project=cats-vs-dogs
    ```

     ```
    polyaxon experiment get 1 --project=alain/cats-vs-dogs
    ```
    """
    user, project_name = get_project_or_local(project)
    try:
        response = PolyaxonClients().experiment.get_experiment(user, project_name, experiment)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not load experiment `{}` info.'.format(experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    response = Printer.add_status_color(response.to_light_dict(humanize_values=True))
    Printer.print_header("Experiment info:")
    dict_tabulate(response)


@experiment.command()
@click.argument('experiment', type=int)
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'")
def delete(experiment, project):
    """Delete experiment group."""
    user, project_name = get_project_or_local(project)
    if not click.confirm("Are sure you want to delete experiment `{}`".format(experiment)):
        click.echo('Existing without deleting experiment.')
        sys.exit(1)

    try:
        response = PolyaxonClients().experiment.delete_experiment(
            user, project_name, experiment)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not delete experiment `{}`.'.format(experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Experiment `{}` was delete successfully".format(experiment))


@experiment.command()
@click.argument('experiment', type=int)
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'")
def stop(experiment, project):
    """Get experiment by uuid.

    Examples:
    ```
    polyaxon experiment stop 2
    ```
    """
    user, project_name = get_project_or_local(project)
    if not click.confirm("Are sure you want to stop experiment `{}`".format(experiment)):
        click.echo('Existing without stopping experiment.')
        sys.exit(0)

    try:
        PolyaxonClients().experiment.stop(user, project_name, experiment)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not stop experiment `{}`.'.format(experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiment is being stopped.")


@experiment.command()
@click.argument('experiment', type=int)
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'")
def restart(experiment, project):
    """Delete experiment."""
    user, project_name = get_project_or_local(project)
    try:
        response = PolyaxonClients().experiment.restart(
            user, project_name, experiment)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not restart experiment `{}`.'.format(experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    response = Printer.add_status_color(response.to_light_dict(humanized_values=True))
    Printer.print_header("Experiment info:")
    dict_tabulate(response)


@experiment.command()
@click.argument('experiment', type=int)
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'")
@click.option('--page', type=int, help='To paginate through the list of experiments.')
def jobs(experiment, project, page):
    """List jobs for this experiment"""
    user, project_name = get_project_or_local(project)
    page = page or 1
    try:
        response = PolyaxonClients().experiment.list_jobs(user, project_name, experiment, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get jobs for experiment `{}`.'.format(experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Jobs for experiment `{}`.'.format(experiment))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No jobs found for experiment `{}`.'.format(experiment))

    objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
               for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Jobs:")
        objects.pop('experiment', None)
        dict_tabulate(objects, is_list_dict=True)


@experiment.command()
@click.argument('experiment', type=int)
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'")
@click.option('--page', type=int, help='To paginate through the list of experiments.')
def statuses(experiment, project, page):
    """Get experiment status.

    Examples:
    ```
    polyaxon experiment statuses 3
    ```
    """
    user, project_name = get_project_or_local(project)
    page = page or 1
    try:
        response = PolyaxonClients().experiment.get_statuses(
            user, project_name, experiment, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could get status for experiment `{}`.'.format(experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Statuses for experiment `{}`.'.format(experiment))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No statuses found for experiment `{}`.'.format(experiment))

    objects = list_dicts_to_tabulate([Printer.handle_statuses(o.to_light_dict(humanize_values=True))
                                      for o in response['results']])
    if objects:
        Printer.print_header("Statuses:")
        objects.pop('experiment', None)
        dict_tabulate(objects, is_list_dict=True)


@experiment.command()
@click.argument('experiment', type=int)
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'")
def resources(experiment, project):
    """Get experiment resources.

    Examples:
    ```
    polyaxon experiment resources 19
    ```
    """
    user, project_name = get_project_or_local(project)
    try:
        PolyaxonClients().experiment.resources(
            user, project_name, experiment, message_handler=Printer.resources)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get resources for experiment `{}`.'.format(experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


@experiment.command()
@click.argument('experiment', type=int)
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'")
def logs(experiment, project):
    """Get experiment logs.

    Examples:
    ```
    polyaxon experiment logs 1
    ```
    """
    user, project_name = get_project_or_local(project)
    colors = deque(Printer.COLORS)
    job_to_color = {}

    def message_handler(message):
        status = message['status']
        log_line = message['log_line']
        if status == 'Running':
            job_info = '{}.{}'.format(message['task_type'], message['job_uuid'])
            if job_info in job_to_color:
                color = job_to_color[job_info]
            else:
                color = colors[0]
                colors.rotate(-1)
                job_to_color[job_info] = color

            log_line = '{} -- {}'.format(Printer.add_color(job_info, color), message['log_line'])
            Printer.log(log_line)
        elif status == 'Building':
            status = Printer.add_color(status, 'yellow')
            try:
                log_line = json.loads(log_line)
                if log_line.get('id') and log_line.get('progress'):
                    log_line = '{} -- container: {}, progress: {}\r'.format(
                        status,
                        log_line['id'],
                        log_line['progress'])
                    Printer.log(log_line)
                    sys.stdout.flush()
                else:
                    click.echo('--')
                    Printer.log('{} -- {}'.format(status, log_line))
            except json.JSONDecodeError:
                click.echo('--')
                Printer.log('{} -- {}'.format(status, log_line))
        else:
            Printer.log('{} -- {}'.format(status, log_line))
    try:
        PolyaxonClients().experiment.logs(
            user, project_name, experiment, message_handler=message_handler)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get logs for experiment `{}`.'.format(experiment))
        sys.exit(1)


@experiment.command()
@click.argument('experiment', type=int)
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'")
def outputs(experiment, project):
    pass
