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

from typing import List

import click

from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon.cli.dashboard import get_dashboard_url
from polyaxon.cli.errors import handle_cli_error
from polyaxon.cli.operations import logs as run_logs
from polyaxon.cli.operations import statuses
from polyaxon.client import RunClient
from polyaxon.managers.run import RunManager
from polyaxon.polyflow import V1Operation
from polyaxon.utils import cache
from polyaxon.utils.formatting import Printer


def run(
    ctx,
    name: str,
    owner: str,
    project_name: str,
    description: str,
    tags: List[str],
    op_spec: V1Operation,
    log: bool,
    watch: bool,
):
    def create_run():
        click.echo("Creating a run.")
        try:
            polyaxon_client = RunClient(owner=owner, project=project_name)
            response = polyaxon_client.create(
                name=name, description=description, tags=tags, content=op_spec
            )
            config = polyaxon_client.client.sanitize_for_serialization(response)
            cache.cache(
                config_manager=RunManager,
                config=config,
                owner=owner,
                project=project_name,
            )
            Printer.print_success("A new run `{}` was created".format(response.uuid))
            click.echo(
                "You can view this run on Polyaxon UI: {}".format(
                    get_dashboard_url(
                        subpath="{}/{}/runs/{}".format(
                            owner, project_name, response.uuid
                        )
                    )
                )
            )
        except (ApiException, HTTPError) as e:
            handle_cli_error(e, message="Could not create a run.")
            sys.exit(1)

    create_run()

    # Check if we need to invoke logs
    if watch:
        ctx.obj = {"project": "{}/{}".format(owner, project_name)}
        ctx.invoke(statuses, watch=True)

    # Check if we need to invoke logs
    if log:
        ctx.obj = {"project": "{}/{}".format(owner, project_name)}
        ctx.invoke(run_logs)
