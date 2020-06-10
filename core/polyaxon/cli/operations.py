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

from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon import settings
from polyaxon.api import REWRITE_SERVICES_V1, SERVICES_V1
from polyaxon.cli.errors import handle_cli_error
from polyaxon.cli.upload import upload
from polyaxon.client import RunClient
from polyaxon.client.run import get_run_logs
from polyaxon.config_reader.spec import ConfigSpec
from polyaxon.env_vars.getters import get_project_or_local, get_project_run_or_local
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.lifecycle import V1Statuses
from polyaxon.logger import clean_outputs
from polyaxon.managers.run import RunManager
from polyaxon.polyflow import V1RunKind
from polyaxon.utils import cache
from polyaxon.utils.formatting import (
    Printer,
    dict_tabulate,
    dict_to_tabulate,
    get_meta_response,
    get_runs_with_keys,
    list_dicts_to_tabulate,
)
from polyaxon.utils.validation import validate_tags


def get_run_details(run):  # pylint:disable=redefined-outer-name
    if run.description:
        Printer.print_header("Run description:")
        click.echo("{}\n".format(run.description))

    if run.inputs:
        Printer.print_header("Run inputs:")
        dict_tabulate(run.inputs)

    if run.outputs:
        Printer.print_header("Run outputs:")
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
def ops(ctx, project, uid):
    """Commands for ops/runs."""
    ctx.obj = ctx.obj or {}
    ctx.obj["project"] = project
    if ctx.invoked_subcommand not in ["ls"]:
        ctx.obj["run_uuid"] = uid


@ops.command()
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

    Uses /docs/core/cli/#caching

    Examples:

    Get all runs:

    \b

    Get all runs with with status {created or running}, and
    creation date between 2018-01-01 and 2018-01-02, and params activation equal to sigmoid
    and metric loss less or equal to 0.2

    \b
    $ polyaxon ops ls \
    -q "status:created|running, started_at:2018-01-01..2018-01-02, \
    params.activation:sigmoid, metric.loss:<=0.2"


    Get all runs sorted by update date:

    \b
    $ polyaxon ops ls -s "-updated_at"

    Get all runs of kind job:

    \b
    $ polyaxon ops ls -q "kind: job"

    Get all runs of kind service:

    \b
    $ polyaxon ops ls -q "kind: service"
    """
    owner, project_name = get_project_or_local(ctx.obj.get("project"), is_cli=True)

    try:
        polyaxon_client = RunClient(owner=owner, project=project_name)
        response = polyaxon_client.list(
            limit=limit, offset=offset, query=query, sort=sort
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
                "settings",
                "meta_info",
                "original",
                "pipeline",
                "role",
                "status_conditions",
                "is_helper",
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
                "inputs",
                "outputs",
                "settings",
                "meta_info",
                "original",
                "pipeline",
                "role",
                "status_conditions",
                "is_helper",
            ],
        )
    if objects:
        Printer.print_header("Runs:")
        objects.pop("project_name", None)
        dict_tabulate(objects, is_list_dict=True)


@ops.command()
@click.pass_context
@clean_outputs
def get(ctx):
    """Get run.

    Uses /docs/core/cli/#caching

    Examples for getting a run:

    \b
    $ polyaxon ops get  # if run is cached

    \b
    $ polyaxon ops --uid=8aac02e3a62a4f0aaa257c59da5eab80 get  # project is cached

    \b
    $ polyaxon ops --project=cats-vs-dogs -uid 8aac02e3a62a4f0aaa257c59da5eab80 get

    \b
    $ polyaxon ops -p alain/cats-vs-dogs --uid=8aac02e3a62a4f0aaa257c59da5eab80 get
    """

    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid"), is_cli=True,
    )

    try:
        polyaxon_client = RunClient(
            owner=owner, project=project_name, run_uuid=run_uuid
        )
        polyaxon_client.refresh_data()
        config = polyaxon_client.client.sanitize_for_serialization(
            polyaxon_client.run_data
        )
        cache.cache(config_manager=RunManager, config=config)
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not load run `{}` info.".format(run_uuid))
        sys.exit(1)

    get_run_details(polyaxon_client.run_data)


@ops.command()
@click.pass_context
@clean_outputs
def delete(ctx):
    """Delete a run.

    Uses /docs/core/cli/#caching

    Example:

    \b
    $ polyaxon ops delete

    \b
    $ polyaxon ops --uid=8aac02e3a62a4f0aaa257c59da5eab80 delete  # project is cached

    \b
    $ polyaxon ops --project=cats-vs-dogs -uid 8aac02e3a62a4f0aaa257c59da5eab80 delete
    """
    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid"), is_cli=True,
    )
    if not click.confirm("Are sure you want to delete run `{}`".format(run_uuid)):
        click.echo("Existing without deleting the run.")
        sys.exit(1)

    try:
        polyaxon_client = RunClient(
            owner=owner, project=project_name, run_uuid=run_uuid
        )
        polyaxon_client.delete()
        # Purge caching
        RunManager.purge()
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not delete run `{}`.".format(run_uuid))
        sys.exit(1)

    Printer.print_success("Run `{}` was delete successfully".format(run_uuid))


@ops.command()
@click.option("--name", type=str, help="Name of the run (optional).")
@click.option("--description", type=str, help="Description of the run (optional).")
@click.option(
    "--tags", type=str, help="Tags of the run, comma separated values (optional)."
)
@click.pass_context
@clean_outputs
def update(ctx, name, description, tags):
    """Update run.

    Uses /docs/core/cli/#caching

    Examples:

    \b
    $ polyaxon ops --uid=8aac02e3a62a4f0aaa257c59da5eab80 update
    --description="new description for my runs"

    \b
    $ polyaxon ops --project=cats-vs-dogs -uid 8aac02e3a62a4f0aaa257c59da5eab80 update
    --tags="foo, bar" --name="unique-name"
    """
    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid"), is_cli=True,
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
        polyaxon_client = RunClient(
            owner=owner, project=project_name, run_uuid=run_uuid
        )
        response = polyaxon_client.update(update_dict)
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not update run `{}`.".format(run_uuid))
        sys.exit(1)

    Printer.print_success("Run updated.")
    get_run_details(response)


@ops.command()
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

    Uses /docs/core/cli/#caching

    Examples:

    \b
    $ polyaxon ops stop

    \b
    $ polyaxon ops --uid=8aac02e3a62a4f0aaa257c59da5eab80 stop
    """
    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid"), is_cli=True,
    )
    if not yes and not click.confirm(
        "Are sure you want to stop " "run `{}`".format(run_uuid)
    ):
        click.echo("Existing without stopping run.")
        sys.exit(0)

    try:
        polyaxon_client = RunClient(
            owner=owner, project=project_name, run_uuid=run_uuid
        )
        polyaxon_client.stop()
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not stop run `{}`.".format(run_uuid))
        sys.exit(1)

    Printer.print_success("Run is being stopped.")


@ops.command()
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

    Uses /docs/core/cli/#caching

    Examples:

    \b
    $ polyaxon run --uid=8aac02e3a62a4f0aaa257c59da5eab80 restart
    """
    content = None
    if polyaxonfile:
        content = "{}".format(ConfigSpec.read_from(polyaxonfile))

    # Check if we need to upload
    if u:
        ctx.invoke(upload, sync=False)

    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid"), is_cli=True,
    )
    try:
        polyaxon_client = RunClient(
            owner=owner, project=project_name, run_uuid=run_uuid
        )
        response = polyaxon_client.restart(override_config=content, copy=copy)
        Printer.print_success(
            "Run was {} with uid {}".format(
                "copied" if copy else "restarted", response.uuid
            )
        )
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not restart run `{}`.".format(run_uuid))
        sys.exit(1)


@ops.command()
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

    Uses /docs/core/cli/#caching

    Examples:

    \b
    $ polyaxon ops --uid=8aac02e3a62a4f0aaa257c59da5eab80 resume
    """
    content = None
    if polyaxonfile:
        content = "{}".format(ConfigSpec.read_from(polyaxonfile))

    # Check if we need to upload
    if u:
        ctx.invoke(upload, sync=False)

    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid"), is_cli=True,
    )
    try:
        polyaxon_client = RunClient(
            owner=owner, project=project_name, run_uuid=run_uuid
        )
        response = polyaxon_client.resume(override_config=content)
        Printer.print_success("Run was resumed with uid {}".format(response.uuid))
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not resume run `{}`.".format(run_uuid))
        sys.exit(1)


@ops.command()
@click.pass_context
@clean_outputs
def invalidate(ctx):
    """Invalidate the run's cache state.

    Uses /docs/core/cli/#caching

    Examples:

    \b
    $ polyaxon ops invalidate
    """

    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid"), is_cli=True,
    )
    try:
        polyaxon_client = RunClient(
            owner=owner, project=project_name, run_uuid=run_uuid
        )
        response = polyaxon_client.invalidate()
        Printer.print_success("Run was invalidated with uid {}".format(response.uuid))
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not invalidate run `{}`.".format(run_uuid))
        sys.exit(1)


@ops.command()
@click.option("--watch", "-w", is_flag=True, help="Watch statuses.")
@click.pass_context
@clean_outputs
def statuses(ctx, watch):
    """Get run or run job statuses.

    Uses /docs/core/cli/#caching

    Examples getting run statuses:

    \b
    $ polyaxon ops statuses

    \b
    $ polyaxon ops -uid=8aac02e3a62a4f0aaa257c59da5eab80 statuses
    """

    def _handle_run_statuses():
        if not conditions:
            return
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

    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid"), is_cli=True,
    )

    client = RunClient(owner=owner, project=project_name, run_uuid=run_uuid)
    if watch:
        try:
            for status, conditions in client.watch_statuses():
                _handle_run_statuses()
        except (ApiException, HTTPError, PolyaxonClientException) as e:
            handle_cli_error(
                e, message="Could get status for run `{}`.".format(run_uuid)
            )
            sys.exit(1)
    else:
        try:
            status, conditions = client.get_statuses()
            _handle_run_statuses()
        except (ApiException, HTTPError, PolyaxonClientException) as e:
            handle_cli_error(
                e, message="Could get status for run `{}`.".format(run_uuid)
            )
            sys.exit(1)


# @ops.command()
# @click.option("--gpu", "-g", is_flag=True, help="List run GPU resources.")
# @click.pass_context
# @clean_outputs
# def resources(ctx, gpu):
#     """Get run or run job resources.
#
#     Uses /docs/core/cli/#caching
#
#     Examples for getting run resources:
#
#     \b
#     $ polyaxon ops -uid=8aac02e3a62a4f0aaa257c59da5eab80 resources
#
#     For GPU resources
#
#     \b
#     $ polyaxon ops -uid=8aac02e3a62a4f0aaa257c59da5eab80 resources --gpu
#     """
#
#     def get_run_resources():
#         try:
#             message_handler = Printer.gpu_resources if gpu else Printer.resources
#             PolyaxonClient().run.resources(
#                 owner, project_name, run_uuid, message_handler=message_handler
#             )
#         except (ApiException, HTTPError) as e:
#             handle_cli_error(
#                 e, message="Could not get resources for run `{}`.".format(run_uuid)
#             )
#             sys.exit(1)
#
#     owner, project_name, run_uuid = get_project_run_or_local(
#         ctx.obj.get("project"), ctx.obj.get("run_uuid"), is_cli=True,
#     )
#
#     get_run_resources()


@ops.command()
@click.option(
    "--follow",
    "-f",
    is_flag=True,
    default=True,
    help="Stream logs after showing past logs.",
)
@click.option(
    "--hide_time",
    "--hide-time",
    is_flag=True,
    default=False,
    help="Whether or not to hide timestamps from the log stream.",
)
@click.option(
    "--all_info",
    "--all-info",
    is_flag=True,
    default=False,
    help="Whether to stream logs from all containers.",
)
@click.pass_context
@clean_outputs
def logs(ctx, follow, hide_time, all_info):
    """Get run or run job logs.

    Uses /docs/core/cli/#caching

    Examples for getting run logs:

    \b
    $ polyaxon run logs

    \b
    $ polyaxon ops -uid=8aac02e3a62a4f0aaa257c59da5eab80 -p mnist logs
    """

    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid"), is_cli=True,
    )
    client = RunClient(owner=owner, project=project_name, run_uuid=run_uuid)

    get_run_logs(
        client=client, hide_time=hide_time, all_info=all_info, follow=follow,
    )


@ops.command()
@click.pass_context
@clean_outputs
def artifacts(ctx):
    """Download outputs/artifacts for run.

    Uses /docs/core/cli/#caching

    Examples:

    \b
    $ polyaxon ops -uid=8aac02e3a62a4f0aaa257c59da5eab80 artifacts
    """
    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid"), is_cli=True,
    )
    try:
        client = RunClient(owner=owner, project=project_name, run_uuid=run_uuid)
        client.download_artifacts()
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not download outputs for run `{}`.".format(run_uuid)
        )
        sys.exit(1)
    Printer.print_success("Files downloaded.")


@ops.command()
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
    help="Print the url of the dashboard for this run.",
)
@click.pass_context
@clean_outputs
def dashboard(ctx, yes, url):
    """Open this operation's dashboard details in browser."""
    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid"), is_cli=True,
    )
    dashboard_url = settings.CLIENT_CONFIG.host
    run_url = "{}/{}/{}/runs/{}/".format(dashboard_url, owner, project_name, run_uuid)
    if url:
        Printer.print_header("The dashboard is available at: {}".format(run_url))
        sys.exit(0)
    if not yes:
        click.confirm(
            "Dashboard page will now open in your browser. Continue?",
            abort=True,
            default=True,
        )
    click.launch(run_url)


@ops.command()
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Automatic yes to prompts. "
    'Assume "yes" as answer to all prompts and run non-interactively.',
)
@click.option(
    "--external", is_flag=True, default=False, help="Open the external service URL.",
)
@click.option(
    "--url",
    is_flag=True,
    default=False,
    help="Print the url of the dashboard or external service.",
)
@click.pass_context
@clean_outputs
def service(ctx, yes, external, url):
    """Open the operation service in browser.

    N.B. The operation must have a run kind service, otherwise it will raise an error.

    You can open the service embedded in Polyaxon UI or using the real service URL,
    please use the `--external` flag.
    """
    owner, project_name, run_uuid = get_project_run_or_local(
        ctx.obj.get("project"), ctx.obj.get("run_uuid"), is_cli=True,
    )
    client = RunClient(owner=owner, project=project_name, run_uuid=run_uuid)
    client.refresh_data()
    if client.run_data.kind != V1RunKind.SERVICE:
        Printer.print_warning(
            "Command expected a operations of "
            "kind `service` received kind: {}!".format(client.run_data.kind)
        )
        sys.exit(1)
    dashboard_url = settings.CLIENT_CONFIG.host

    Printer.print_header("Waiting for running condition ...")
    client.wait_for_condition(statuses=[V1Statuses.RUNNING], print_status=True)

    client.refresh_data()
    namespace = client.run_data.settings.namespace

    run_url = "{}/{}/{}/runs/{}/service".format(
        dashboard_url, owner, project_name, run_uuid
    )
    service_endpoint = SERVICES_V1
    if client.run_data.meta_info.get("rewrite_path", False):
        service_endpoint = REWRITE_SERVICES_V1
    external_run_url = "{}/{}/{}/{}/{}/runs/{}/".format(
        dashboard_url, service_endpoint, namespace, owner, project_name, run_uuid
    )
    if url:
        Printer.print_header("The service will be available at: {}".format(run_url))
        Printer.print_header(
            "You can also view it in an external link at: {}".format(external_run_url)
        )
        sys.exit(0)
    if not yes:
        click.confirm(
            "Dashboard page will now open in your browser. Continue?",
            abort=True,
            default=True,
        )
    if external:
        click.launch(external_run_url)
        sys.exit(0)
    click.launch(run_url)
