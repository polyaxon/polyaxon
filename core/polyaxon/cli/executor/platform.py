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
from polyaxon.managers.run import RunConfigManager
from polyaxon.polyflow import V1CompiledOperation, V1Operation
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
    eager: bool,
):
    polyaxon_client = RunClient(owner=owner, project=project_name)

    def cache_run(data):
        config = polyaxon_client.client.sanitize_for_serialization(data)
        cache.cache(
            config_manager=RunConfigManager,
            config=config,
            owner=owner,
            project=project_name,
        )

    def create_run(is_manged: bool = True):
        try:
            response = polyaxon_client.create(
                name=name,
                description=description,
                tags=tags,
                content=op_spec,
                is_managed=is_manged,
            )
            Printer.print_success("A new run `{}` was created".format(response.uuid))
            if not eager:
                cache_run(response)
                click.echo(
                    "You can view this run on Polyaxon UI: {}".format(
                        get_dashboard_url(
                            subpath="{}/{}/runs/{}".format(
                                owner, project_name, response.uuid
                            )
                        )
                    )
                )
                return response.uuid
        except (ApiException, HTTPError) as e:
            handle_cli_error(e, message="Could not create a run.")
            sys.exit(1)

    def refresh():
        try:
            polyaxon_client.refresh_data()
        except (ApiException, HTTPError) as e:
            handle_cli_error(e, message="Could not create a run.")
            sys.exit(1)

    click.echo("Creating a new run...")
    run_uuid = create_run(not eager)
    if eager:
        from polyaxon.polyaxonfile.manager import get_eager_matrix_operations

        refresh()
        click.echo("Starting eager mode...")
        compiled_operation = V1CompiledOperation.read(polyaxon_client.run_data.content)
        op_specs = get_eager_matrix_operations(
            content=polyaxon_client.run_data.raw_content,
            compiled_operation=compiled_operation,
            is_cli=True,
        )
        click.echo("Creating {} operations".format(len(op_specs)))
        for op_spec in op_specs:
            create_run()
        return

    # Check if we need to invoke logs
    if watch and not eager:
        ctx.obj = {"project": "{}/{}".format(owner, project_name), "run_uuid": run_uuid}
        ctx.invoke(statuses, watch=True)

    # Check if we need to invoke logs
    if log and not eager:
        ctx.obj = {"project": "{}/{}".format(owner, project_name), "run_uuid": run_uuid}
        ctx.invoke(run_logs)
