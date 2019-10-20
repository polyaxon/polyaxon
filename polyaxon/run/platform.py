# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_sdk import V1Run

from polyaxon.cli.runs import logs as run_logs
from polyaxon.cli.upload import upload as upload_cmd
from polyaxon.client import PolyaxonClient
from polyaxon.exceptions import (
    PolyaxonClientException,
    PolyaxonHTTPError,
    PolyaxonShouldExitError,
)
from polyaxon.managers.run import RunManager
from polyaxon.schemas.ops.termination import TerminationConfig
from polyaxon.schemas.polyflow.ops import OpConfig
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
    ttl,
    upload,
    log,
    can_upload,
):
    def run_experiment():
        click.echo("Creating a run.")
        termination = TerminationConfig(ttl=ttl)
        op = OpConfig(
            name=name,
            description=description,
            tags=tags,
            _template=specification.config,
            termination=termination,
            nocache=True,
        )
        run = V1Run(content=specification.config_dump)
        try:
            polyaxon_client = PolyaxonClient()
            response = polyaxon_client.runs_v1.create_run(owner, project_name, run)
            cache.cache(config_manager=RunManager, response=response)
            Printer.print_success("A new run `{}` was created".format(response.uuid))
        except (
            PolyaxonHTTPError,
            PolyaxonShouldExitError,
            PolyaxonClientException,
        ) as e:
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
        ctx.obj = {"project": "{}/{}".format(user, project_name)}
        ctx.invoke(logs_cmd)
