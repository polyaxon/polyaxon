# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_cli.cli.project import get_project_or_local
from polyaxon_cli.cli.upload import upload
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.job import JobManager
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


def get_job_or_local(project=None, _job=None):
    user, project_name = get_project_or_local(project)
    _job = _job or JobManager.get_config_or_raise().id
    return user, project_name, _job


def get_job_details(_job):
    if _job.description:
        Printer.print_header("Job description:")
        click.echo('{}\n'.format(_job.description))

    if _job.resources:
        get_resources(_job.resources.to_dict(), header="Job resources:")

    response = _job.to_light_dict(
        humanize_values=True,
        exclude_attrs=[
            'uuid', 'config', 'project', 'description', 'resources',
        ])

    Printer.print_header("Job info:")
    dict_tabulate(Printer.add_status_color(response))


@click.group()
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'")
@click.option('--job', '-j', type=int, help="The job id.")
@click.pass_context
@clean_outputs
def job(ctx, project, job):  # pylint:disable=redefined-outer-name
    """Commands for jobs."""
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project
    ctx.obj['job'] = job


@job.command()
@click.pass_context
@clean_outputs
def get(ctx):
    """Get job.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon job --job=1 get
    ```

    \b
    ```bash
    $ polyaxon job --job=1 --project=project_name get
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    try:
        response = PolyaxonClients().job.get_job(user, project_name, _job)
        cache.cache(config_manager=JobManager, response=response)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    get_job_details(response)


@job.command()
@click.pass_context
@clean_outputs
def delete(ctx):
    """Delete job.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon job delete
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    if not click.confirm("Are sure you want to delete job `{}`".format(_job)):
        click.echo('Existing without deleting job.')
        sys.exit(1)

    try:
        response = PolyaxonClients().job.delete_job(
            user, project_name, _job)
        # Purge caching
        JobManager.purge()
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not delete job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Job `{}` was delete successfully".format(_job))


@job.command()
@click.option('--name', type=str,
              help='Name of the job, must be unique within the project, could none.')
@click.option('--description', type=str, help='Description of the job.')
@click.option('--tags', type=str, help='Tags of the job, comma separated values.')
@click.pass_context
@clean_outputs
def update(ctx, name, description, tags):
    """Update job.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon job -j 2 update --description="new description for my job"
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    update_dict = {}

    if name:
        update_dict['name'] = name

    if description:
        update_dict['description'] = description

    if tags:
        update_dict['tags'] = tags.split(',')

    if not update_dict:
        Printer.print_warning('No argument was provided to update the job.')
        sys.exit(0)

    try:
        response = PolyaxonClients().build_job.update_job(
            user, project_name, _job, update_dict)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not update job  `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Job updated.")
    get_job_details(response)


@job.command()
@click.option('--yes', '-y', is_flag=True, default=False,
              help="Automatic yes to prompts. "
                   "Assume \"yes\" as answer to all prompts and run non-interactively.")
@click.pass_context
@clean_outputs
def stop(ctx, yes):
    """Stop job.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon job stop
    ```

    \b
    ```bash
    $ polyaxon job -xp 2 stop
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    if not yes and not click.confirm("Are sure you want to stop "
                                     "job `{}`".format(_job)):
        click.echo('Existing without stopping job.')
        sys.exit(0)

    try:
        PolyaxonClients().job.stop(user, project_name, _job)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not stop job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Job is being stopped.")


@job.command()
@click.option('--copy', '-c', is_flag=True, default=False,
              help="To copy the job before restarting.")
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help="The polyaxon files to update with.")
@click.option('-u', is_flag=True, default=False,
              help="To upload the repo before restarting.")
@click.pass_context
@clean_outputs
def restart(ctx, copy, file, u):  # pylint:disable=redefined-builtin
    """Restart job.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon job --job=1 restart
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

    user, project_name, _job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    try:
        if copy:
            response = PolyaxonClients().job.copy(
                user, project_name, _job, config=config, update_code=update_code)
        else:
            response = PolyaxonClients().job.restart(
                user, project_name, _job, config=config, update_code=update_code)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not restart job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    get_job_details(response)


@job.command()
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help="The polyaxon files to update with.")
@click.option('-u', is_flag=True, default=False,
              help="To upload the repo before resuming.")
@click.pass_context
@clean_outputs
def resume(ctx, file, u):  # pylint:disable=redefined-builtin
    """Resume job.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon job --job=1 resume
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

    user, project_name, _job = get_job_or_local(ctx.obj['project'],
                                                ctx.obj['job'])
    try:
        response = PolyaxonClients().job.resume(
            user, project_name, _job, config=config, update_code=update_code)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not resume job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    get_job_details(response)


@job.command()
@click.option('--page', type=int, help="To paginate through the list of statuses.")
@click.pass_context
@clean_outputs
def statuses(ctx, page):
    """Get job statuses.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon job -j 2 statuses
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    page = page or 1
    try:
        response = PolyaxonClients().job.get_statuses(user, project_name, _job, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get status for job `{}`.'.format(_job))
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


@job.command()
@click.option('--gpu', '-g', is_flag=True, help='List job GPU resources.')
@click.pass_context
@clean_outputs
def resources(ctx, gpu):
    """Get job resources.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon job -j 2 resources
    ```

    For GPU resources

    \b
    ```bash
    $ polyaxon job -j 2 resources --gpu
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    try:
        message_handler = Printer.gpu_resources if gpu else Printer.resources
        PolyaxonClients().job.resources(user,
                                        project_name,
                                        _job,
                                        message_handler=message_handler)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get resources for job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


@job.command()
@click.option('--past', '-p', is_flag=True, help="Show the past logs.")
@click.option('--follow', '-f', is_flag=True, default=False,
              help="Stream logs after showing past logs.")
@click.pass_context
@clean_outputs
def logs(ctx, past, follow):
    """Get job logs.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon job -j 2 logs
    ```

    \b
    ```bash
    $ polyaxon job logs
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])

    def message_handler(message):
        log_lines = to_list(message['log_lines'])
        for log_line in log_lines:
            Printer.log(log_line, nl=True)

    if past:
        try:
            response = PolyaxonClients().job.logs(
                user, project_name, _job, stream=False)
            for log_line in response.content.decode().split('\n'):
                Printer.log(log_line, nl=True)

            if not follow:
                return
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not get logs for job `{}`.'.format(_job))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    try:
        PolyaxonClients().job.logs(user,
                                   project_name,
                                   _job,
                                   message_handler=message_handler)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get logs for job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


@job.command()
@click.pass_context
@clean_outputs
def outputs(ctx):
    """Download outputs for job.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon job -j 1 outputs
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    try:
        PolyaxonClients().job.download_outputs(user, project_name, _job)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not download outputs for job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
    Printer.print_success('Files downloaded.')


@job.command()
@click.pass_context
@clean_outputs
def bookmark(ctx):
    """Bookmark job.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon job bookmark
    ```

    \b
    ```bash
    $ polyaxon job -xp 2 bookmark
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    try:
        PolyaxonClients().job.bookmark(user, project_name, _job)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not bookmark job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Job is bookmarked.")


@job.command()
@click.pass_context
@clean_outputs
def unbookmark(ctx):
    """Unbookmark job.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon job unbookmark
    ```

    \b
    ```bash
    $ polyaxon job -xp 2 unbookmark
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    try:
        PolyaxonClients().job.unbookmark(user, project_name, _job)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not unbookmark job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Job is unbookmarked.")
