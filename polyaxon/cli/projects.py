# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from marshmallow import ValidationError
from polyaxon_sdk.rest import ApiException

from polyaxon.cli.getters.project import get_project_or_local
from polyaxon.cli.init import init as init_project
from polyaxon.client import PolyaxonClient
from polyaxon.logger import clean_outputs
from polyaxon.managers.auth import AuthConfigManager
from polyaxon.managers.project import ProjectManager
from polyaxon.schemas.api.project import ProjectConfig
from polyaxon.utils.formatting import (
    Printer,
    dict_tabulate,
    get_runs_with_inputs,
    get_runs_with_outputs,
    get_meta_response,
    list_dicts_to_tabulate,
)
from polyaxon.utils.validation import validate_tags


def get_project_details(project):
    if project.description:
        Printer.print_header("Project description:")
        click.echo("{}\n".format(project.description))

    response = project.to_light_dict(
        humanize_values=True,
        exclude_attrs=["uuid", "runs", "description"],
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
def create(ctx, name, owner, description, tags, private, init):
    """Create a new project.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon project create --name=cats-vs-dogs --description="Image Classification with DL"
    ```
    """
    owner = owner or AuthConfigManager.get_value("username")
    try:
        tags = tags.split(",") if tags else None
        project_dict = dict(
            name=name, description=description, is_public=not private, tags=tags
        )
        project_config = ProjectConfig.from_dict(project_dict)
    except ValidationError:
        Printer.print_error(
            'Project name should contain only alpha numerical, "-", and "_".'
        )
        sys.exit(1)

    try:
        polyaxon_client = PolyaxonClient()
        _project = polyaxon_client.project_service.create_project(owner, project_config)
    except ApiException as e:
        Printer.print_error("Could not create project `{}`.".format(name))
        Printer.print_error("Error message `{}`.".format(e))
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
@click.option("--page", type=int, help="To paginate through the list of projects.")
@clean_outputs
def list(owner, page):  # pylint:disable=redefined-builtin
    """List projects.

    Uses [Caching](/references/polyaxon-cli/#caching)
    """
    owner = owner or AuthConfigManager.get_value("username")
    if not owner:
        Printer.print_error("Please login first. `polyaxon login --help`")

    page = page or 1
    try:
        polyaxon_client = PolyaxonClient()
        response = polyaxon_client.project_service.list_projects(owner, page=page)
    except ApiException as e:
        Printer.print_error("Could not get list of projects.")
        Printer.print_error("Error message `{}`.".format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header("Projects for current user")
        Printer.print_header("Navigation:")
        dict_tabulate(meta)
    else:
        Printer.print_header("No projects found for current user")

    objects = list_dicts_to_tabulate(
        [
            o.to_light_dict(
                humanize_values=True,
                exclude_attrs=[
                    "uuid",
                    "experiment_groups",
                    "experiments",
                    "description",
                    "num_experiments",
                    "num_independent_experiments",
                    "num_experiment_groups",
                    "num_jobs",
                    "num_builds",
                    "unique_name",
                ],
            )
            for o in response["results"]
        ]
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
        response = polyaxon_client.project_service.get_project(owner, project_name)
    except ApiException as e:
        Printer.print_error("Could not get project `{}`.".format(project_name))
        Printer.print_error("Error message `{}`.".format(e))
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
        response = polyaxon_client.project_service.delete_project(owner, project_name)
        local_project = ProjectManager.get_config()
        if local_project and (owner, project_name) == (
            local_project.user,
            local_project.name,
        ):
            # Purge caching
            ProjectManager.purge()
    except ApiException as e:
        Printer.print_error(
            "Could not delete project `{}/{}`.".format(owner, project_name)
        )
        Printer.print_error("Error message `{}`.".format(e))
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
@click.option("--tags", type=str, help="Tags, comma separated values, of the project.")
@click.option(
    "--private", type=bool, help="Set the visibility of the project to private/public."
)
@click.pass_context
@clean_outputs
def update(ctx, name, description, tags, private):
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

    tags = validate_tags(tags)
    if tags:
        update_dict["tags"] = tags

    if not update_dict:
        Printer.print_warning("No argument was provided to update the project.")
        sys.exit(1)

    try:
        polyaxon_client = PolyaxonClient()
        response = polyaxon_client.project_service.update_project(
            owner, project_name, update_dict
        )
    except ApiException as e:
        Printer.print_error("Could not update project `{}`.".format(project_name))
        Printer.print_error("Error message `{}`.".format(e))
        sys.exit(1)

    Printer.print_success("Project updated.")
    get_project_details(response)


@projects.command()
@click.option(
    "--io", "-io",
    is_flag=True,
    help="List runs with their inputs/outputs (params, metrics, results, ...)."
)
@click.option(
    "--query",
    "-q",
    type=str,
    help="To filter the runs based on this query spec.",
)
@click.option("--sort", "-s", type=str, help="To change order by of the runs.")
@click.option("--page", type=int, help="To paginate through the list of runs.")
@click.pass_context
@clean_outputs
@clean_outputs
def runs(ctx, io, query, sort, page):
    """List runs for this project.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    Get all runs:

    \b
    ```bash
    $ polyaxon project runs
    ```

    Get all runs with with status {created or running}, and
    creation date between 2018-01-01 and 2018-01-02, and params activation equal to sigmoid
    and metric loss less or equal to 0.2

    \b
    ```bash
    $ polyaxon project runs \
      -q "status:created|running, started_at:2018-01-01..2018-01-02, \
          params.activation:sigmoid, metric.loss:<=0.2"
    ```

    Get all runs sorted by update date

    \b
    ```bash
    $ polyaxon project runs -s "-updated_at"
    ```
    """
    user, project_name = get_project_or_local(ctx.obj.get("project"))

    page = page or 1
    try:
        polyaxon_client = PolyaxonClient()
        response = polyaxon_client.project_service.list_runs(
            username=user,
            project_name=project_name,
            query=query,
            sort=sort,
            page=page,
        )
    except ApiException as e:
        Printer.print_error(
            "Could not get runs for project `{}`.".format(project_name)
        )
        Printer.print_error("Error message `{}`.".format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header(
            "Experiments for project `{}/{}`.".format(user, project_name)
        )
        Printer.print_header("Navigation:")
        dict_tabulate(meta)
    else:
        Printer.print_header(
            "No runs found for project `{}/{}`.".format(user, project_name)
        )

    if io:
        objects = get_runs_with_outputs(response)
        objects = get_runs_with_inputs(response)
    else:
        objects = [
            Printer.add_status_color(o.to_light_dict(humanize_values=True))
            for o in response["results"]
        ]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Experiments:")
        objects.pop("project_name", None)
        dict_tabulate(objects, is_list_dict=True)


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
            PolyaxonClient().project.set_repo(user, project_name, url, not private)
        except ApiException as e:
            Printer.print_error(
                "Could not set git repo on project `{}`.".format(project_name)
            )
            Printer.print_error("Error message `{}`.".format(e))
            sys.exit(1)

        Printer.print_success(
            "Project was successfully initialized with `{}`.".format(url)
        )

    def git_sync_repo():
        try:
            response = PolyaxonClient().project.sync_repo(user, project_name)
        except ApiException as e:
            Printer.print_error(
                "Could not sync git repo on project `{}`.".format(project_name)
            )
            Printer.print_error("Error message `{}`.".format(e))
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
            polyaxon_client.project_service.enable_ci(owner, project_name)
        except ApiException as e:
            Printer.print_error(
                "Could not enable CI on project `{}`.".format(project_name)
            )
            Printer.print_error("Error message `{}`.".format(e))
            sys.exit(1)

        Printer.print_success(
            "Polyaxon CI was successfully enabled on project: `{}`.".format(
                project_name
            )
        )

    def disable_ci():
        try:
            polyaxon_client.project_service.disable_ci(owner, project_name)
        except ApiException as e:
            Printer.print_error(
                "Could not disable CI on project `{}`.".format(project_name)
            )
            Printer.print_error("Error message `{}`.".format(e))
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
        polyaxon_client.project_service.download_repo(user, project_name, commit=commit)
    except ApiException as e:
        Printer.print_error(
            "Could not download code for project `{}`.".format(project_name)
        )
        Printer.print_error("Error message `{}`.".format(e))
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
        polyaxon_client.project_service.bookmark_project(owner, project_name)
    except ApiException as e:
        Printer.print_error(
            "Could not bookmark project `{}/{}`.".format(owner, project_name)
        )
        Printer.print_error("Error message `{}`.".format(e))
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
        polyaxon_client.project_service.unbookmark(owner, project_name)
    except ApiException as e:
        Printer.print_error(
            "Could not unbookmark project `{}/{}`.".format(owner, project_name)
        )
        Printer.print_error("Error message `{}`.".format(e))
        sys.exit(1)

    Printer.print_success("Project `{}/{}` is unbookmarked.".format(owner, project_name))


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
        polyaxon_client.project_service.invalidate_builds(owner, project_name)
    except ApiException as e:
        Printer.print_error(
            "Could not invalidate build jobs for project `{}`.".format(project_name)
        )
        Printer.print_error("Error message `{}`.".format(e))
        sys.exit(1)

    Printer.print_success(
        "Build jobs have being invalidated for project `{}`.".format(project_name)
    )
