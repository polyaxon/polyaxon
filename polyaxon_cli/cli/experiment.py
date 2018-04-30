# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import sys

from collections import deque

import click

from polyaxon_cli.cli.project import get_project_or_local
from polyaxon_cli.cli.upload import upload
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.experiment import ExperimentManager
from polyaxon_cli.managers.project import ProjectManager
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import (
    Printer,
    dict_tabulate,
    get_meta_response,
    get_resources,
    list_dicts_to_tabulate
)
from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError
from polyaxon_schemas.polyaxonfile import reader


def get_experiment_or_local(project=None, experiment=None):  # pylint:disable=redefined-outer-name
    user, project_name = get_project_or_local(project)
    experiment = experiment or ExperimentManager.get_config_or_raise().sequence
    return user, project_name, experiment


def get_experiment_details(experiment):  # pylint:disable=redefined-outer-name
    if experiment.description:
        Printer.print_header("Experiment description:")
        click.echo('{}\n'.format(experiment.description))

    if experiment.resources:
        get_resources(experiment.resources.to_dict(), header="Experiment resources:")

    if experiment.declarations:
        Printer.print_header("Experiment declarations:")
        dict_tabulate(experiment.declarations)

    if experiment.last_metric:
        Printer.print_header("Experiment last metrics:")
        dict_tabulate(experiment.last_metric)

    response = experiment.to_light_dict(
        humanize_values=True,
        exclude_attrs=[
            'uuid', 'config', 'project', 'experiments', 'description',
            'declarations', 'last_metric', 'resources', 'jobs'
        ])

    Printer.print_header("Experiment info:")
    dict_tabulate(Printer.add_status_color(response))


@click.group()
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'.")
@click.option('--experiment', '-xp', type=int, help="The experiment sequence number.")
@click.pass_context
@clean_outputs
def experiment(ctx, project, experiment):  # pylint:disable=redefined-outer-name
    """Commands for experiments."""
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project
    ctx.obj['experiment'] = experiment


@experiment.command()
@click.pass_context
@clean_outputs
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
    user, project_name, _experiment = get_experiment_or_local(ctx.obj['project'],
                                                              ctx.obj['experiment'])
    try:
        response = PolyaxonClients().experiment.get_experiment(user, project_name, _experiment)
        # Set caching only if we have an initialized project
        if ProjectManager.is_initialized():
            ExperimentManager.set_config(response)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not load experiment `{}` info.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    get_experiment_details(response)


@experiment.command()
@click.pass_context
@clean_outputs
def delete(ctx):
    """Delete experiment.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon experiment delete
    ```
    """
    user, project_name, _experiment = get_experiment_or_local(ctx.obj['project'],
                                                              ctx.obj['experiment'])
    if not click.confirm("Are sure you want to delete experiment `{}`".format(_experiment)):
        click.echo('Existing without deleting experiment.')
        sys.exit(1)

    try:
        response = PolyaxonClients().experiment.delete_experiment(
            user, project_name, _experiment)
        # Purge caching
        ExperimentManager.purge()
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not delete experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Experiment `{}` was delete successfully".format(_experiment))


@experiment.command()
@click.option('--yes', '-y', is_flag=True, default=False,
              help='Automatic yes to prompts. '
                   'Assume "yes" as answer to all prompts and run non-interactively.')
@click.pass_context
@clean_outputs
def stop(ctx, yes):
    """Stop experiment.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment stop
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 2 stop
    ```
    """
    user, project_name, _experiment = get_experiment_or_local(ctx.obj['project'],
                                                              ctx.obj['experiment'])
    if not yes and not click.confirm("Are sure you want to stop "
                                     "experiment `{}`".format(_experiment)):
        click.echo('Existing without stopping experiment.')
        sys.exit(0)

    try:
        PolyaxonClients().experiment.stop(user, project_name, _experiment)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not stop experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiment is being stopped.")


@experiment.command()
@click.option('--copy', '-c', is_flag=True, default=False,
              help='To copy the experiment before restarting.')
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help='The polyaxon files to update with.')
@click.option('-u', is_flag=True, default=False,
              help='To upload the repo before restarting.')
@click.pass_context
@clean_outputs
def restart(ctx, copy, file, u):  # pylint:disable=redefined-builtin
    """Restart experiment.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment --experiment=1 restart
    ```
    """
    config = None
    update_code = None
    if file:
        config = reader.read(file)

    # Check if we need to upload
    if u:
        ctx.invoke(upload, async=False)
        update_code = True

    user, project_name, _experiment = get_experiment_or_local(ctx.obj['project'],
                                                              ctx.obj['experiment'])
    try:
        if copy:
            response = PolyaxonClients().experiment.copy(
                user, project_name, _experiment, config=config, update_code=update_code)
        else:
            response = PolyaxonClients().experiment.restart(
                user, project_name, _experiment, config=config, update_code=update_code)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not restart experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    get_experiment_details(response)


@experiment.command()
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help='The polyaxon files to update with.')
@click.option('-u', is_flag=True, default=False,
              help='To upload the repo before resuming.')
@click.pass_context
@clean_outputs
def resume(ctx, file, u):  # pylint:disable=redefined-builtin
    """Resume experiment.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment --experiment=1 resume
    ```
    """
    config = None
    update_code = None
    if file:
        config = reader.read(file)

    # Check if we need to upload
    if u:
        ctx.invoke(upload, async=False)
        update_code = True

    user, project_name, _experiment = get_experiment_or_local(ctx.obj['project'],
                                                              ctx.obj['experiment'])
    try:
        response = PolyaxonClients().experiment.resume(
            user, project_name, _experiment, config=config, update_code=update_code)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not resume experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    get_experiment_details(response)


@experiment.command()
@click.option('--page', type=int, help='To paginate through the list of jobs.')
@click.pass_context
@clean_outputs
def jobs(ctx, page):
    """List jobs for experiment.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment --experiment=1 jobs
    ```
    """
    user, project_name, _experiment = get_experiment_or_local(ctx.obj['project'],
                                                              ctx.obj['experiment'])
    page = page or 1
    try:
        response = PolyaxonClients().experiment.list_jobs(
            user, project_name, _experiment, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get jobs for experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Jobs for experiment `{}`.'.format(_experiment))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No jobs found for experiment `{}`.'.format(_experiment))

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
@clean_outputs
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
    user, project_name, _experiment = get_experiment_or_local(ctx.obj['project'],
                                                              ctx.obj['experiment'])
    page = page or 1
    try:
        response = PolyaxonClients().experiment.get_statuses(
            user, project_name, _experiment, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could get status for experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Statuses for experiment `{}`.'.format(_experiment))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No statuses found for experiment `{}`.'.format(_experiment))

    objects = list_dicts_to_tabulate([Printer.handle_statuses(o.to_light_dict(humanize_values=True))
                                      for o in response['results']])
    if objects:
        Printer.print_header("Statuses:")
        objects.pop('experiment', None)
        dict_tabulate(objects, is_list_dict=True)


@experiment.command()
@click.option('--gpu', '-g', is_flag=True, help='List experiment GPU resources.')
@click.pass_context
@clean_outputs
def resources(ctx, gpu):
    """Get experiment resources.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon experiment -xp 19 resources
    ```

    For GPU resources

    \b
    ```bash
    $ polyaxon experiment -xp 19 resources --gpu
    ```
    """
    user, project_name, _experiment = get_experiment_or_local(ctx.obj['project'],
                                                              ctx.obj['experiment'])
    try:
        message_handler = Printer.gpu_resources if gpu else Printer.resources
        PolyaxonClients().experiment.resources(
            user, project_name, _experiment, message_handler=message_handler)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get resources for experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


@experiment.command()
@click.option('--past', is_flag=True, help='Show the past logs.')
@click.option('--follow', is_flag=True, default=False, help='Stream logs after showing past logs.')
@click.pass_context
@clean_outputs
def logs(ctx, past, follow):
    """Get experiment logs.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment logs
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 10 -p mnist logs
    ```
    """
    user, project_name, _experiment = get_experiment_or_local(ctx.obj['project'],
                                                              ctx.obj['experiment'])
    colors = deque(Printer.COLORS)
    job_to_color = {}
    sign = {'current': '-', 'values': ['-', '|']}

    def handle_docker_progress(status, log_line):  # pylint:disable=unused-variable
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
            Printer.log("{} -- your job's image is being created.".format(status))

    def message_handler(message):
        status = message['status']
        log_line = message['log_line']
        if status == 'Running':
            job_info = '{}.{}'.format(message['task_type'], int(message['task_idx']) + 1)
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

    if past:
        try:
            response = PolyaxonClients().experiment.logs(
                user, project_name, _experiment, stream=False)
            for log_line in response.content.decode().split('\n'):
                Printer.log(log_line)
                print()

            if not follow:
                return
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not get logs for experiment `{}`.'.format(_experiment))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    try:
        PolyaxonClients().experiment.logs(
            user, project_name, _experiment, message_handler=message_handler)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get logs for experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


@experiment.command()
@clean_outputs
def outputs(ctx):
    pass
