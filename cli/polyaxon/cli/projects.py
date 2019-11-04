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

from polyaxon_sdk import V1Project
from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon.cli.errors import handle_cli_error
from polyaxon.cli.getters.project import get_project_or_local
from polyaxon.cli.init import init as init_project
from polyaxon.client import PolyaxonClient
from polyaxon.logger import clean_outputs
from polyaxon.managers.auth import AuthConfigManager
from polyaxon.managers.project import ProjectManager
from polyaxon.utils.formatting import (
    Printer,
    dict_tabulate,
    dict_to_tabulate,
    get_meta_response,
    list_dicts_to_tabulate,
)
from polyaxon.utils.query_params import get_query_params


def get_project_details(project):
    if project.description:
        Printer.print_header("Project description:")
        click.echo("{}\n".format(project.description))

    response = dict_to_tabulate(
        project.to_dict(), humanize_values=True, exclude_attrs=["description"]
    )

    Printer.print_header("Project info:")
    dict_tabulate(response)


@click.group()
@click.option("--project", "-p", type=str)
@click.pass_context
@clean_outputs
def projects(ctx, project):  # pylint:disable=redefined-outer-name
    """Commands for projects."""
    if ctx.invoked_subcommand not in ["create", "list"]:
        ctx.obj = ctx.obj or {}
        ctx.obj["project"] = project


@projects.command()
@click.option(
    "--name",
    required=True,
    type=str,
    help="Name of the project, must be unique for the owner namespace.",
)
@click.option(
    "--owner",
    type=str,
    help="Name of the owner/namespace, "
    "if not provided it will default to the namespace of the current user.",
)
@click.option("--description", type=str, help="Description of the project.")
@click.option(
    "--private", is_flag=True, help="Set the visibility of the project to private."
)
@click.option("--init", is_flag=True, help="Initialize the project after creation.")
@click.pass_context
@clean_outputs
def create(ctx, name, owner, description, private, init):
    """Create a new project.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon project create --name=cats-vs-dogs --description="Image Classification with DL"
    ```
    """
    owner = owner or AuthConfigManager.get_value("username")

    if not owner:
        Printer.print_error(
            "Please login first or provide a valid owner --owner. "
            "`polyaxon login --help`"
        )
        sys.exit(1)

    try:
        polyaxon_client = PolyaxonClient()
        project_config = V1Project(
            name=name, description=description, is_public=not private
        )
        _project = polyaxon_client.projects_v1.create_project(owner, project_config)
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not create project `{}`.".format(name))
        sys.exit(1)

    Printer.print_success(
        "Project `{}` was created successfully.".format(_project.name)
    )

    if init:
        ctx.obj = {}
        ctx.invoke(init_project, project=name)


@projects.command()
@click.option(
    "--owner",
    type=str,
    help="Name of the owner/namespace, "
    "if not provided it will default to the namespace of the current user.",
)
@click.option("--limit", type=int, help="To limit the list of projects.")
@click.option("--offset", type=int, help="To offset the list of projects.")
@clean_outputs
def ls(owner, limit, offset):
    """List projects.

    Uses [Caching](/references/polyaxon-cli/#caching)
    """
    owner = owner or AuthConfigManager.get_value("username")
    if not owner:
        Printer.print_error(
            "Please login first or provide a valid owner --owner. "
            "`polyaxon login --help`"
        )
        sys.exit(1)

    try:
        params = get_query_params(limit=limit, offset=offset)
        polyaxon_client = PolyaxonClient()
        response = polyaxon_client.projects_v1.list_projects(owner, **params)
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
        exclude_attrs=["uuid", "description"],
    )
    if objects:
        Printer.print_header("Projects:")
        dict_tabulate(objects, is_list_dict=True)


@projects.command()
@click.pass_context
@clean_outputs
def get(ctx):
    """Get info for current project, by project_name, or user/project_name.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    To get current project:

    \b
    ```bash
    $ polyaxon project get
    ```

    To get a project by name

    \b
    ```bash
    $ polyaxon project get user/project
    ```
    """
    owner, project_name = get_project_or_local(ctx.obj.get("project"))

    try:
        polyaxon_client = PolyaxonClient()
        response = polyaxon_client.projects_v1.get_project(owner, project_name)
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not get project `{}`.".format(project_name))
        sys.exit(1)

    get_project_details(response)


@projects.command()
@click.pass_context
@clean_outputs
def delete(ctx):
    """Delete project.

    Uses [Caching](/references/polyaxon-cli/#caching)
    """
    owner, project_name = get_project_or_local(ctx.obj.get("project"))

    if not click.confirm(
        "Are sure you want to delete project `{}/{}`".format(owner, project_name)
    ):
        click.echo("Existing without deleting project.")
        sys.exit(1)

    try:
        polyaxon_client = PolyaxonClient()
        response = polyaxon_client.projects_v1.delete_project(owner, project_name)
        local_project = ProjectManager.get_config()
        if local_project and (owner, project_name) == (
            local_project.user,
            local_project.name,
        ):
            # Purge caching
            ProjectManager.purge()
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not delete project `{}/{}`.".format(owner, project_name)
        )
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success(
            "Project `{}/{}` was delete successfully".format(owner, project_name)
        )


@projects.command()
@click.option(
    "--name", type=str, help="Name of the project, must be unique for the same user."
)
@click.option("--description", type=str, help="Description of the project.")
@click.option(
    "--private", type=bool, help="Set the visibility of the project to private/public."
)
@click.pass_context
@clean_outputs
def update(ctx, name, description, private):
    """Update project.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon update foobar --description="Image Classification with DL using TensorFlow"
    ```

    \b
    ```bash
    $ polyaxon update mike1/foobar --description="Image Classification with DL using TensorFlow"
    ```

    \b
    ```bash
    $ polyaxon update --tags="foo, bar"
    ```
    """
    owner, project_name = get_project_or_local(ctx.obj.get("project"))

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
        polyaxon_client = PolyaxonClient()
        response = polyaxon_client.projects_v1.patch_project(
            owner, project_name, update_dict
        )
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not update project `{}`.".format(project_name)
        )
        sys.exit(1)

    Printer.print_success("Project updated.")
    get_project_details(response)


@projects.command()
@click.option("--url", type=str, help="The url of the git repo.")
@click.option(
    "--private", is_flag=True, help="Set the visibility of the repo to private."
)
@click.option(
    "--sync", is_flag=True, help="Sync and fetch latest repo changes on Polyaxon."
)
@click.pass_context
@clean_outputs
def git(ctx, url, private, sync):  # pylint:disable=assign-to-new-keyword
    """Set/Sync git repo on this project. TODO

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon project git --url=https://github.com/polyaxon/polyaxon-quick-start
    ```

    \b
    ```bash
    $ polyaxon project git --url=https://github.com/polyaxon/polyaxon-quick-start --private
    ```
    """
    user, project_name = get_project_or_local(ctx.obj.get("project"))

    def git_set_url():
        if private:
            click.echo(
                '\nSetting a private git repo "{}" on project: {} ...\n'.format(
                    url, project_name
                )
            )
        else:
            click.echo(
                '\nSetting a public git repo "{}" on project: {} ...\n'.format(
                    url, project_name
                )
            )

        try:
            PolyaxonClient().projects_v1.set_repo(user, project_name, url, not private)
        except (ApiException, HTTPError) as e:
            handle_cli_error(
                e,
                message="Could not set git repo on project `{}`.".format(project_name),
            )
            sys.exit(1)

        Printer.print_success(
            "Project was successfully initialized with `{}`.".format(url)
        )

    def git_sync_repo():
        try:
            response = PolyaxonClient().projects_v1.sync_repo(user, project_name)
        except (ApiException, HTTPError) as e:
            handle_cli_error(
                e,
                message="Could not sync git repo on project `{}`.".format(project_name),
            )
            sys.exit(1)

        click.echo(response.status_code)
        Printer.print_success("Project was successfully synced with latest changes.")

    if url:
        git_set_url()
    if sync:
        git_sync_repo()


@projects.command()
@click.option("--enable", is_flag=True, help="Enable CI on this project.")
@click.option("--disable", is_flag=True, help="Disable CI on this project.")
@click.pass_context
@clean_outputs
def ci(ctx, enable, disable):  # pylint:disable=assign-to-new-keyword
    """Enable/Disable CI on this project.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon project ci --enable
    ```

    \b
    ```bash
    $ polyaxon project ci --disable
    ```
    """
    owner, project_name = get_project_or_local(ctx.obj.get("project"))

    polyaxon_client = PolyaxonClient()

    def enable_ci():
        try:
            polyaxon_client.projects_v1.enable_ci(owner, project_name)
        except (ApiException, HTTPError) as e:
            handle_cli_error(
                e, message="Could not enable CI on project `{}`.".format(project_name)
            )
            sys.exit(1)

        Printer.print_success(
            "Polyaxon CI was successfully enabled on project: `{}`.".format(
                project_name
            )
        )

    def disable_ci():
        try:
            polyaxon_client.projects_v1.disable_ci(owner, project_name)
        except (ApiException, HTTPError) as e:
            handle_cli_error(
                e, message="Could not disable CI on project `{}`.".format(project_name)
            )
            sys.exit(1)

        Printer.print_success(
            "Polyaxon CI was successfully disabled on project: `{}`.".format(
                project_name
            )
        )

    if enable:
        enable_ci()
    if disable:
        disable_ci()


@projects.command()
@click.option("--commit", "-c", type=str, help="The Commit to download.")
@click.pass_context
@clean_outputs
def download(ctx, commit):
    """Download code of the current project."""
    user, project_name = get_project_or_local(ctx.obj.get("project"))
    try:
        polyaxon_client = PolyaxonClient()
        polyaxon_client.projects_v1.download_repo(user, project_name, commit=commit)
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not download code for project `{}`.".format(project_name)
        )
        sys.exit(1)
    Printer.print_success("Files downloaded.")


@projects.command()
@click.pass_context
@clean_outputs
def bookmark(ctx):
    """Bookmark project.

    Uses [Caching](/references/polyaxon-cli/#caching)
    """
    owner, project_name = get_project_or_local(ctx.obj.get("project"))

    try:
        polyaxon_client = PolyaxonClient()
        polyaxon_client.projects_v1.bookmark_project(owner, project_name)
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not bookmark project `{}/{}`.".format(owner, project_name)
        )
        sys.exit(1)

    Printer.print_success("Project `{}/{}` is bookmarked.".format(owner, project_name))


@projects.command()
@click.pass_context
@clean_outputs
def unbookmark(ctx):
    """Unbookmark project.

    Uses [Caching](/references/polyaxon-cli/#caching)
    """
    owner, project_name = get_project_or_local(ctx.obj.get("project"))

    try:
        polyaxon_client = PolyaxonClient()
        polyaxon_client.projects_v1.unbookmark_project(owner, project_name)
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e,
            message="Could not unbookmark project `{}/{}`.".format(owner, project_name),
        )
        sys.exit(1)

    Printer.print_success(
        "Project `{}/{}` is unbookmarked.".format(owner, project_name)
    )


@projects.command()
@click.pass_context
@clean_outputs
def invalidate_runs(ctx):
    """Invalidate runs' cache inside this project.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon invalidate_builds
    ```
    """
    owner, project_name = get_project_or_local(ctx.obj.get("project"))

    try:
        polyaxon_client = PolyaxonClient()
        polyaxon_client.projects_v1.invalidate_builds(owner, project_name)
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e,
            message="Could not invalidate build jobs for project `{}`.".format(
                project_name
            ),
        )
        sys.exit(1)

    Printer.print_success(
        "Build jobs have being invalidated for project `{}`.".format(project_name)
    )
