#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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
from polyaxon.cli.options import OPTIONS_PROJECT
from polyaxon.env_vars.getters import get_project_or_local
from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.logger import clean_outputs
from polyaxon.managers.git import GitConfigManager
from polyaxon.polyaxonfile import (
    CompiledOperationSpecification,
    OperationSpecification,
    check_polyaxonfile,
)
from polyaxon.utils import code_reference
from polyaxon.utils.formatting import Printer
from polyaxon.utils.validation import validate_tags


@click.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
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
    "--url",
    type=str,
    help="The url containing the polyaxonfile to run.",
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
    "--upload",
    "-u",
    is_flag=True,
    default=False,
    help="To upload an init context before scheduling the run.",
)
@click.option(
    "--upload-from",
    "-u-from",
    type=str,
    help="The path to upload from relative the current location.",
)
@click.option(
    "--upload-to",
    "-u-to",
    type=str,
    help="The path to upload to relative the run's root context.",
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
@click.option("--presets", type=str, help="Name of the presets to use for this run.")
@click.option(
    "--queue",
    "-q",
    type=str,
    help="Name of the queue to use for this run. "
    "If the name is not namespaced by the agent name the default agent is used: "
    "queue-name or agent-name/queue-name",
)
@click.option(
    "--nocache",
    is_flag=True,
    default=False,
    help="Disable cache check before starting this operation.",
)
@click.option(
    "--cache",
    is_flag=True,
    default=False,
    help="Enable cache check before starting this operation.",
)
@click.option(
    "--eager",
    is_flag=True,
    default=False,
    help="A flag to enable eager mode for pipeline operations, "
    "currently this mode supports grid search, random search, and parallel mapping. "
    "Note that this flag requires numpy.",
)
@click.option(
    "--git-preset",
    is_flag=True,
    default=False,
    help="A flag to enable automatic injection of a git initializer as a preset "
    "using the initialized git connection.",
)
@click.option(
    "--git-revision",
    type=str,
    help="If provided, Polyaxon will use this git revision "
    "instead of trying to detected and use the latest commit. "
    "The git revision could be a commit or a branch or any valid tree-ish. "
    "This flag is only used when the repo is initialized with: "
    "`polyaxon init [--git-connection] [--git-url]`",
)
@click.option(
    "--ignore-template",
    is_flag=True,
    default=False,
    help="If provided, Polyaxon will ignore template definition and "
    "submit the manifest to be checked by the API.",
)
@click.pass_context
@clean_outputs
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
    upload,
    upload_from,
    upload_to,
    watch,
    local,
    params,
    presets,
    queue,
    nocache,
    cache,
    eager,
    git_preset,
    git_revision,
    ignore_template,
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
    if cache and nocache:
        Printer.print_error(
            "You can't use `--cache` and `--nocache` at the same.", sys_exit=True
        )
    if (upload_to or upload_from) and not upload:
        upload = True
    if upload and eager:
        Printer.print_error(
            "You can't use `--upload` and `--eager` at the same.", sys_exit=True
        )

    git_init = None
    if git_preset or git_revision:
        # Check that the current path was initialized
        if not GitConfigManager.is_initialized():
            Printer.print_error(
                "You can't use `--git-preset [--git-revision]`, "
                "the current path is not initialized with a valid git connection or a git url, "
                "please run `polyaxon init [--git-connection] [--git-url]` "
                "to set a valid git configuration.",
                sys_exit=True,
            )
        git_init = GitConfigManager.get_config()
        if git_revision:
            git_init.git.revision = git_revision
        elif code_reference.is_git_initialized(path="."):
            if code_reference.is_dirty(path="."):
                Printer.print_warning(
                    "Polyaxon detected uncommitted changes in the current git repo!"
                )
            commit_hash = code_reference.get_commit()
            git_init.git.revision = commit_hash
        else:
            Printer.print_warning(
                "Polyaxon could not find a valid git repo, "
                "and will not add the current commit to the git initializer."
            )

    presets = validate_tags(presets)

    op_spec = check_polyaxonfile(
        polyaxonfile=polyaxonfile,
        python_module=python_module,
        url=url,
        hub=hub,
        params=params,
        presets=presets,
        queue=queue,
        cache=cache,
        nocache=nocache,
        verbose=False,
        eager=eager,
        git_init=git_init,
        ignore_template=ignore_template,
    )

    if ignore_template:
        op_spec.disable_template()
    if op_spec.is_template():
        click.echo("Please customize the specification or disable the template.")
        sys.exit(1)

    owner, project_name = get_project_or_local(project, is_cli=True)
    tags = validate_tags(tags)

    if local:
        try:
            compiled_operation = OperationSpecification.compile_operation(op_spec)
            compiled_operation = (
                CompiledOperationSpecification.apply_operation_contexts(
                    compiled_operation
                )
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
            upload=upload,
            upload_to=upload_to,
            upload_from=upload_from,
            watch=watch,
            eager=eager,
        )
