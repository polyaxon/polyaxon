# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_cli.cli.getters.user import get_username_or_local
from polyaxon_cli.client import PolyaxonClient
from polyaxon_cli.client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.utils.formatting import (
    Printer,
    dict_tabulate,
    get_meta_response,
    list_dicts_to_tabulate
)
from polyaxon_client.exceptions import PolyaxonClientException


@click.group()
@click.option('--username', '-u', type=str)
@click.pass_context
@clean_outputs
def bookmark(ctx, username):  # pylint:disable=redefined-outer-name
    """Commands for bookmarks."""
    ctx.obj = ctx.obj or {}
    ctx.obj['username'] = username


@bookmark.command()
@click.option('--page', type=int, help='To paginate through the list of projects.')
@click.pass_context
@clean_outputs
def projects(ctx, page):
    """List bookmarked projects for user.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon bookmark projects
    ```

    \b
    ```bash
    $ polyaxon bookmark -u adam projects
    ```
    """
    user = get_username_or_local(ctx.obj.get('username'))

    page = page or 1
    try:
        response = PolyaxonClient().bookmark.projects(username=user, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error(
            'Could not get bookmarked projects for user `{}`.'.format(user))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Bookmarked projects for user `{}`.'.format(user))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No bookmarked projects found for user `{}`.'.format(user))

    objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
               for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Projects:")
        dict_tabulate(objects, is_list_dict=True)


@bookmark.command()
@click.option('--page', type=int, help='To paginate through the list of groups.')
@click.pass_context
@clean_outputs
def groups(ctx, page):
    """List bookmarked experiment groups for user.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon bookmark groups
    ```

    \b
    ```bash
    $ polyaxon bookmark -u adam groups
    ```
    """
    user = get_username_or_local(ctx.obj.get('username'))

    page = page or 1
    try:
        response = PolyaxonClient().bookmark.groups(username=user, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error(
            'Could not get bookmarked experiment groups for user `{}`.'.format(user))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Bookmarked experiment groups for user `{}`.'.format(user))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No bookmarked experiment groups found for user `{}`.'.format(user))

    objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
               for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Experiment groups:")
        dict_tabulate(objects, is_list_dict=True)


@bookmark.command()
@click.option('--page', type=int, help='To paginate through the list of experiments.')
@click.pass_context
@clean_outputs
def experiments(ctx, page):
    """List bookmarked experiments for user.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon bookmark experiments
    ```

    \b
    ```bash
    $ polyaxon bookmark -u adam experiments
    ```
    """
    user = get_username_or_local(ctx.obj.get('username'))

    page = page or 1
    try:
        response = PolyaxonClient().bookmark.experiments(username=user, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error(
            'Could not get bookmarked experiments for user `{}`.'.format(user))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Bookmarked experiments for user `{}`.'.format(user))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No bookmarked experiments found for user `{}`.'.format(user))

    objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
               for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Experiments:")
        dict_tabulate(objects, is_list_dict=True)


@bookmark.command()
@click.option('--page', type=int, help='To paginate through the list of jobs.')
@click.pass_context
@clean_outputs
def jobs(ctx, page):
    """List bookmarked jobs for user.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon bookmark jobs
    ```

    \b
    ```bash
    $ polyaxon bookmark -u adam jobs
    ```
    """
    user = get_username_or_local(ctx.obj.get('username'))

    page = page or 1
    try:
        response = PolyaxonClient().bookmark.jobs(username=user, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error(
            'Could not get bookmarked jobs for user `{}`.'.format(user))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Bookmarked jobs for user `{}`.'.format(user))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No bookmarked jobs found for user `{}`.'.format(user))

    objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
               for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Jobs:")
        dict_tabulate(objects, is_list_dict=True)


@bookmark.command()
@click.option('--page', type=int, help='To paginate through the list of builds.')
@click.pass_context
@clean_outputs
def builds(ctx, page):
    """List bookmarked builds for user.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon bookmark builds
    ```

    \b
    ```bash
    $ polyaxon bookmark -u adam builds
    ```
    """
    user = get_username_or_local(ctx.obj.get('username'))

    page = page or 1
    try:
        response = PolyaxonClient().bookmark.builds(username=user, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error(
            'Could not get bookmarked builds for user `{}`.'.format(user))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Bookmarked builds for user `{}`.'.format(user))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No bookmarked builds found for user `{}`.'.format(user))

    objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
               for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Builds:")
        dict_tabulate(objects, is_list_dict=True)
