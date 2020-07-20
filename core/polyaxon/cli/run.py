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

from marshmallow import ValidationError

from polyaxon import settings
from polyaxon.cli.executor import docker_run, k8s_run, platform_run
from polyaxon.env_vars.getters import get_project_or_local
from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.polyaxonfile import (
    CompiledOperationSpecification,
    OperationSpecification,
    check_polyaxonfile,
)
from polyaxon.utils.formatting import Printer
from polyaxon.utils.validation import validate_tags


@click.command()
@click.option("--project", "-p", type=str)
@click.option(
    "-f",
    "--file",
    "polyaxonfile",
    multiple=True,
    type=click.Path(exists=True),
    help="The polyaxonfiles to run.",
)
@click.option(
    "-pm",
    "--python-module",
    type=str,
    help="The python module containing the polyaxonfile to run.",
)
@click.option(
    "--url", type=str, help="The url containing the polyaxonfile to run.",
)
@click.option(
    "--hub",
    type=str,
    help="The Component Hub name containing the polyaxonfile to run.",
)
@click.option(
    "--name",
    type=str,
    help="Name to give to this run, must be unique within the project, could be none.",
)
@click.option("--tags", type=str, help="Tags of this run, comma separated values.")
@click.option("--description", type=str, help="The description to give to this run.")
@click.option(
    "--log",
    "-l",
    is_flag=True,
    default=False,
    help="To start logging after scheduling the run.",
)
@click.option(
    "--watch",
    "-w",
    is_flag=True,
    default=False,
    help="To start statuses watch loop after scheduling the run.",
)
@click.option(
    "--local",
    is_flag=True,
    default=False,
    help="To start the run locally, with `docker` environment as default.",
)
@click.option(
    "--params",
    "-P",
    metavar="NAME=VALUE",
    multiple=True,
    help="A parameter to override the default params of the run, form -P name=value.",
)
@click.option("--profile", type=str, help="Name of the profile to use for this run.")
@click.option(
    "--queue",
    type=str,
    help="Name of the queue to use for this run. "
    "If the name is not namespaced by the agent name the default agent is used: "
    "queue-name or agent-name/queue-name",
)
@click.option(
    "--nocache",
    is_flag=True,
    default=None,
    help="Disable cache check before starting this operation.",
)
@click.pass_context
def run(
    ctx,
    project,
    polyaxonfile,
    python_module,
    url,
    hub,
    name,
    tags,
    description,
    log,
    watch,
    local,
    params,
    profile,
    queue,
    nocache,
):
    """Run polyaxonfile specification.

    Examples:

    \b
    $ polyaxon run -f file -f file_override ...

    Run and set description and tags for this run

    \b
    $ polyaxon run -f file --description="Description of the current run" --tags="foo, bar, moo"

    Run and set a unique name for this run

    \b
    polyaxon run --name=foo

    Run for a specific project

    \b
    $ polyaxon run -p project1 -f file.yaml

    Run with updated params

    \b
    $ polyaxon run -p project1 -f file.yaml -P param1=234.2 -P param2=relu

    If a python file contains a component main, you can run that component

    \b
    polyaxon run -pm path/to/my-component.py


    If a python file contains more than one component, you can specify the component to run

    \b
    polyaxon run -pm path/to/my-component.py:componentA
    """
    op_spec = check_polyaxonfile(
        polyaxonfile=polyaxonfile,
        python_module=python_module,
        url=url,
        hub=hub,
        params=params,
        profile=profile,
        queue=queue,
        nocache=nocache,
        log=False,
    )

    owner, project_name = get_project_or_local(project, is_cli=True)
    tags = validate_tags(tags)

    if local:
        try:
            compiled_operation = OperationSpecification.compile_operation(op_spec)
            compiled_operation = CompiledOperationSpecification.apply_operation_contexts(
                compiled_operation
            )
        except (PolyaxonSchemaError, ValidationError):
            Printer.print_error(
                "Could not run this polyaxonfile locally, "
                "a context is required to resolve it dependencies."
            )
            sys.exit(1)
        docker_run(
            ctx=ctx,
            name=name,
            owner=owner,
            project_name=project_name,
            description=description,
            tags=tags,
            compiled_operation=compiled_operation,
            log=log,
        )
    elif settings.CLIENT_CONFIG.no_api:
        k8s_run(
            ctx=ctx,
            name=name,
            owner=owner,
            project_name=project_name,
            description=description,
            tags=tags,
            op_spec=op_spec,
            log=log,
        )
    else:
        platform_run(
            ctx=ctx,
            name=name,
            owner=owner,
            project_name=project_name,
            description=description,
            tags=tags,
            op_spec=op_spec,
            log=log,
            watch=watch,
        )
