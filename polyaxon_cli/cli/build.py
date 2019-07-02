# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_cli.cli.getters.build import get_build_or_local
from polyaxon_cli.client import PolyaxonClient
from polyaxon_cli.client.exceptions import (
    PolyaxonClientException,
    PolyaxonHTTPError,
    PolyaxonShouldExitError
)
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.build_job import BuildJobManager
from polyaxon_cli.utils import cache
from polyaxon_cli.utils.formatting import (
    Printer,
    dict_tabulate,
    get_meta_response,
    get_resources,
    list_dicts_to_tabulate
)
from polyaxon_cli.utils.log_handler import get_logs_handler
from polyaxon_cli.utils.validation import validate_tags


def get_build_details(_build):
    if _build.description:
        Printer.print_header("Build description:")
        click.echo('{}\n'.format(_build.description))

    if _build.resources:
        get_resources(_build.resources.to_dict(), header="Build resources:")

    response = _build.to_light_dict(
        humanize_values=True,
        exclude_attrs=[
            'uuid', 'content', 'project', 'description', 'resources', 'is_clone', 'build_job'
        ])

    Printer.print_header("Build info:")
    dict_tabulate(Printer.add_status_color(response))


@click.group()
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'")
@click.option('--build', '-b', type=int, help="The build id.")
@click.pass_context
@clean_outputs
def build(ctx, project, build):  # pylint:disable=redefined-outer-name
    """Commands for build jobs."""
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project
    ctx.obj['build'] = build


@build.command()
@click.pass_context
@clean_outputs
def get(ctx):
    """Get build job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon build -b 1 get
    ```

    \b
    ```bash
    $ polyaxon build --build=1 --project=project_name get
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))
    try:
        response = PolyaxonClient().build_job.get_build(user, project_name, _build)
        cache.cache(config_manager=BuildJobManager, response=response)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get build job `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    get_build_details(response)


@build.command()
@click.pass_context
@clean_outputs
def delete(ctx):
    """Delete build job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon build delete
    ```

    \b
    ```bash
    $ polyaxon build -b 2 delete
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))
    if not click.confirm("Are sure you want to delete build job `{}`".format(_build)):
        click.echo('Existing without deleting build job.')
        sys.exit(1)

    try:
        response = PolyaxonClient().build_job.delete_build(
            user, project_name, _build)
        # Purge caching
        BuildJobManager.purge()
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not delete job `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Build job `{}` was deleted successfully".format(_build))


@build.command()
@click.option('--name', type=str,
              help='Name of the build, must be unique within the project, could none.')
@click.option('--description', type=str, help='Description of the build.')
@click.option('--tags', type=str, help='Tags of the build, comma separated values.')
@click.pass_context
@clean_outputs
def update(ctx, name, description, tags):
    """Update build.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon build -b 2 update --description="new description for my build"
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))
    update_dict = {}

    if name:
        update_dict['name'] = name

    if description:
        update_dict['description'] = description

    tags = validate_tags(tags)
    if tags:
        update_dict['tags'] = tags

    if not update_dict:
        Printer.print_warning('No argument was provided to update the build.')
        sys.exit(0)

    try:
        response = PolyaxonClient().build_job.update_build(
            user, project_name, _build, update_dict)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not update build `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Build updated.")
    get_build_details(response)


@build.command()
@click.option('--yes', '-y', is_flag=True, default=False,
              help="Automatic yes to prompts. "
                   "Assume \"yes\" as answer to all prompts and run non-interactively.")
@click.pass_context
@clean_outputs
def stop(ctx, yes):
    """Stop build job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon build stop
    ```

    \b
    ```bash
    $ polyaxon build -b 2 stop
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))
    if not yes and not click.confirm("Are sure you want to stop "
                                     "job `{}`".format(_build)):
        click.echo('Existing without stopping build job.')
        sys.exit(0)

    try:
        PolyaxonClient().build_job.stop(user, project_name, _build)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not stop build job `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Build job is being stopped.")


@build.command()
@click.pass_context
@clean_outputs
def invalidate(ctx):
    """Invalidate build job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon build invalidate
    ```

    \b
    ```bash
    $ polyaxon build -b 2 invalidate
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))
    try:
        PolyaxonClient().build_job.invalidate(user, project_name, _build)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not invalidate build job `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Build job has being invalidated.")


@build.command()
@click.pass_context
@clean_outputs
def bookmark(ctx):
    """Bookmark build job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon build bookmark
    ```

    \b
    ```bash
    $ polyaxon build -b 2 bookmark
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))
    try:
        PolyaxonClient().build_job.bookmark(user, project_name, _build)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not bookmark build job `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Build job bookmarked.")


@build.command()
@click.pass_context
@clean_outputs
def unbookmark(ctx):
    """Unbookmark build job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon build unbookmark
    ```

    \b
    ```bash
    $ polyaxon build -b 2 unbookmark
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))
    try:
        PolyaxonClient().build_job.unbookmark(user, project_name, _build)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not unbookmark build job `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Build job unbookmarked.")


@build.command()
@click.option('--page', type=int, help="To paginate through the list of statuses.")
@click.pass_context
@clean_outputs
def statuses(ctx, page):
    """Get build job statuses.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon build -b 2 statuses
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))
    page = page or 1
    try:
        response = PolyaxonClient().build_job.get_statuses(user, project_name, _build, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get status for build job `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Statuses for build job `{}`.'.format(_build))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No statuses found for build job `{}`.'.format(_build))

    objects = list_dicts_to_tabulate(
        [Printer.add_status_color(o.to_light_dict(humanize_values=True), status_key='status')
         for o in response['results']])
    if objects:
        Printer.print_header("Statuses:")
        objects.pop('job', None)
        dict_tabulate(objects, is_list_dict=True)


@build.command()
@click.option('--gpu', '-g', is_flag=True, help='List build GPU resources.')
@click.pass_context
@clean_outputs
def resources(ctx, gpu):
    """Get build job resources.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon build -b 2 resources
    ```

    For GPU resources

    \b
    ```bash
    $ polyaxon build -b 2 resources --gpu
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))
    try:
        message_handler = Printer.gpu_resources if gpu else Printer.resources
        PolyaxonClient().build_job.resources(user,
                                             project_name,
                                             _build,
                                             message_handler=message_handler)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get resources for build job `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


@build.command()
@click.option('--past', '-p', is_flag=True, help="Show the past logs.")
@click.option('--follow', '-f', is_flag=True, default=False,
              help="Stream logs after showing past logs.")
@click.option('--hide_time', is_flag=True, default=False,
              help="Whether or not to hide timestamps from the log stream.")
@click.pass_context
@clean_outputs
def logs(ctx, past, follow, hide_time):
    """Get build logs.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon build -b 2 logs
    ```

    \b
    ```bash
    $ polyaxon build logs
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))

    if past:
        try:
            response = PolyaxonClient().build_job.logs(
                user, project_name, _build, stream=False)
            get_logs_handler(handle_job_info=False,
                             show_timestamp=not hide_time,
                             stream=False)(response.content.decode().split('\n'))
            print()

            if not follow:
                return
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            if not follow:
                Printer.print_error('Could not get logs for job `{}`.'.format(_build))
                Printer.print_error('Error message `{}`.'.format(e))
                sys.exit(1)

    try:
        PolyaxonClient().build_job.logs(
            user,
            project_name,
            _build,
            message_handler=get_logs_handler(handle_job_info=False, show_timestamp=not hide_time))
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get logs for build job `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
