# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json

import click
import sys

from collections import deque

from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError

from polyaxon_cli.cli.project import get_project_or_local
from polyaxon_cli.managers.experiment import ExperimentManager
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import (
    Printer,
    dict_tabulate,
    get_meta_response,
    list_dicts_to_tabulate,
)


def get_experiment_or_local(experiment=None):
    return experiment or ExperimentManager.get_config_or_raise().sequence


@click.group()
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'.")
@click.option('--experiment', '-xp', type=int, help="The experiment sequence number.")
@click.pass_context
def experiment(ctx, project, experiment):
    """Commands for experiments."""
    user, project_name = get_project_or_local(project)
    experiment = get_experiment_or_local(experiment)
    ctx.obj = ctx.obj or {}
    ctx.obj['user'] = user
    ctx.obj['project_name'] = project_name
    ctx.obj['experiment'] = experiment


@experiment.command()
@click.pass_context
def get(ctx):
    """Get experiment.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon experiment get  # if experiment is cached
    ```

    \b
    ```bash
    $ polyaxon experiment --experiment=1 get
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 --project=cats-vs-dogs get
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 -p alain/cats-vs-dogs get
    ```
    """
    user, project_name, experiment = ctx.obj['user'], ctx.obj['project_name'], ctx.obj['experiment']
    try:
        response = PolyaxonClients().experiment.get_experiment(user, project_name, experiment)
        # Set caching
        ExperimentManager.set_config(response)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not load experiment `{}` info.'.format(experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    response = Printer.add_status_color(response.to_light_dict(humanize_values=True))
    Printer.print_header("Experiment info:")
    dict_tabulate(response)


@experiment.command()
@click.pass_context
def delete(ctx):
    """Delete experiment.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon experiment delete
    ```
    """
    user, project_name, experiment = ctx.obj['user'], ctx.obj['project_name'], ctx.obj['experiment']
    if not click.confirm("Are sure you want to delete experiment `{}`".format(experiment)):
        click.echo('Existing without deleting experiment.')
        sys.exit(1)

    try:
        response = PolyaxonClients().experiment.delete_experiment(
            user, project_name, experiment)
        # Purge caching
        ExperimentManager.purge()
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not delete experiment `{}`.'.format(experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Experiment `{}` was delete successfully".format(experiment))


@experiment.command()
@click.pass_context
def stop(ctx):
    """Stop experiment.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment stop
    ```

    \b
    ```bash
    $ polyaxon experiment -x 2 stop
    ```
    """
    user, project_name, experiment = ctx.obj['user'], ctx.obj['project_name'], ctx.obj['experiment']
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
@click.pass_context
def restart(ctx):
    """Restart experiment.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment --experiment=1 restart
    ```
    """
    user, project_name, experiment = ctx.obj['user'], ctx.obj['project_name'], ctx.obj['experiment']
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
@click.option('--page', type=int, help='To paginate through the list of jobs.')
@click.pass_context
def jobs(ctx, page):
    """List jobs for experiment.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment --experiment=1 jobs
    ```
    """
    user, project_name, experiment = ctx.obj['user'], ctx.obj['project_name'], ctx.obj['experiment']
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
@click.option('--page', type=int, help='To paginate through the list of statuses.')
@click.pass_context
def statuses(ctx, page):
    """Get experiment status.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon experiment statuses 3
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 statuses
    ```
    """
    user, project_name, experiment = ctx.obj['user'], ctx.obj['project_name'], ctx.obj['experiment']
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
@click.pass_context
def resources(ctx):
    """Get experiment resources.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon experiment -xp 19 resources
    ```
    """
    user, project_name, experiment = ctx.obj['user'], ctx.obj['project_name'], ctx.obj['experiment']
    try:
        PolyaxonClients().experiment.resources(
            user, project_name, experiment, message_handler=Printer.resources)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get resources for experiment `{}`.'.format(experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


@experiment.command()
@click.pass_context
def logs(ctx):
    """Get experiment logs.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment logs
    ```

    \b
    ```bash
    $ polyaxon experiment -x 10 -p mnist logs
    ```
    """
    user, project_name, experiment = ctx.obj['user'], ctx.obj['project_name'], ctx.obj['experiment']
    colors = deque(Printer.COLORS)
    job_to_color = {}
    sign = {'current': '-', 'values': ['-', '|']}

    def handle_docker_progress(status, log_line):
        try:
            log_line = json.loads(log_line)
            if log_line.get('id') and log_line.get('progress'):
                log_line = '{} -- container: {}, progress: {}\r'.format(
                    status,
                    log_line['id'],
                    log_line['progress'])
                Printer.log(log_line)
                sys.stdout.flush()
        except json.JSONDecodeError:
            click.echo('--')
            Printer.log("{} -- your job's image is being created.".format(status, log_line))

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
            sign['current'] = (sign['values'][0]
                               if sign['current'] == sign['values'][1]
                               else sign['values'][1])
            status = Printer.add_color(status, 'yellow')
            Printer.log("{} -- creating image {}\r".format(status, sign['current']))
            sys.stdout.flush()
        else:
            Printer.log('{} -- {}'.format(status, log_line))

    try:
        PolyaxonClients().experiment.logs(
            user, project_name, experiment, message_handler=message_handler)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get logs for experiment `{}`.'.format(experiment))
        sys.exit(1)


@experiment.command()
def outputs(ctx):
    pass
