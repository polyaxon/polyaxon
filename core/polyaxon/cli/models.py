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

import click

from polyaxon.cli.options import OPTIONS_MODEL_VERSION, OPTIONS_NAME, OPTIONS_PROJECT
from polyaxon.cli.project_versions import (
    delete_project_version,
    get_project_version,
    list_project_versions,
    open_project_version_dashboard,
    register_project_version,
    stage_project_version,
    update_project_version,
)
from polyaxon.env_vars.getters import get_project_or_local
from polyaxon.lifecycle import V1ProjectVersionKind, V1Stages
from polyaxon.logger import clean_outputs
from polyaxon.utils.formatting import Printer


@click.group()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_MODEL_VERSION["args"], **OPTIONS_MODEL_VERSION["kwargs"])
@click.pass_context
@clean_outputs
def models(ctx, project, version):
    """Commands for managing models."""
    ctx.obj = ctx.obj or {}
    if project or version:
        Printer.print_warning(
            "Passing arguments to command groups is deprecated and will be removed in v2! "
            "Please use arguments on the sub-command directly: `polyaxon ops SUB_COMMAND --help`"
        )
    ctx.obj["project"] = project
    if ctx.invoked_subcommand not in ["ls"]:
        ctx.obj["version"] = version


@models.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(
    "--query",
    "-q",
    type=str,
    help="To filter the model versions based on this query spec.",
)
@click.option(
    "--sort",
    "-s",
    type=str,
    help="To order the model versions based on the sort spec.",
)
@click.option("--limit", type=int, help="To limit the list of model versions.")
@click.option("--offset", type=int, help="To offset the list of model versions.")
@click.pass_context
@clean_outputs
def ls(ctx, project, query, sort, limit, offset):
    """List model versions by owner or owner/model.

    Example:

    \b
    $ polyaxon models ls -p=project-name

    \b
    $ polyaxon models ls -p=acme/project-name
    """
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )

    list_project_versions(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.MODEL,
        query=query,
        sort=sort,
        limit=limit,
        offset=offset,
    )


@models.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_MODEL_VERSION["args"], **OPTIONS_MODEL_VERSION["kwargs"])
@click.option("--description", type=str, help="Description of the version.")
@click.option("--tags", type=str, help="Tags of the version, comma separated values.")
@click.option(
    "--content", type=str, help="Additional content/metadata fo the model version."
)
@click.option("--run-uid", type=str, help="The run to link to this model version.")
@click.option(
    "--artifacts",
    "artifacts_",
    type=str,
    help="The artifacts to link to this model version.",
)
@click.option(
    "--connection", type=str, help="The connection to link to this model version."
)
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Flag to force register if the version already exists.",
)
@click.pass_context
@clean_outputs
def register(
    ctx,
    project,
    version,
    description,
    tags,
    content,
    run_uid,
    artifacts_,
    connection,
    force,
):
    """Push a new model version.
    If the name corresponds to an existing model version, it will be updated.

    Example:

    \b
    $ polyaxon models register --artifacts=model,env --run=uuid

    \b
    $ polyaxon models register -f polyaxonfile.yaml --project=kaniko --description="..."

    \b
    $ polyaxon models register -f polyaxonfile.yaml -p kaniko -ver latest --run=uuid

    \b
    $ polyaxon models register -f polyaxonfile.yaml -p owner/name -ver v1 --tags="tag1,tag2"
    """
    version = version or ctx.obj.get("version")
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    register_project_version(
        owner=owner,
        project_name=project_name,
        version=version,
        kind=V1ProjectVersionKind.MODEL,
        description=description,
        tags=tags,
        content=content,
        run=run_uid,
        connection=connection,
        artifacts=artifacts_,
        force=force,
    )


@models.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_MODEL_VERSION["args"], **OPTIONS_MODEL_VERSION["kwargs"])
@click.pass_context
@clean_outputs
def get(ctx, project, version):
    """Get info for a model version by name, name & version, owner/name & tag.

    Examples:

    \b
    $ polyaxon models get  // returns `latest` in current project

    \b
    $ polyaxon models get --project=my-project --version=test-version

    \b
    $ polyaxon models get -p owner/my-project -ver rc12
    """
    version = version or ctx.obj.get("version") or "latest"
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    get_project_version(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.MODEL,
        version=version,
    )


@models.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_MODEL_VERSION["args"], **OPTIONS_MODEL_VERSION["kwargs"])
@click.pass_context
@clean_outputs
def delete(ctx, project, version):
    """Delete a model version.

    Examples:

    \b
    $ polyaxon models delete  // delete `latest` in current project

    \b
    $ polyaxon models delete --project=my-project --version=test-version

    \b
    $ polyaxon models get -p owner/my-project -ver rc12
    """
    version = version or ctx.obj.get("version") or "latest"
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    delete_project_version(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.MODEL,
        version=version,
    )


@models.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_MODEL_VERSION["args"], **OPTIONS_MODEL_VERSION["kwargs"])
@click.option(
    *OPTIONS_NAME["args"],
    type=str,
    help="Name of the model version, must be unique within the same project.",
)
@click.option("--description", type=str, help="Description of the model version.")
@click.option(
    "--tags", type=str, help="Tags of the run, comma separated values (optional)."
)
@click.pass_context
@clean_outputs
def update(ctx, project, version, name, description, tags):
    """Update model version.

    Uses /docs/core/cli/#caching

    Example:

    \b
    $ polyaxon models update --version=foobar --description="..."

    \b
    $ polyaxon models update -p mike1/foobar -ver current-name --name=new-name

    \b
    $ polyaxon models update --tags="foo, bar"
    """
    version = version or ctx.obj.get("version") or "latest"
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    update_project_version(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.MODEL,
        version=version,
        name=name,
        description=description,
        tags=tags,
    )


@models.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_MODEL_VERSION["args"], **OPTIONS_MODEL_VERSION["kwargs"])
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
    """Update stage for a model version.

    Uses /docs/core/cli/#caching

    Example:

    \b
    $ polyaxon models stage -ver rc-12 --to=production

    \b
    $ polyaxon models stage -p amce/foobar -ver rc-12 --to=staging --message="Use carefully!"
    """
    version = version or ctx.obj.get("version") or "latest"
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    stage_project_version(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.MODEL,
        version=version,
        to=to,
        message=message,
    )


@models.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_MODEL_VERSION["args"], **OPTIONS_MODEL_VERSION["kwargs"])
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
    help="Print the url of the dashboard for this model version.",
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
        kind=V1ProjectVersionKind.MODEL,
        version=version,
        url=url,
        yes=yes,
    )
