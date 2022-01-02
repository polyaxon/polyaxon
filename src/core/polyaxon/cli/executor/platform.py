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

from collections import namedtuple
from typing import Dict, List

import click

from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon.cli.dashboard import get_dashboard_url
from polyaxon.cli.errors import handle_cli_error
from polyaxon.cli.operations import approve
from polyaxon.cli.operations import logs as run_logs
from polyaxon.cli.operations import statuses
from polyaxon.cli.operations import upload as run_upload
from polyaxon.cli.utils import handle_output
from polyaxon.client import RunClient
from polyaxon.constants.globals import DEFAULT_UPLOADS_PATH
from polyaxon.constants.metadata import (
    META_COPY_ARTIFACTS,
    META_EAGER_MODE,
    META_UPLOAD_ARTIFACTS,
)
from polyaxon.managers.run import RunConfigManager
from polyaxon.polyflow import V1CompiledOperation, V1Operation
from polyaxon.schemas import V1RunPending
from polyaxon.schemas.types import V1ArtifactsType
from polyaxon.utils import cache
from polyaxon.utils.formatting import Printer


class RunWatchSpec(namedtuple("RunWatchSpec", "uuid name")):
    pass


def run(
    ctx,
    name: str,
    owner: str,
    project_name: str,
    description: str,
    tags: List[str],
    op_spec: V1Operation,
    log: bool,
    upload: bool,
    upload_to: str,
    upload_from: str,
    watch: bool,
    eager: bool,
    output: str = None,
):

    polyaxon_client = RunClient(owner=owner, project=project_name)

    def cache_run(data):
        config = polyaxon_client.client.sanitize_for_serialization(data)
        cache.cache(
            config_manager=RunConfigManager,
            config=config,
            owner=owner,
            project=project_name,
        )

    def create_run(
        is_managed: bool = True, meta_info: Dict = None, pending: str = None
    ):
        try:
            response = polyaxon_client.create(
                name=name,
                description=description,
                tags=tags,
                content=op_spec,
                is_managed=is_managed,
                meta_info=meta_info,
                pending=pending,
            )
            if output:
                handle_output(
                    polyaxon_client.client.sanitize_for_serialization(response), output
                )
                return
            Printer.print_success("A new run `{}` was created".format(response.uuid))
            if not eager:
                cache_run(response)
                click.echo(
                    "You can view this run on Polyaxon UI: {}".format(
                        get_dashboard_url(
                            subpath="{}/{}/runs/{}".format(
                                owner, project_name, response.uuid
                            )
                        )
                    )
                )
            return response
        except (ApiException, HTTPError) as e:
            handle_cli_error(
                e,
                message="Could not create a run.",
                http_messages_mapping={
                    404: "Make sure you have a project initialized in your current workdir, "
                    "otherwise you need to pass a project with `-p/--project`. "
                    "The project {}/{} does not exist.".format(owner, project_name)
                },
            )
            sys.exit(1)

    def refresh_run():
        try:
            polyaxon_client.refresh_data()
        except (ApiException, HTTPError) as e:
            handle_cli_error(
                e, message="The current eager operation does not exist anymore."
            )
            sys.exit(1)

    def delete_run():
        try:
            polyaxon_client.delete()
        except (ApiException, HTTPError) as e:
            handle_cli_error(
                e, message="The current eager operation does not exist anymore."
            )
            sys.exit(1)

    def watch_run_statuses(run_uuid: str):
        ctx.obj = {"project": "{}/{}".format(owner, project_name), "run_uuid": run_uuid}
        ctx.invoke(statuses, watch=True)

    def watch_run_logs(run_uuid: str):
        ctx.obj = {"project": "{}/{}".format(owner, project_name), "run_uuid": run_uuid}
        ctx.invoke(run_logs)

    def upload_run(run_uuid: str):
        ctx.obj = {"project": "{}/{}".format(owner, project_name), "run_uuid": run_uuid}
        ctx.invoke(
            run_upload, path_to=upload_to, path_from=upload_from, sync_failure=True
        )
        ctx.invoke(approve)

    if not output:
        click.echo("Creating a new run...")
    run_meta_info = None
    if eager:
        run_meta_info = {META_EAGER_MODE: True}
    if upload:
        run_meta_info = run_meta_info or {}
        run_meta_info[META_UPLOAD_ARTIFACTS] = upload_to or DEFAULT_UPLOADS_PATH
    run_instance = create_run(
        not eager, run_meta_info, pending=V1RunPending.UPLOAD if upload else None
    )
    if not run_instance:
        return

    runs_to_watch = [RunWatchSpec(run_instance.uuid, run_instance.name)]

    build_uuid = None
    if run_instance.pending == V1RunPending.BUILD and run_instance.settings.build:
        build_uuid = run_instance.settings.build.get("uuid")
        build_name = run_instance.settings.build.get("name")
        runs_to_watch.insert(0, RunWatchSpec(build_uuid, build_name))

    if upload:
        upload_run(build_uuid or run_instance.uuid)

    if eager:
        from polyaxon.polyaxonfile.manager import get_eager_matrix_operations

        refresh_run()
        # Prepare artifacts
        run_meta_info = {}
        if upload:
            run_meta_info = {
                META_UPLOAD_ARTIFACTS: upload_to or DEFAULT_UPLOADS_PATH,
                META_COPY_ARTIFACTS: V1ArtifactsType(
                    dirs=[run_instance.uuid]
                ).to_dict(),
            }
        compiled_operation = V1CompiledOperation.read(polyaxon_client.run_data.content)
        matrix_content = polyaxon_client.run_data.raw_content
        # Delete matrix placeholder
        click.echo("Cleaning matrix run placeholder...")
        delete_run()
        # Suggestions
        click.echo("Starting eager mode...")
        for op_spec in get_eager_matrix_operations(
            content=matrix_content,
            compiled_operation=compiled_operation,
            is_cli=True,
        ):
            i_run_instance = create_run(meta_info=run_meta_info)
            runs_to_watch.append(RunWatchSpec(i_run_instance.uuid, i_run_instance.name))

        return

    # Check if we need to invoke logs
    if watch and not eager:
        for instance in runs_to_watch:
            Printer.print_success(
                f"Starting watch for run: <Name: {instance.name}> - <uuid: {instance.uuid}>"
            )
            watch_run_statuses(instance.uuid)

    # Check if we need to invoke logs
    if log and not eager:
        for instance in runs_to_watch:
            Printer.print_success(
                f"Starting logs for run: <Name: {instance.name}> - <uuid: {instance.uuid}>"
            )
            watch_run_logs(instance.uuid)
