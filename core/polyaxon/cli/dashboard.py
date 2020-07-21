#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

import sys

import click

from polyaxon import settings
from polyaxon.utils.http_utils import clean_host


def get_dashboard_url(base: str = "ui", subpath: str = "") -> str:
    dashboard_url = "{}/{}/".format(clean_host(settings.CLIENT_CONFIG.host), base)
    if subpath:
        return "{}{}/".format(dashboard_url, subpath.rstrip("/"))
    return dashboard_url


def get_dashboard(dashboard_url: str, url_only: bool, yes: bool):
    if url_only:
        click.echo(dashboard_url)
        sys.exit(0)
    if not yes:
        click.confirm(
            "Dashboard page will now open in your browser. Continue?",
            abort=True,
            default=True,
        )

    click.launch(dashboard_url)


@click.command()
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Automatic yes to prompts. "
    'Assume "yes" as answer to all prompts and run non-interactively.',
)
@click.option(
    "--url", is_flag=True, default=False, help="Print the url of the dashboard."
)
def dashboard(yes, url):
    """Open dashboard in browser."""
    get_dashboard(dashboard_url=get_dashboard_url(), url_only=url, yes=yes)
