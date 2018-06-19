# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_cli.cli.project import get_project_or_local
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.build_job import BuildJobManager
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
from polyaxon_schemas.utils import to_list


def get_job_or_local(project=None, job=None):
    user, project_name = get_project_or_local(project)
    job = job or BuildJobManager.get_config_or_raise().id
    return user, project_name, job


def get_job_details(job):
    if job.description:
        Printer.print_header("Job description:")
        click.echo('{}\n'.format(job.description))

    if job.resources:
        get_resources(job.resources.to_dict(), header="Job resources:")

    response = job.to_light_dict(
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
def build(ctx, project, job):  # pylint:disable=redefined-outer-name
    """Commands for build jobs."""
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project
    ctx.obj['job'] = job


@build.command()
@click.pass_context
@clean_outputs
def get(ctx):
    """Get build job.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon build --job=1 get
    ```

    \b
    ```bash
    $ polyaxon build --job=1 --project=project_name get
    ```
    """
    user, project_name, job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    try:
        response = PolyaxonClients().build_job.get_job(user, project_name, job)
        # Set caching only if we have an initialized project
        if ProjectManager.is_initialized():
            BuildJobManager.set_config(response)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get build job `{}`.'.format(job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    get_job_details(response)


@build.command()
@click.pass_context
@clean_outputs
def delete(ctx):
    """Delete build job.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon build delete
    ```

    \b
    ```bash
    $ polyaxon build -j 2 delete
    ```
    """
    user, project_name, job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    if not click.confirm("Are sure you want to delete build job `{}`".format(job)):
        click.echo('Existing without deleting build job.')
        sys.exit(1)

    try:
        response = PolyaxonClients().build_job.delete_job(
            user, project_name, job)
        # Purge caching
        BuildJobManager.purge()
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not delete job `{}`.'.format(job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Experiment `{}` was delete successfully".format(job))


@build.command()
@click.option('--name', type=str,
              help='Name of the build, must be unique within the project, could none.')
@click.option('--description', type=str, help='Description of the build.')
@click.option('--tags', type=str, help='Tags of the build, comma separated values.')
@click.pass_context
@clean_outputs
def update(ctx, name, description, tags):
    """Update build.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Example:

    \b
    ```bash
    $ polyaxon build -j 2 update --description="new description for my build"
    ```
    """
    user, project_name, job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    update_dict = {}

    if name:
        update_dict['name'] = name

    if description:
        update_dict['description'] = description

    if tags:
        update_dict['tags'] = tags.split(',')

    if not update_dict:
        Printer.print_warning('No argument was provided to update the build.')
        sys.exit(0)

    try:
        response = PolyaxonClients().build_job.update_job(
            user, project_name, job, update_dict)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not update build `{}`.'.format(job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Build updated.")
    get_job_details(response)


@build.command()
@click.option('--yes', '-y', is_flag=True, default=False,
              help="Automatic yes to prompts. "
                   "Assume \"yes\" as answer to all prompts and run non-interactively.")
@click.pass_context
@clean_outputs
def stop(ctx, yes):
    """Stop build job.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon build stop
    ```

    \b
    ```bash
    $ polyaxon build -j 2 stop
    ```
    """
    user, project_name, job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    if not yes and not click.confirm("Are sure you want to stop "
                                     "job `{}`".format(job)):
        click.echo('Existing without stopping build job.')
        sys.exit(0)

    try:
        PolyaxonClients().build_job.stop(user, project_name, job)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not stop build job `{}`.'.format(job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Build job is being stopped.")


@build.command()
@click.option('--page', type=int, help="To paginate through the list of statuses.")
@click.pass_context
@clean_outputs
def statuses(ctx, page):
    """Get build job status.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon build -j 2 statuses
    ```
    """
    user, project_name, job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    page = page or 1
    try:
        response = PolyaxonClients().build_job.get_statuses(user, project_name, job, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get status for build job `{}`.'.format(job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Statuses for build job `{}`.'.format(job))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No statuses found for build job `{}`.'.format(job))

    objects = list_dicts_to_tabulate([Printer.handle_statuses(o.to_light_dict(humanize_values=True))
                                      for o in response['results']])
    if objects:
        Printer.print_header("Statuses:")
        objects.pop('job', None)
        dict_tabulate(objects, is_list_dict=True)


@build.command()
@click.option('--gpu', '-g', is_flag=True, help='List job GPU resources.')
@click.pass_context
@clean_outputs
def resources(ctx, gpu):
    """Get build job resources.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon build -j 2 resources
    ```

    For GPU resources

    \b
    ```bash
    $ polyaxon build -j 2 resources --gpu
    ```
    """
    user, project_name, job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])
    try:
        message_handler = Printer.gpu_resources if gpu else Printer.resources
        PolyaxonClients().build_job.resources(user,
                                              project_name,
                                              job,
                                              message_handler=message_handler)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get resources for build job `{}`.'.format(job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


@build.command()
@click.option('--past', is_flag=True, help="Show the past logs.")
@click.option('--follow', is_flag=True, default=False, help="Stream logs after showing past logs.")
@click.pass_context
@clean_outputs
def logs(ctx, past, follow):
    """Get build logs.

    Uses [Caching](/polyaxon_cli/introduction#Caching)

    Examples:

    \b
    ```bash
    $ polyaxon build -j 2 logs
    ```

    \b
    ```bash
    $ polyaxon build logs
    ```
    """
    user, project_name, job = get_job_or_local(ctx.obj['project'], ctx.obj['job'])

    def message_handler(message):
        log_lines = to_list(message['log_lines'])
        for log_line in log_lines:
            Printer.log(log_line, nl=True)

    if past:
        try:
            response = PolyaxonClients().build_job.logs(
                user, project_name, job, stream=False)
            for log_line in response.content.decode().split('\n'):
                Printer.log(log_line, nl=True)

            if not follow:
                return
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not get logs for job `{}`.'.format(job))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    try:
        PolyaxonClients().build_job.logs(user,
                                         project_name,
                                         job,
                                         message_handler=message_handler)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not get logs for build job `{}`.'.format(job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
