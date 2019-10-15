# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon.cli.experiment import logs as experiment_logs
from polyaxon.cli.upload import upload as upload_cmd
from polyaxon.client import PolyaxonClient
from polyaxon.client.exceptions import (
    PolyaxonClientException,
    PolyaxonHTTPError,
    PolyaxonShouldExitError,
)
from polyaxon.managers.run import RunManager
from polyaxon.schemas.polyflow.ops import OpConfig
from polyaxon.utils import cache
from polyaxon.utils.formatting import Printer


def run(
    ctx,
    name,
    user,
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
        click.echo("Creating an independent experiment.")
        experiment = OpConfig(
            name=name,
            description=description,
            tags=tags,
            content=specification.raw_data,
            ttl=ttl,
            is_managed=True,
        )
        try:
            response = PolyaxonClient().project.create_experiment(
                user, project_name, experiment
            )
            cache.cache(config_manager=RunManager, response=response)
            Printer.print_success("Experiment `{}` was created".format(response.id))
        except (
            PolyaxonHTTPError,
            PolyaxonShouldExitError,
            PolyaxonClientException,
        ) as e:
            Printer.print_error("Could not create experiment.")
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
    logs_cmd = experiment_logs

    # Check if we need to invoke logs
    if log and logs_cmd:
        ctx.obj = {"project": "{}/{}".format(user, project_name)}
        ctx.invoke(logs_cmd)
