# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from collections import deque

import click

from polyaxon_cli.cli.project import get_project_or_local
from polyaxon_cli.cli.upload import upload
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.experiment import ExperimentManager
from polyaxon_cli.managers.experiment_job import ExperimentJobManager
from polyaxon_cli.utils import cache
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
from polyaxon_schemas.utils import to_list


def get_experiment_or_local(_experiment=None):
    return _experiment or ExperimentManager.get_config_or_raise().id


def get_project_experiment_or_local(_project=None, _experiment=None):
    user, project_name = get_project_or_local(_project)
    _experiment = get_experiment_or_local(_experiment)
    return user, project_name, _experiment


def get_experiment_job_or_local(_job=None):
    return _job or ExperimentJobManager.get_config_or_raise().id


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
@click.option('--experiment', '-xp', type=int, help="The experiment id number.")
@click.pass_context
@clean_outputs
def experiment(ctx, project, experiment):  # pylint:disable=redefined-outer-name
    """Commands for experiments."""
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project
    ctx.obj['experiment'] = experiment


@experiment.command()
@click.option('--job', '-j', type=int, help="The job id.")
@click.pass_context
@clean_outputs
def get(ctx, job):
    """Get experiment or experiment job.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples for getting an experiment:

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

    Examples for getting an experiment job:

    \b
    ```bash
    $ polyaxon experiment get -j 1  # if experiment is cached
    ```

    \b
    ```bash
    $ polyaxon experiment --experiment=1 get --job=10
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 --project=cats-vs-dogs get -j 2
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 -p alain/cats-vs-dogs get -j 2
    ```
    """

    def get_experiment():
        try:
            response = PolyaxonClients().experiment.get_experiment(user, project_name, _experiment)
            cache.cache(config_manager=ExperimentManager, response=response)
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not load experiment `{}` info.'.format(_experiment))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

        get_experiment_details(response)

    def get_experiment_job():
        try:
            response = PolyaxonClients().experiment_job.get_job(user,
                                                                project_name,
                                                                _experiment,
                                                                _job)
            cache.cache(config_manager=ExperimentJobManager, response=response)
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not get job `{}`.'.format(_job))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

        if response.resources:
            get_resources(response.resources.to_dict(), header="Job resources:")

        response = Printer.add_status_color(response.to_light_dict(
            humanize_values=True,
            exclude_attrs=['uuid', 'definition', 'experiment', 'unique_name', 'resources']
        ))
        Printer.print_header("Job info:")
        dict_tabulate(response)

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj['project'],
                                                                      ctx.obj['experiment'])

    if job:
        _job = get_experiment_job_or_local(job)
        get_experiment_job()
    else:
        get_experiment()


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
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj['project'],
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
@click.option('--name', type=str,
              help='Name of the experiment, must be unique within the project, could be none.')
@click.option('--description', type=str, help='Description of the experiment.')
@click.option('--tags', type=str, help='Tags of the experiment, comma separated values.')
@click.pass_context
@clean_outputs
def update(ctx, name, description, tags):
    """Update experiment.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment -xp 2 update --description="new description for my experiments"
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 2 update --tags="foo, bar" --name="unique-name"
    ```
    """
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj['project'],
                                                                      ctx.obj['experiment'])
    update_dict = {}

    if name:
        update_dict['name'] = name

    if description:
        update_dict['description'] = description

    if tags:
        update_dict['tags'] = tags.split(',')

    if not update_dict:
        Printer.print_warning('No argument was provided to update the experiment.')
        sys.exit(0)

    try:
        response = PolyaxonClients().experiment.update_experiment(
            user, project_name, _experiment, update_dict)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not update experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiment updated.")
    get_experiment_details(response)


@experiment.command()
@click.option('--yes', '-y', is_flag=True, default=False,
              help="Automatic yes to prompts. "
                   "Assume \"yes\" as answer to all prompts and run non-interactively.")
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
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj['project'],
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
              help="To copy the experiment before restarting.")
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help="The polyaxon files to update with.")
@click.option('-u', is_flag=True, default=False,
              help="To upload the repo before restarting.")
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

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj['project'],
                                                                      ctx.obj['experiment'])
    try:
        if copy:
            response = PolyaxonClients().experiment.copy(
                user, project_name, _experiment, config=config, update_code=update_code)
            Printer.print_success('Experiment was copied with id {}'.format(response.id))
        else:
            response = PolyaxonClients().experiment.restart(
                user, project_name, _experiment, config=config, update_code=update_code)
            Printer.print_success('Experiment was restarted with id {}'.format(response.id))
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not restart experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


@experiment.command()
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help="The polyaxon files to update with.")
@click.option('-u', is_flag=True, default=False,
              help="To upload the repo before resuming.")
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

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj['project'],
                                                                      ctx.obj['experiment'])
    try:
        response = PolyaxonClients().experiment.resume(
            user, project_name, _experiment, config=config, update_code=update_code)
        Printer.print_success('Experiment was resumed with id {}'.format(response.id))
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not resume experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


@experiment.command()
@click.option('--page', type=int, help="To paginate through the list of jobs.")
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
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj['project'],
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
@click.option('--job', '-j', type=int, help="The job id.")
@click.option('--page', type=int, help="To paginate through the list of statuses.")
@click.pass_context
@clean_outputs
def statuses(ctx, job, page):
    """Get experiment or experiment job statuses.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples getting experiment statuses:

    \b
    ```bash
    $ polyaxon experiment statuses
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 statuses
    ```

    Examples getting experiment job statuses:

    \b
    ```bash
    $ polyaxon experiment statuses -j 3
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 statuses --job 1
    ```
    """

    def get_experiment_statuses():
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

        objects = list_dicts_to_tabulate(
            [Printer.add_status_color(o.to_light_dict(humanize_values=True), status_key='status')
             for o in response['results']])
        if objects:
            Printer.print_header("Statuses:")
            objects.pop('experiment', None)
            dict_tabulate(objects, is_list_dict=True)

    def get_experiment_job_statuses():
        try:
            response = PolyaxonClients().experiment_job.get_statuses(user,
                                                                     project_name,
                                                                     _experiment,
                                                                     _job,
                                                                     page=page)
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not get status for job `{}`.'.format(job))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

        meta = get_meta_response(response)
        if meta:
            Printer.print_header('Statuses for Job `{}`.'.format(_job))
            Printer.print_header('Navigation:')
            dict_tabulate(meta)
        else:
            Printer.print_header('No statuses found for job `{}`.'.format(_job))

        objects = list_dicts_to_tabulate(
            [Printer.add_status_color(o.to_light_dict(humanize_values=True), status_key='status')
             for o in response['results']])
        if objects:
            Printer.print_header("Statuses:")
            objects.pop('job', None)
            dict_tabulate(objects, is_list_dict=True)

    page = page or 1

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj['project'],
                                                                      ctx.obj['experiment'])

    if job:
        _job = get_experiment_job_or_local(job)
        get_experiment_job_statuses()
    else:
        get_experiment_statuses()


@experiment.command()
@click.option('--job', '-j', type=int, help="The job id.")
@click.option('--gpu', '-g', is_flag=True, help="List experiment GPU resources.")
@click.pass_context
@clean_outputs
def resources(ctx, job, gpu):
    """Get experiment or experiment job resources.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples for getting experiment resources:

    \b
    ```bash
    $ polyaxon experiment -xp 19 resources
    ```

    For GPU resources

    \b
    ```bash
    $ polyaxon experiment -xp 19 resources --gpu
    ```

    Examples for getting experiment job resources:

    \b
    ```bash
    $ polyaxon experiment -xp 19 resources -j 1
    ```

    For GPU resources

    \b
    ```bash
    $ polyaxon experiment -xp 19 resources -j 1 --gpu
    ```
    """

    def get_experiment_resources():
        try:
            message_handler = Printer.gpu_resources if gpu else Printer.resources
            PolyaxonClients().experiment.resources(
                user, project_name, _experiment, message_handler=message_handler)
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not get resources for experiment `{}`.'.format(_experiment))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    def get_experiment_job_resources():
        try:
            message_handler = Printer.gpu_resources if gpu else Printer.resources
            PolyaxonClients().experiment_job.resources(user,
                                                       project_name,
                                                       _experiment,
                                                       _job,
                                                       message_handler=message_handler)
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not get resources for job `{}`.'.format(_job))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj['project'],
                                                                      ctx.obj['experiment'])

    if job:
        _job = get_experiment_job_or_local(job)
        get_experiment_job_resources()
    else:
        get_experiment_resources()


@experiment.command()
@click.option('--job', '-j', type=int, help="The job id.")
@click.option('--past', '-p', is_flag=True, help="Show the past logs.")
@click.option('--follow', '-f', is_flag=True, default=False,
              help="Stream logs after showing past logs.")
@click.pass_context
@clean_outputs
def logs(ctx, job, past, follow):
    """Get experiment or experiment job logs.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples for getting experiment logs:

    \b
    ```bash
    $ polyaxon experiment logs
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 10 -p mnist logs
    ```

    Examples for getting experiment job logs:

    \b
    ```bash
    $ polyaxon experiment -xp 1 -j 1 logs
    ```
    """

    def get_experiment_logs():
        colors = deque(Printer.COLORS)
        job_to_color = {}
        sign = {'current': '-', 'values': ['-', '|']}

        def message_handler(message):
            status = message['status']
            log_lines = to_list(message['log_lines'])
            if status == 'running':
                job_info = '{}.{}'.format(message['task_type'], int(message['task_idx']) + 1)
                if job_info in job_to_color:
                    color = job_to_color[job_info]
                else:
                    color = colors[0]
                    colors.rotate(-1)
                    job_to_color[job_info] = color

                for log_line in log_lines:
                    log_line = '{} -- {}'.format(Printer.add_color(job_info, color), log_line)
                    Printer.log(log_line, nl=True)
            elif status == 'building':
                sign['current'] = (sign['values'][0]
                                   if sign['current'] == sign['values'][1]
                                   else sign['values'][1])
                status = Printer.add_color(status, 'yellow')
                Printer.log("{} -- creating image {}\r".format(status, sign['current']))
                sys.stdout.flush()
            else:
                for log_line in log_lines:
                    Printer.log('{} -- {}'.format(status, log_line), nl=True)

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

    def get_experiment_job_logs():
        def message_handler(message):
            log_lines = to_list(message['log_lines'])
            for log_line in log_lines:
                Printer.log(log_line, nl=True)

        try:
            PolyaxonClients().experiment_job.logs(user,
                                                  project_name,
                                                  _experiment,
                                                  _job,
                                                  message_handler=message_handler)
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not get logs for job `{}`.'.format(_job))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj['project'],
                                                                      ctx.obj['experiment'])

    if job:
        _job = get_experiment_job_or_local(job)
        get_experiment_job_logs()
    else:
        get_experiment_logs()


@experiment.command()
@click.pass_context
@clean_outputs
def outputs(ctx):
    """Download outputs for experiment.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment -xp 1 outputs
    ```
    """
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj['project'],
                                                                      ctx.obj['experiment'])
    try:
        PolyaxonClients().experiment.download_outputs(user, project_name, _experiment)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not download outputs for experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
    Printer.print_success('Files downloaded.')


@experiment.command()
@click.pass_context
@clean_outputs
def bookmark(ctx):
    """Bookmark experiment.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment bookmark
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 2 bookmark
    ```
    """
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj['project'],
                                                                      ctx.obj['experiment'])
    try:
        PolyaxonClients().experiment.bookmark(user, project_name, _experiment)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not bookmark experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiment is bookmarked.")


@experiment.command()
@click.pass_context
@clean_outputs
def unbookmark(ctx):
    """Unbookmark experiment.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment unbookmark
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 2 unbookmark
    ```
    """
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj['project'],
                                                                      ctx.obj['experiment'])
    try:
        PolyaxonClients().experiment.unbookmark(user, project_name, _experiment)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not unbookmark experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiment is unbookmarked.")
