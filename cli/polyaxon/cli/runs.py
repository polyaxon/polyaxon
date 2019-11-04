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
import rhea

from polyaxon_sdk import V1Run
from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon.cli.errors import handle_cli_error
from polyaxon.cli.getters.project import get_project_or_local
from polyaxon.cli.getters.run import get_project_run_or_local
from polyaxon.cli.upload import upload
from polyaxon.client import PolyaxonClient
from polyaxon.client.statuses import get_run_statuses
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.logger import clean_outputs
from polyaxon.managers.run import RunManager
from polyaxon.utils import cache
from polyaxon.utils.formatting import (
    Printer,
    dict_tabulate,
    dict_to_tabulate,
    get_meta_response,
    get_runs_with_keys,
    list_dicts_to_tabulate,
)
from polyaxon.utils.log_handler import get_logs_handler
from polyaxon.utils.query_params import get_query_params
from polyaxon.utils.validation import validate_tags


def get_run_details(run):  # pylint:disable=redefined-outer-name
    if run.description:
        Printer.print_header("Run description:")
        click.echo("{}\n".format(run.description))

    if run.inputs:
        Printer.print_header("Run inputs:")
        dict_tabulate(run.inputs)

    if run.outputs:
        Printer.print_header("Run inputs:")
        dict_tabulate(run.outputs)

    response = Printer.add_status_color(run.to_dict())
    response = dict_to_tabulate(
        response,
        humanize_values=True,
        exclude_attrs=[
            "project",
            "description",
            "readme",
            "content",
            "inputs",
            "outputs",
            "run_env",
            "is_managed",
        ],
    )

    Printer.print_header("Run info:")
    dict_tabulate(response)


@click.group()
@click.option(
    "--project", "-p", type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'."
)
@click.option("--uid", "-uid", type=str, help="The run uuid.")
@click.pass_context
@clean_outputs
def runs(ctx, project, uid):
    """Commands for runs."""
    ctx.obj = ctx.obj or {}
    ctx.obj["project"] = project
    if ctx.invoked_subcommand not in ["list"]:
        ctx.obj["run_uuid"] = uid


@runs.command()
@click.option(
    "--io",
    "-io",
    is_flag=True,
    help="List runs with their inputs/outputs (params, metrics, results, ...).",
)
@click.option(
    "--query", "-q", type=str, help="To filter the runs based on this query spec."
)
@click.option("--sort", "-s", type=str, help="To change order by of the runs.")
@click.option("--limit", type=int, help="To limit the list of runs.")
@click.option("--offset", type=int, help="To offset the list of runs.")
@click.pass_context
@clean_outputs
@clean_outputs
def ls(ctx, io, query, sort, limit, offset):
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
    owner, project_name = get_project_or_local(ctx.obj.get("project"))

    try:
        polyaxon_client = PolyaxonClient()
        params = get_query_params(limit=limit, offset=offset, query=query, sort=sort)
        response = polyaxon_client.runs_v1.list_runs(
            owner=owner, project=project_name, **params
        )
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not get runs for project `{}`.".format(project_name)
        )
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header(
            "Experiments for project `{}/{}`.".format(owner, project_name)
        )
        Printer.print_header("Navigation:")
        dict_tabulate(meta)
    else:
        Printer.print_header(
            "No runs found for project `{}/{}`.".format(owner, project_name)
        )

    objects = [Printer.add_status_color(o.to_dict()) for o in response.results]

    if io:
        objects = get_runs_with_keys(objects=objects, params_keys=["inputs", "outputs"])
        objects = list_dicts_to_tabulate(
            objects,
            exclude_attrs=[
                "owner",
                "project",
                "description",
                "content",
                "deleted",
                "readme",
                "run_env",
            ],
        )
    else:
        objects = list_dicts_to_tabulate(
            objects,
            exclude_attrs=[
                "owner",
                "project",
                "description",
                "content",
                "deleted",
                "readme",
                "run_env",
                "inputs",
                "outputs",
            ],
        )
    if objects:
        Printer.print_header("Runs:")
        objects.pop("project_name", None)
        dict_tabulate(objects, is_list_dict=True)


@runs.command()
@click.pass_context
@clean_outputs
def get(ctx):
    """Get run.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples for getting a run:

    \b
    ```bash
    $ polyaxon runs get  # if run is cached
    ```

    \b
    ```bash
    $ polyaxon runs --uid=8aac02e3a62a4f0aaa257c59da5eab80 get  # project is cached
    ```

    \b
    ```bash
    $ polyaxon runs --project=cats-vs-dogs -id 8aac02e3a62a4f0aaa257c59da5eab80 get
    ```

    \b
    ```bash
    $ polyaxon runs -p alain/cats-vs-dogs --uid=8aac02e3a62a4f0aaa257c59da5eab80 get
    ```
    """

    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid")
    )

    try:
        polyaxon_client = PolyaxonClient()
        response = polyaxon_client.runs_v1.get_run(owner, project_name, run_uuid)
        config = polyaxon_client.api_client.sanitize_for_serialization(response)
        cache.cache(config_manager=RunManager, response=config)
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not load run `{}` info.".format(run_uuid))
        sys.exit(1)

    get_run_details(response)


@runs.command()
@click.pass_context
@clean_outputs
def delete(ctx):
    """Delete a run.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon runs delete
    ```

    \b
    ```bash
    $ polyaxon runs --uid=8aac02e3a62a4f0aaa257c59da5eab80 delete  # project is cached
    ```

    \b
    ```bash
    $ polyaxon runs --project=cats-vs-dogs -id 8aac02e3a62a4f0aaa257c59da5eab80 delete
    ```
    """
    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid")
    )
    if not click.confirm("Are sure you want to delete run `{}`".format(run_uuid)):
        click.echo("Existing without deleting the run.")
        sys.exit(1)

    try:
        polyaxon_client = PolyaxonClient()
        polyaxon_client.runs_v1.delete_run(owner, project_name, run_uuid)
        # Purge caching
        RunManager.purge()
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not delete run `{}`.".format(run_uuid))
        sys.exit(1)

    Printer.print_success("Run `{}` was delete successfully".format(run_uuid))


@runs.command()
@click.option("--name", type=str, help="Name of the run (optional).")
@click.option("--description", type=str, help="Description of the run (optional).")
@click.option(
    "--tags", type=str, help="Tags of the run, comma separated values (optional)."
)
@click.pass_context
@clean_outputs
def update(ctx, name, description, tags):
    """Update run.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon runs --uid=8aac02e3a62a4f0aaa257c59da5eab80 update
    --description="new description for my runs"
    ```

    \b
    ```bash
    $ polyaxon runs --project=cats-vs-dogs -id 8aac02e3a62a4f0aaa257c59da5eab80 update
    --tags="foo, bar" --name="unique-name"
    ```
    """
    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid")
    )
    update_dict = {}

    if name:
        update_dict["name"] = name

    if description:
        update_dict["description"] = description

    tags = validate_tags(tags)
    if tags:
        update_dict["tags"] = tags

    if not update_dict:
        Printer.print_warning("No argument was provided to update the run.")
        sys.exit(0)

    try:
        polyaxon_client = PolyaxonClient()
        response = polyaxon_client.runs_v1.patch_run(
            owner, project_name, run_uuid, update_dict
        )
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not update run `{}`.".format(run_uuid))
        sys.exit(1)

    Printer.print_success("Run updated.")
    get_run_details(response)


@runs.command()
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Automatic yes to prompts. "
    'Assume "yes" as answer to all prompts and run non-interactively.',
)
@click.pass_context
@clean_outputs
def stop(ctx, yes):
    """Stop run.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon runs stop
    ```

    \b
    ```bash
    $ polyaxon runs --uid=8aac02e3a62a4f0aaa257c59da5eab80 stop
    ```
    """
    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid")
    )
    if not yes and not click.confirm(
        "Are sure you want to stop " "run `{}`".format(run_uuid)
    ):
        click.echo("Existing without stopping run.")
        sys.exit(0)

    try:
        polyaxon_client = PolyaxonClient()
        polyaxon_client.runs_v1.stop_run(owner, project_name, run_uuid)
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not stop run `{}`.".format(run_uuid))
        sys.exit(1)

    Printer.print_success("Run is being stopped.")


@runs.command()
@click.option(
    "--copy",
    "-c",
    is_flag=True,
    default=False,
    help="To copy the run before restarting.",
)
@click.option(
    "-f",
    "--file",
    "polyaxonfile",
    multiple=True,
    type=click.Path(exists=True),
    help="The polyaxonfiles to update with.",
)
@click.option(
    "-u", is_flag=True, default=False, help="To upload the repo before restarting."
)
@click.pass_context
@clean_outputs
def restart(ctx, copy, polyaxonfile, u):
    """Restart run.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon run --uid=8aac02e3a62a4f0aaa257c59da5eab80 restart
    ```
    """
    content = None
    if polyaxonfile:
        content = "{}".format(rhea.read(polyaxonfile))

    # Check if we need to upload
    if u:
        ctx.invoke(upload, sync=False)

    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid")
    )
    try:
        polyaxon_client = PolyaxonClient()
        body = V1Run(content=content)
        if copy:
            response = polyaxon_client.runs_v1.copy_run(
                owner, project_name, run_uuid, body
            )
            Printer.print_success("Run was copied with uid {}".format(response.uuid))
        else:
            response = polyaxon_client.runs_v1.restart_run(
                owner, project_name, run_uuid, body
            )
            Printer.print_success("Run was restarted with uid {}".format(response.uuid))
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not restart run `{}`.".format(run_uuid))
        sys.exit(1)


@runs.command()
@click.option(
    "-f",
    "--file",
    "polyaxonfile",
    multiple=True,
    type=click.Path(exists=True),
    help="The polyaxonfiles to update with.",
)
@click.option(
    "-u", is_flag=True, default=False, help="To upload the repo before resuming."
)
@click.pass_context
@clean_outputs
def resume(ctx, polyaxonfile, u):
    """Resume run.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon runs --uid=8aac02e3a62a4f0aaa257c59da5eab80 resume
    ```
    """
    content = None
    if polyaxonfile:
        content = "{}".format(rhea.read(polyaxonfile))

    # Check if we need to upload
    if u:
        ctx.invoke(upload, sync=False)

    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid")
    )
    try:
        polyaxon_client = PolyaxonClient()
        body = V1Run(content=content)
        response = polyaxon_client.runs_v1.resume_run(
            owner, project_name, run_uuid, body
        )
        Printer.print_success("Run was resumed with uid {}".format(response.uuid))
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not resume run `{}`.".format(run_uuid))
        sys.exit(1)


@runs.command()
@click.option("--watch", "-w", is_flag=True, help="Watch statuses.")
@click.pass_context
@clean_outputs
def statuses(ctx, watch):
    """Get run or run job statuses.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples getting run statuses:

    \b
    ```bash
    $ polyaxon runs statuses
    ```

    \b
    ```bash
    $ polyaxon runs -uid=8aac02e3a62a4f0aaa257c59da5eab80 statuses
    ```
    """

    def _get_run_statuses():
        try:
            for status, conditions in get_run_statuses(
                owner, project_name, run_uuid, watch
            ):
                if not conditions:
                    continue
                Printer.print_header("Latest status:")
                latest_status = Printer.add_status_color(
                    {"status": status}, status_key="status"
                )
                click.echo("{}\n".format(latest_status["status"]))

                objects = list_dicts_to_tabulate(
                    [
                        Printer.add_status_color(o.to_dict(), status_key="type")
                        for o in conditions
                    ]
                )
                if objects:
                    Printer.print_header("Conditions:")
                    dict_tabulate(objects, is_list_dict=True)
        except (ApiException, HTTPError, PolyaxonClientException) as e:
            handle_cli_error(
                e, message="Could get status for run `{}`.".format(run_uuid)
            )
            sys.exit(1)

    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid")
    )

    _get_run_statuses()


@runs.command()
@click.option("--gpu", "-g", is_flag=True, help="List run GPU resources.")
@click.pass_context
@clean_outputs
def resources(ctx, gpu):
    """Get run or run job resources.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples for getting run resources:

    \b
    ```bash
    $ polyaxon runs -uid=8aac02e3a62a4f0aaa257c59da5eab80 resources
    ```

    For GPU resources

    \b
    ```bash
    $ polyaxon runs -uid=8aac02e3a62a4f0aaa257c59da5eab80 resources --gpu
    ```
    """

    def get_run_resources():
        try:
            message_handler = Printer.gpu_resources if gpu else Printer.resources
            PolyaxonClient().run.resources(
                owner, project_name, run_uuid, message_handler=message_handler
            )
        except (ApiException, HTTPError) as e:
            handle_cli_error(
                e, message="Could not get resources for run `{}`.".format(run_uuid)
            )
            sys.exit(1)

    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid")
    )

    get_run_resources()


@runs.command()
@click.option("--past", "-p", is_flag=True, help="Show the past logs.")
@click.option(
    "--follow",
    "-f",
    is_flag=True,
    default=False,
    help="Stream logs after showing past logs.",
)
@click.option(
    "--hide_time",
    is_flag=True,
    default=False,
    help="Whether or not to hide timestamps from the log stream.",
)
@click.pass_context
@clean_outputs
def logs(ctx, past, follow, hide_time):
    """Get run or run job logs.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples for getting run logs:

    \b
    ```bash
    $ polyaxon run logs
    ```

    \b
    ```bash
    $ polyaxon runs -uid=8aac02e3a62a4f0aaa257c59da5eab80 -p mnist logs
    ```
    """

    def get_run_logs():
        if past:
            try:
                response = PolyaxonClient().run.logs(
                    owner, project_name, run_uuid, stream=False
                )
                get_logs_handler(
                    handle_job_info=True, show_timestamp=not hide_time, stream=False
                )(response.content.decode().split("\n"))
                print()

                if not follow:
                    return
            except (ApiException, HTTPError) as e:
                if not follow:
                    handle_cli_error(
                        e, message="Could not get logs for run `{}`.".format(run_uuid)
                    )
                    sys.exit(1)

        try:
            PolyaxonClient().run.logs(
                owner,
                project_name,
                run_uuid,
                message_handler=get_logs_handler(
                    handle_job_info=True, show_timestamp=not hide_time
                ),
            )
        except (ApiException, HTTPError) as e:
            handle_cli_error(
                e, message="Could not get logs for run `{}`.".format(run_uuid)
            )
            sys.exit(1)

    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid")
    )

    get_run_logs()


@runs.command()
@click.pass_context
@clean_outputs
def outputs(ctx):
    """Download outputs for run.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon runs -uid=8aac02e3a62a4f0aaa257c59da5eab80 outputs
    ```
    """
    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid")
    )
    try:
        PolyaxonClient().run.download_outputs(owner, project_name, run_uuid)
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not download outputs for run `{}`.".format(run_uuid)
        )
        sys.exit(1)
    Printer.print_success("Files downloaded.")


@runs.command()
@click.pass_context
@clean_outputs
def code(ctx):
    """Download code for run.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon runs -uid=8aac02e3a62a4f0aaa257c59da5eab80 code
    ```
    """
    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid")
    )
    try:
        polyaxon_client = PolyaxonClient()
        code_ref = polyaxon_client.runs_v1.get_run_code_refs(
            owner, project_name, run_uuid
        )
        commit = None
        if code_ref:
            commit = code_ref.commit
            Printer.print_header(
                "Run has code ref: `{}`, downloading ...".format(commit)
            )
        else:
            Printer.print_warning("Run has no code ref, downloading latest code...")
        PolyaxonClient().project.download_repo(owner, project_name, commit=commit)
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not download outputs for run `{}`.".format(run_uuid)
        )
        sys.exit(1)
    Printer.print_success("Files downloaded.")


@runs.command()
@click.pass_context
@clean_outputs
def bookmark(ctx):
    """Bookmark run.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon runs bookmark
    ```

    \b
    ```bash
    $ polyaxon runs -uid=8aac02e3a62a4f0aaa257c59da5eab80 bookmark
    ```
    """
    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid")
    )
    try:
        polyaxon_client = PolyaxonClient()
        polyaxon_client.runs_v1.bookmark_run(owner, project_name, run_uuid)
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not bookmark run `{}`.".format(run_uuid))
        sys.exit(1)

    Printer.print_success("Run is bookmarked.")


@runs.command()
@click.pass_context
@clean_outputs
def unbookmark(ctx):
    """Unbookmark run.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon runs unbookmark
    ```

    \b
    ```bash
    $ polyaxon runs -uid=8aac02e3a62a4f0aaa257c59da5eab80 unbookmark
    ```
    """
    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid")
    )
    try:
        polyaxon_client = PolyaxonClient()
        polyaxon_client.runs_v1.unbookmark_run(owner, project_name, run_uuid)
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not unbookmark run `{}`.".format(run_uuid))
        sys.exit(1)

    Printer.print_success("Run is unbookmarked.")
