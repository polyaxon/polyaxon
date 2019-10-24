#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon.cli.getters.user import get_username_or_local
from polyaxon.client import PolyaxonClient
from polyaxon.logger import clean_outputs
from polyaxon.utils.formatting import (
    Printer,
    dict_tabulate,
    get_meta_response,
    list_dicts_to_tabulate,
)
from polyaxon.utils.query_params import get_query_params


@click.group()
@click.option("--username", "-u", type=str)
@click.pass_context
@clean_outputs
def bookmark(ctx, username):  # pylint:disable=redefined-outer-name
    """Commands for bookmarks."""
    ctx.obj = ctx.obj or {}
    ctx.obj["username"] = username


@bookmark.command()
@click.option("--limit", type=int, help="To limit the list of projects.")
@click.option("--offset", type=int, help="To offset the list of projects.")
@click.pass_context
@clean_outputs
def projects(ctx, limit, offset):
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
    user = get_username_or_local(ctx.obj.get("username"))

    try:
        params = get_query_params(limit=limit, offset=offset)
        polyaxon_client = PolyaxonClient()
        response = polyaxon_client.projects_v1.list_bookmarked_projects(user, **params)
    except (ApiException, HTTPError) as e:
        Printer.print_error(
            "Could not get bookmarked projects for user `{}`.".format(user)
        )
        Printer.print_error("Error message `{}`.".format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header("Bookmarked projects for user `{}`.".format(user))
        Printer.print_header("Navigation:")
        dict_tabulate(meta)
    else:
        Printer.print_header("No bookmarked projects found for user `{}`.".format(user))

    objects = [
        Printer.add_status_color(o.to_light_dict(humanize_values=True))
        for o in response.results
    ]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Projects:")
        dict_tabulate(objects, is_list_dict=True)


@bookmark.command()
@click.option("--limit", type=int, help="To limit the list of runs.")
@click.option("--offset", type=int, help="To offset the list of runs.")
@click.pass_context
@clean_outputs
def runs(ctx, limit, offset):
    """List bookmarked runs for user.

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
    user = get_username_or_local(ctx.obj.get("username"))

    try:
        params = get_query_params(limit=limit, offset=offset)
        polyaxon_client = PolyaxonClient()
        response = polyaxon_client.runs_v1.list_bookmarked_runs(user, **params)
    except (ApiException, HTTPError) as e:
        Printer.print_error(
            "Could not get bookmarked experiments for user `{}`.".format(user)
        )
        Printer.print_error("Error message `{}`.".format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header("Bookmarked experiments for user `{}`.".format(user))
        Printer.print_header("Navigation:")
        dict_tabulate(meta)
    else:
        Printer.print_header(
            "No bookmarked experiments found for user `{}`.".format(user)
        )

    objects = [
        Printer.add_status_color(o.to_light_dict(humanize_values=True))
        for o in response.results
    ]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Experiments:")
        dict_tabulate(objects, is_list_dict=True)
