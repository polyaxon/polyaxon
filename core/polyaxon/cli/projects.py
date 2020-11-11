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

from polyaxon_sdk import V1Project
from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon import settings
from polyaxon.cli.dashboard import get_dashboard_url
from polyaxon.cli.errors import handle_cli_error
from polyaxon.cli.init import init as init_project
from polyaxon.cli.options import OPTIONS_OWNER, OPTIONS_PROJECT
from polyaxon.client import ProjectClient
from polyaxon.constants import DEFAULT
from polyaxon.env_vars.getters import get_project_or_local
from polyaxon.managers.project import ProjectConfigManager
from polyaxon.utils import cache
from polyaxon.utils.formatting import (
    Printer,
    dict_tabulate,
    dict_to_tabulate,
    get_meta_response,
    list_dicts_to_tabulate,
)
from polyaxon.utils.validation import validate_tags


def get_project_details(_project):
    if _project.description:
        Printer.print_header("Project description:")
        click.echo("{}\n".format(_project.description))

    response = dict_to_tabulate(
        _project.to_dict(), humanize_values=True, exclude_attrs=["description"]
    )

    Printer.print_header("Project info:")
    dict_tabulate(response)


@click.group()
@click.option(*OPTIONS_PROJECT["args"], "_project", **OPTIONS_PROJECT["kwargs"])
@click.pass_context
def project(ctx, _project):  # pylint:disable=redefined-outer-name
    """Commands for projects."""
    if _project:
        Printer.print_warning(
            "Passing arguments to command groups is deprecated and will be removed in v1.2! "
            "Please use arguments on the sub-command directly: "
            "`polyaxon project SUB_COMMAND --help`"
        )
    if ctx.invoked_subcommand not in ["create", "ls"]:
        ctx.obj = ctx.obj or {}
        ctx.obj["project"] = _project


@project.command()
@click.option(
    "--name", type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'."
)
@click.option("--description", type=str, help="Description of the project.")
@click.option("--tags", type=str, help="Tags of the project, comma separated values.")
@click.option(
    "--public", is_flag=True, help="Set the visibility of the project to public."
)
@click.option("--init", is_flag=True, help="Initialize the project after creation.")
@click.pass_context
def create(ctx, name, description, tags, public, init):
    """Create a new project.

    Uses /docs/core/cli/#caching

    Example:

    \b
    $ polyaxon project create --project=cats-vs-dogs --description="Image Classification with DL"

    \b
    $ polyaxon project create --project=owner/name --description="Project Description"
    """
    if not name:
        Printer.print_error(
            "Please login provide a name to create a project.",
            command_help="project create",
            sys_exit=True,
        )
    owner, project_name = get_project_or_local(
        name or ctx.obj.get("project"), is_cli=True
    )
    owner = owner or settings.AUTH_CONFIG.username
    if not owner and (not settings.CLI_CONFIG or settings.CLI_CONFIG.is_ce):
        owner = DEFAULT

    tags = validate_tags(tags)

    if not owner:
        Printer.print_error(
            "Please login first or provide a valid name with owner --name=owner/project. "
            "`polyaxon login --help`"
        )
        sys.exit(1)

    try:
        project_config = V1Project(
            name=project_name, description=description, tags=tags, is_public=public
        )
        polyaxon_client = ProjectClient(owner=owner)
        _project = polyaxon_client.create(project_config)
        config = polyaxon_client.client.sanitize_for_serialization(_project)
        cache.cache(config_manager=ProjectConfigManager, config=config)
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not create project `{}`.".format(project_name)
        )
        sys.exit(1)

    Printer.print_success(
        "Project `{}` was created successfully.".format(_project.name)
    )
    click.echo(
        "You can view this project on Polyaxon UI: {}".format(
            get_dashboard_url(subpath="{}/{}".format(owner, _project.name))
        )
    )

    if init:
        ctx.obj = {}
        ctx.invoke(init_project, project="{}/{}".format(owner, project_name))


@project.command()
@click.option(*OPTIONS_OWNER["args"], **OPTIONS_OWNER["kwargs"])
@click.option(
    "--query", "-q", type=str, help="To filter the projects based on this query spec."
)
@click.option(
    "--sort", "-s", type=str, help="To order the projects based on the sort spec."
)
@click.option("--limit", type=int, help="To limit the list of projects.")
@click.option("--offset", type=int, help="To offset the list of projects.")
def ls(owner, query, sort, limit, offset):
    """List projects.

    Uses /docs/core/cli/#caching
    """
    owner = owner or settings.AUTH_CONFIG.username
    if not owner and (not settings.CLI_CONFIG or settings.CLI_CONFIG.is_ce):
        owner = DEFAULT
    if not owner:
        Printer.print_error(
            "Please login first or provide a valid owner --owner. "
            "`polyaxon login --help`"
        )
        sys.exit(1)

    try:
        polyaxon_client = ProjectClient(owner=owner)
        response = polyaxon_client.list(
            limit=limit, offset=offset, query=query, sort=sort
        )
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not get list of projects.")
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header("Projects for current user")
        Printer.print_header("Navigation:")
        dict_tabulate(meta)
    else:
        Printer.print_header("No projects found for current user")

    objects = list_dicts_to_tabulate(
        [o.to_dict() for o in response.results],
        humanize_values=True,
        exclude_attrs=[
            "uuid",
            "readme",
            "description",
            "owner",
            "user_email",
            "teams",
            "role",
            "settings",
        ],
    )
    if objects:
        Printer.print_header("Projects:")
        dict_tabulate(objects, is_list_dict=True)


@project.command()
@click.option(*OPTIONS_PROJECT["args"], "_project", **OPTIONS_PROJECT["kwargs"])
@click.pass_context
def get(ctx, _project):
    """Get info for current project, by project_name, or owner/project_name.

    Uses /docs/core/cli/#caching

    Examples:

    To get current project:

    \b
    $ polyaxon project get

    To get a project by name

    \b
    $ polyaxon project get -p owner/project
    """
    owner, project_name = get_project_or_local(
        _project or ctx.obj.get("project"), is_cli=True
    )

    try:
        polyaxon_client = ProjectClient(owner=owner, project=project_name)
        polyaxon_client.refresh_data()
        config = polyaxon_client.client.sanitize_for_serialization(
            polyaxon_client.project_data
        )
        cache.cache(
            config_manager=ProjectConfigManager,
            config=config,
            owner=owner,
            project=project_name,
        )
        get_project_details(polyaxon_client.project_data)
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not get project `{}`.".format(project_name), sys_exit=True
        )


@project.command()
@click.option(*OPTIONS_PROJECT["args"], "_project", **OPTIONS_PROJECT["kwargs"])
@click.pass_context
def delete(ctx, _project):
    """Delete project.

    Uses /docs/core/cli/#caching
    """
    owner, project_name = get_project_or_local(
        _project or ctx.obj.get("project"), is_cli=True
    )

    if not click.confirm(
        "Are sure you want to delete project `{}/{}`".format(owner, project_name)
    ):
        click.echo("Existing without deleting project.")
        sys.exit(1)

    try:
        polyaxon_client = ProjectClient(owner=owner, project=project_name)
        polyaxon_client.delete()
        try:
            local_project = ProjectConfigManager.get_config()
        except TypeError:
            Printer.print_error(
                "Found an invalid project config or project config cache, "
                "if you are using Polyaxon CLI please run: "
                "`polyaxon config purge --cache-only`",
                sys_exit=True,
            )
        if local_project and (owner, project_name) == (
            local_project.user,
            local_project.name,
        ):
            # Purge caching
            ProjectConfigManager.purge()
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not delete project `{}/{}`.".format(owner, project_name)
        )
        sys.exit(1)

    Printer.print_success(
        "Project `{}/{}` was delete successfully".format(owner, project_name)
    )


@project.command()
@click.option(*OPTIONS_PROJECT["args"], "_project", **OPTIONS_PROJECT["kwargs"])
@click.option(
    "--name", type=str, help="Name of the project, must be unique for the same user."
)
@click.option("--description", type=str, help="Description of the project.")
@click.option(
    "--private", type=bool, help="Set the visibility of the project to private/public."
)
@click.pass_context
def update(ctx, _project, name, description, private):
    """Update project.

    Uses /docs/core/cli/#caching

    Example:

    \b
    $ polyaxon update foobar --description="Image Classification with DL using TensorFlow"

    \b
    $ polyaxon update mike1/foobar --description="Image Classification with DL using TensorFlow"

    \b
    $ polyaxon update --tags="foo, bar"
    """
    owner, project_name = get_project_or_local(
        _project or ctx.obj.get("project"), is_cli=True
    )

    update_dict = {}
    if name:
        update_dict["name"] = name

    if description:
        update_dict["description"] = description

    if private is not None:
        update_dict["is_public"] = not private

    if not update_dict:
        Printer.print_warning("No argument was provided to update the project.")
        sys.exit(1)

    try:
        polyaxon_client = ProjectClient(owner=owner)
        response = polyaxon_client.update(update_dict)
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not update project `{}`.".format(project_name)
        )
        sys.exit(1)

    Printer.print_success("Project updated.")
    get_project_details(response)


@project.command()
@click.option(*OPTIONS_PROJECT["args"], "_project", **OPTIONS_PROJECT["kwargs"])
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
    help="Print the url of the dashboard for this project.",
)
@click.pass_context
def dashboard(ctx, _project, yes, url):
    """Open this operation's dashboard details in browser."""
    owner, project_name = get_project_or_local(
        _project or ctx.obj.get("project"), is_cli=True
    )
    project_url = get_dashboard_url(subpath="{}/{}".format(owner, project_name))
    if url:
        Printer.print_header("The dashboard is available at: {}".format(project_url))
        sys.exit(0)
    if not yes:
        click.confirm(
            "Dashboard page will now open in your browser. Continue?",
            abort=True,
            default=True,
        )
    click.launch(project_url)
