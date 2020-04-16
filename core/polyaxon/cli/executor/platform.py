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

from typing import Callable, List

import click

from polyaxon_sdk import V1OperationBody
from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon.cli.errors import handle_cli_error
from polyaxon.cli.operations import logs as run_logs
from polyaxon.cli.operations import statuses
from polyaxon.cli.upload import upload as upload_cmd
from polyaxon.client import PolyaxonClient
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
    upload: Callable,
    log: bool,
    watch: bool,
    can_upload: bool,
):
    def create_run():
        click.echo("Creating a run.")
        body = V1OperationBody(
            name=name,
            description=description,
            tags=tags,
            content=op_spec.to_dict(dump=True),
        )
        try:
            polyaxon_client = PolyaxonClient()
            response = polyaxon_client.runs_v1.create_run(owner, project_name, body)
            config = polyaxon_client.sanitize_for_serialization(response)
            cache.cache(config_manager=RunManager, config=config)
            Printer.print_success("A new run `{}` was created".format(response.uuid))
        except (ApiException, HTTPError) as e:
            handle_cli_error(e, message="Could not create a run.")
            sys.exit(1)

    # Check if we need to upload
    if upload:
        if can_upload:
            Printer.print_error(
                "Uploading is not supported when switching project context!"
            )
            click.echo(
                "Please, either omit the `-u` option or `-p` / `--project=` option."
            )
            sys.exit(1)
        ctx.invoke(upload_cmd, sync=False)

    create_run()

    # Check if we need to invoke logs
    if watch:
        ctx.obj = {"project": "{}/{}".format(owner, project_name)}
        ctx.invoke(statuses, watch=True)

    # Check if we need to invoke logs
    if log:
        ctx.obj = {"project": "{}/{}".format(owner, project_name)}
        ctx.invoke(run_logs)
