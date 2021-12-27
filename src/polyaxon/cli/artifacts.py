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

from polyaxon.cli.options import OPTIONS_ARTIFACT_VERSION, OPTIONS_NAME, OPTIONS_PROJECT
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
@click.option(*OPTIONS_ARTIFACT_VERSION["args"], **OPTIONS_ARTIFACT_VERSION["kwargs"])
@click.pass_context
@clean_outputs
def artifacts(ctx, project, version):
    """Commands for managing artifacts."""
    ctx.obj = ctx.obj or {}
    if project or version:
        Printer.print_warning(
            "Passing arguments to command groups is deprecated and will be removed in v2! "
            "Please use arguments on the sub-command directly: `polyaxon ops SUB_COMMAND --help`"
        )
    ctx.obj["project"] = project
    if ctx.invoked_subcommand not in ["ls"]:
        ctx.obj["version"] = version


@artifacts.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(
    "--query",
    "-q",
    type=str,
    help="To filter the artifact versions based on this query spec.",
)
@click.option(
    "--sort",
    "-s",
    type=str,
    help="To order the artifact versions based on the sort spec.",
)
@click.option("--limit", type=int, help="To limit the list of artifact versions.")
@click.option("--offset", type=int, help="To offset the list of artifact versions.")
@click.pass_context
@clean_outputs
def ls(ctx, project, query, sort, limit, offset):
    """List artifact versions by owner or owner/artifact.

    Example:

    \b
    $ polyaxon artifacts ls -p project

    \b
    $ polyaxon artifacts ls --project=acme/data-versioning
    """
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    list_project_versions(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.ARTIFACT,
        query=query,
        sort=sort,
        limit=limit,
        offset=offset,
    )


@artifacts.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_ARTIFACT_VERSION["args"], **OPTIONS_ARTIFACT_VERSION["kwargs"])
@click.option("--description", type=str, help="Description of the version.")
@click.option("--tags", type=str, help="Tags of the version, comma separated values.")
@click.option(
    "--content", type=str, help="Additional content/metadata fo the artifact version."
)
@click.option("--run-uid", type=str, help="The run to link to this artifact version.")
@click.option(
    "--artifacts",
    "artifacts_",
    type=str,
    help="The artifacts to link to this artifact version.",
)
@click.option(
    "--connection", type=str, help="The connection to link to this artifact version."
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
    """Push a new artifact version.
    If the name corresponds to an existing artifact version, it will be updated.

    Example:

    \b
    $ polyaxon components register --name=version-name --connection=dataset-gcs --run=uuid

    \b
    $ polyaxon components register --project=images-dataset --connection=dataset-gcs --description="..."

    \b
    $ polyaxon components register -p images-dataset -ver latest --run=uuid --artifacts=lin1,lin2

    \b
    $ polyaxon components register -p owner/name -ver v1 --tags="tag1,tag2"
    """
    version = version or ctx.obj.get("version")
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    register_project_version(
        owner=owner,
        project_name=project_name,
        version=version,
        kind=V1ProjectVersionKind.ARTIFACT,
        description=description,
        tags=tags,
        content=content,
        run=run_uid,
        connection=connection,
        artifacts=artifacts_,
        force=force,
    )


@artifacts.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_ARTIFACT_VERSION["args"], **OPTIONS_ARTIFACT_VERSION["kwargs"])
@click.pass_context
@clean_outputs
def get(ctx, project, version):
    """Get info for an artifact version by name, name & version, owner/name & tag.

    Examples:

    To get a default artifact version:

    \b
    $ polyaxon artifacts get -p data-versioning

    To get by specific owner/name

    \b
    $ polyaxon artifacts get -p owner/data-versioning
    """
    version = version or ctx.obj.get("version") or "latest"
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    get_project_version(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.ARTIFACT,
        version=version,
    )


@artifacts.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_ARTIFACT_VERSION["args"], **OPTIONS_ARTIFACT_VERSION["kwargs"])
@click.pass_context
@clean_outputs
def delete(ctx, project, version):
    """Delete a artifact version.
    \b
    $ polyaxon artifacts delete  // delete `latest` in current project

    \b
    $ polyaxon artifacts delete --project=my-project --version=test-version

    \b
    $ polyaxon artifacts get -p owner/my-project -ver rc12
    """
    version = version or ctx.obj.get("version") or "latest"
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    delete_project_version(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.ARTIFACT,
        version=version,
    )


@artifacts.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_ARTIFACT_VERSION["args"], **OPTIONS_ARTIFACT_VERSION["kwargs"])
@click.option(
    *OPTIONS_NAME["args"],
    type=str,
    help="Name of the artifact version, must be unique within the same project.",
)
@click.option("--description", type=str, help="Description of the artifact version.")
@click.option(
    "--tags", type=str, help="Tags of the run, comma separated values (optional)."
)
@click.pass_context
@clean_outputs
def update(ctx, project, version, name, description, tags):
    """Update artifact version.

    Uses /docs/core/cli/#caching

    Example:

    \b
    $ polyaxon artifacts update --version=foobar --description="..."

    \b
    $ polyaxon artifacts update -p mike1/foobar -ver current-name --name=new-name

    \b
    $ polyaxon artifacts update --tags="foo, bar"
    """
    version = version or ctx.obj.get("version") or "latest"
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    update_project_version(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.ARTIFACT,
        version=version,
        name=name,
        description=description,
        tags=tags,
    )


@artifacts.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_ARTIFACT_VERSION["args"], **OPTIONS_ARTIFACT_VERSION["kwargs"])
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
    """Update stage for a artifact version.

    Uses /docs/core/cli/#caching

    Example:

    \b
    $ polyaxon artifacts stage -ver rc-12 --to=production

    \b
    $ polyaxon artifacts stage -p amce/foobar -ver rc-12 --to=staging --message="Use carefully!"
    """
    version = version or ctx.obj.get("version") or "latest"
    owner, project_name = get_project_or_local(
        project or ctx.obj.get("project"), is_cli=True
    )
    stage_project_version(
        owner=owner,
        project_name=project_name,
        kind=V1ProjectVersionKind.ARTIFACT,
        version=version,
        to=to,
        message=message,
    )


@artifacts.command()
@click.option(*OPTIONS_PROJECT["args"], **OPTIONS_PROJECT["kwargs"])
@click.option(*OPTIONS_ARTIFACT_VERSION["args"], **OPTIONS_ARTIFACT_VERSION["kwargs"])
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
    help="Print the url of the dashboard for this artifact version.",
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
        kind=V1ProjectVersionKind.ARTIFACT,
        version=version,
        url=url,
        yes=yes,
    )
