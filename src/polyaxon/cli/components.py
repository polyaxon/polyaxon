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
import os
import sys

import click

from polyaxon import settings
from polyaxon.cli.errors import handle_cli_error
from polyaxon.cli.options import (
    OPTIONS_COMPONENT_VERSION,
    OPTIONS_NAME,
    OPTIONS_PROJECT,
)
from polyaxon.cli.project_versions import (
    delete_project_version,
    get_project_version,
    list_project_versions,
    open_project_version_dashboard,
    register_project_version,
    stage_project_version,
    update_project_version,
)
from polyaxon.client import PolyaxonClient
from polyaxon.constants.globals import NO_AUTH
from polyaxon.env_vars.getters import get_project_or_local
from polyaxon.lifecycle import V1ProjectVersionKind, V1Stages
from polyaxon.logger import clean_outputs
from polyaxon.polyaxonfile import get_specification
from polyaxon.schemas.cli.client_config import ClientConfig
from polyaxon.utils.formatting import Printer, dict_tabulate, list_dicts_to_tabulate


def get_current_or_public_client():
    if settings.CLI_CONFIG.is_ce:
        return PolyaxonClient(config=ClientConfig(), token=NO_AUTH)

    return PolyaxonClient()


def get_specification_details(content):
    if not content:
        Printer.print_warning(
            "This component version does not have any polyaxonfile content!"
        )
        return
    specification = get_specification(data=content)
    if specification.inputs:
        Printer.print_header("Component inputs:")
        objects = list_dicts_to_tabulate([i.to_dict() for i in specification.inputs])
        dict_tabulate(objects, is_list_dict=True)

    if specification.outputs:
        Printer.print_header("Component outputs:")
        objects = list_dicts_to_tabulate([o.to_dict() for o in specification.outputs])
        dict_tabulate(objects, is_list_dict=True)

    Printer.print_header("Content:")
    click.echo(specification.to_dict())


@click.group()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_COMPONENT_VERSION["args"], **OPTIONS_COMPONENT_VERSION["kwargs"])
@click.pass_context
@clean_outputs
def components(ctx, project, version):
    """Commands for managing components."""
    ctx.obj = ctx.obj or {}
    if project or version:
        Printer.print_warning(
            "Passing arguments to command groups is deprecated and will be removed in v2! "
            "Please use arguments on the sub-command directly: `polyaxon ops SUB_COMMAND --help`"
        )
    ctx.obj["project"] = project
    if ctx.invoked_subcommand not in ["ls"]:
        ctx.obj["version"] = version


@components.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(
    "--query",
    "-q",
    type=str,
    help="To filter the component versions based on this query spec.",
)
@click.option(
    "--sort",
    "-s",
    type=str,
    help="To order the component versions based on the sort spec.",
)
@click.option("--limit", type=int, help="To limit the list of component versions.")
@click.option("--offset", type=int, help="To offset the list of component versions.")
@click.pass_context
@clean_outputs
def ls(ctx, project, query, sort, limit, offset):
    """List component versions by project or owner/project.

    Example:

    \b
    $ polyaxon components ls -p=kaniko

    \b
    $ polyaxon components ls -p=acme/kaniko
    """
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    polyaxon_client = get_current_or_public_client()
    list_project_versions(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.COMPONENT,
        query=query,
        sort=sort,
        limit=limit,
        offset=offset,
        client=polyaxon_client,
    )


@components.command()
@click.option(
    "-f",
    "--file",
    "polyaxonfile",
    type=click.Path(exists=True),
    help="The component spec version to push.",
)
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_COMPONENT_VERSION["args"], **OPTIONS_COMPONENT_VERSION["kwargs"])
@click.option("--description", type=str, help="Description of the version.")
@click.option("--tags", type=str, help="Tags of the version, comma separated values.")
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Flag to force push if the version already exists.",
)
@click.pass_context
@clean_outputs
def push(ctx, polyaxonfile, project, version, description, tags, force):
    """Push a new component version.
    If the name corresponds to an existing component version, it will be updated.

    Example:

    \b
    $ polyaxon components push -f polyaxonfile.yaml

    \b
    $ polyaxon components push -f polyaxonfile.yaml --project=kaniko --description="..."

    \b
    $ polyaxon components push -f polyaxonfile.yaml -p kaniko -ver latest

    \b
    $ polyaxon components push -f polyaxonfile.yaml -p owner/name -ver v1 --tags="tag1,tag2"
    """
    version = version or ctx.obj.get("version")
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )

    if not polyaxonfile or not os.path.isfile(polyaxonfile):
        Printer.print_error(
            "Please provide a path to a polyaxonfile to create a component version.",
            command_help="components push",
            sys_exit=True,
        )
    try:
        plx_file = get_specification(data=polyaxonfile)
    except Exception as e:
        handle_cli_error(e, message="Polyaxonfile is not valid.")
        sys.exit(1)

    register_project_version(
        owner=owner,
        project_name=project_name,
        version=version,
        kind=V1ProjectVersionKind.COMPONENT,
        description=description,
        tags=tags,
        content=plx_file.to_dict(dump=True),
        force=force,
    )


@components.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_COMPONENT_VERSION["args"], **OPTIONS_COMPONENT_VERSION["kwargs"])
@click.pass_context
@clean_outputs
def get(ctx, project, version):
    """Get info for a component version by name, name & version, owner/name & tag.

    Examples:

    \b
    $ polyaxon components get  // returns `latest` in current project

    \b
    $ polyaxon components get --project=my-project --version=test-version

    \b
    $ polyaxon components get -p owner/my-project -ver rc12
    """
    version = version or ctx.obj.get("version") or "latest"
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    polyaxon_client = get_current_or_public_client()

    get_project_version(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.COMPONENT,
        version=version,
        content_callback=get_specification_details,
        client=polyaxon_client,
    )


@components.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_COMPONENT_VERSION["args"], **OPTIONS_COMPONENT_VERSION["kwargs"])
@click.pass_context
@clean_outputs
def delete(ctx, project, version):
    """Delete component version.

    Examples:

    \b
    $ polyaxon components delete  // delete `latest` in current project

    \b
    $ polyaxon components delete --project=my-project --version=test-version

    \b
    $ polyaxon components get -p owner/my-project -ver rc12
    """
    version = version or ctx.obj.get("version") or "latest"
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    delete_project_version(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.COMPONENT,
        version=version,
    )


@components.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_COMPONENT_VERSION["args"], **OPTIONS_COMPONENT_VERSION["kwargs"])
@click.option(
    *OPTIONS_NAME["args"],
    type=str,
    help="Name of the component version, must be unique within a project.",
)
@click.option("--description", type=str, help="Description of the component version.")
@click.option(
    "--tags", type=str, help="Tags of the run, comma separated values (optional)."
)
@click.pass_context
@clean_outputs
def update(ctx, project, version, name, description, tags):
    """Update component version.

    Uses /docs/core/cli/#caching

    Example:

    \b
    $ polyaxon components update --version=foobar --description="..."

    \b
    $ polyaxon components update -p mike1/foobar -ver current-name --name=new-name

    \b
    $ polyaxon components update --tags="foo, bar"
    """
    version = version or ctx.obj.get("version") or "latest"
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    update_project_version(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.COMPONENT,
        version=version,
        name=name,
        description=description,
        tags=tags,
        content_callback=get_specification_details,
    )


@components.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_COMPONENT_VERSION["args"], **OPTIONS_COMPONENT_VERSION["kwargs"])
@click.option(
    "--to",
    "-to",
    type=click.Choice(V1Stages.allowable_values, case_sensitive=True),
    help="Stage to transition to.",
)
@click.option(
    "--message", type=str, help="Additional information to set with this stage change."
)
@click.pass_context
@clean_outputs
def stage(ctx, project, version, to, message):
    """Update stage for a component version.

    Uses /docs/core/cli/#caching

    Example:

    \b
    $ polyaxon components stage -ver rc-12 --to=production

    \b
    $ polyaxon components stage -p amce/foobar -ver rc-12 --to=staging --message="Use carefully!"
    """
    version = version or ctx.obj.get("version") or "latest"
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    stage_project_version(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.COMPONENT,
        version=version,
        to=to,
        message=message,
    )


@components.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_COMPONENT_VERSION["args"], **OPTIONS_COMPONENT_VERSION["kwargs"])
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Automatic yes to prompts. "
    'Assume "yes" as answer to all prompts and run non-interactively.',
)
@click.option(
    "--url",
    is_flag=True,
    default=False,
    help="Print the url of the dashboard for this component version.",
)
@click.pass_context
@clean_outputs
def dashboard(ctx, project, version, yes, url):
    """Open this operation's dashboard details in browser."""
    version = version or ctx.obj.get("version") or "latest"
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    open_project_version_dashboard(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.COMPONENT,
        version=version,
        url=url,
        yes=yes,
    )
