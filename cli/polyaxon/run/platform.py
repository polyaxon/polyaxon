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

# coding: utf-8
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_sdk import V1Run
from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon.cli.runs import logs as run_logs
from polyaxon.cli.upload import upload as upload_cmd
from polyaxon.client import PolyaxonClient
from polyaxon.managers.run import RunManager
from polyaxon.utils import cache
from polyaxon.utils.formatting import Printer


def run(
    ctx,
    name,
    owner,
    project_name,
    description,
    tags,
    specification,
    upload,
    log,
    can_upload,
):
    def run_experiment():
        click.echo("Creating a run.")
        run = V1Run(content=specification.config_dump)
        try:
            polyaxon_client = PolyaxonClient()
            response = polyaxon_client.runs_v1.create_run(owner, project_name, run)
            cache.cache(config_manager=RunManager, response=response)
            Printer.print_success("A new run `{}` was created".format(response.uuid))
        except (ApiException, HTTPError) as e:
            Printer.print_error("Could not create op.")
            Printer.print_error("Error message `{}`.".format(e))
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

    run_experiment()
    logs_cmd = run_logs

    # Check if we need to invoke logs
    if log and logs_cmd:
        ctx.obj = {"project": "{}/{}".format(owner, project_name)}
        ctx.invoke(logs_cmd)
