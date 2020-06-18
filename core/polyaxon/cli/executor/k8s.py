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

from polyaxon import settings
from polyaxon.agents.spawners.spawner import Spawner
from polyaxon.cli.errors import handle_cli_error
from polyaxon.cli.operations import logs as run_logs
from polyaxon.exceptions import (
    PolyaxonCompilerError,
    PolyaxonK8SError,
    PolypodException,
)
from polyaxon.k8s.custom_resources.operation import get_resource_name
from polyaxon.polyaxonfile.specs import OperationSpecification
from polyaxon.polyflow import V1Operation
from polyaxon.polypod import compiler
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
):
    if not settings.CLIENT_CONFIG.set_polypod:
        Printer.print_warning("Polypod not configured!")
        return

    def create_run():
        click.echo("Creating a run.")
        try:
            compiled_operation = OperationSpecification.compile_operation(op_spec)
            run_name = compiled_operation.name or name
            resource = compiler.make(
                owner_name=owner,
                project_name=project_name,
                project_uuid=project_name,
                run_uuid=run_name,
                run_name=name,
                run_path=run_name,
                compiled_operation=compiled_operation,
                params=op_spec.params,
                default_sa=settings.AGENT_CONFIG.runs_sa,
            )
            Spawner(namespace=settings.AGENT_CONFIG.namespace).create(
                run_uuid=run_name,
                run_kind=compiled_operation.get_run_kind(),
                resource=resource,
            )
            # cache.cache(config_manager=RunManager, response=response)
            run_job_uid = get_resource_name(run_name)
            Printer.print_success("A new run `{}` was created".format(run_job_uid))
        except (PolyaxonCompilerError, PolyaxonK8SError, PolypodException) as e:
            handle_cli_error(e, message="Could not create a run.")
            sys.exit(1)

    create_run()
    logs_cmd = run_logs

    # Check if we need to invoke logs
    if log and logs_cmd:
        ctx.obj = {"project": "{}/{}".format(owner, project_name)}
        ctx.invoke(logs_cmd)
