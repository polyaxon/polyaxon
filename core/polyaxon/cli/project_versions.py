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

from typing import Callable, List, Optional, Union

import click

from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon.cli.dashboard import get_dashboard_url
from polyaxon.cli.errors import handle_cli_error
from polyaxon.client import PolyaxonClient, ProjectClient
from polyaxon.env_vars.getters import get_versioned_entity_full_name
from polyaxon.lifecycle import V1ProjectVersionKind, V1StageCondition, V1Stages
from polyaxon.utils.formatting import (
    Printer,
    dict_tabulate,
    dict_to_tabulate,
    get_meta_response,
    list_dicts_to_tabulate,
)
from polyaxon.utils.query_params import get_query_params
from polyaxon.utils.validation import validate_tags


def get_version_details(response, content_callback: Callable = None):
    content = response.content
    response = dict_to_tabulate(
        response.to_dict(), humanize_values=True, exclude_attrs=["content"]
    )

    Printer.print_header("Version info:")
    dict_tabulate(response)

    def get_content(content):
        if content:
            Printer.print_header("Content:")
            click.echo(content)

    content_callback = content_callback or get_content
    content_callback(content)


def list_project_versions(
    owner: str,
    project_name: str,
    kind: V1ProjectVersionKind,
    limit: str = None,
    offset: str = None,
    query: str = None,
    sort: str = None,
    client: PolyaxonClient = None,
):
    version_info = "<owner: {}> <project: {}>".format(owner, project_name)
    polyaxon_client = ProjectClient(owner=owner, project=project_name, client=client)
    params = get_query_params(limit=limit, offset=offset, query=query, sort=sort)
    try:
        response = polyaxon_client.list_versions(kind=kind, **params)
    except (ApiException, HTTPError) as e:
        message = "Could not get list of versions."
        handle_cli_error(e, message=message)
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header("Versions for {}".format(version_info))
        Printer.print_header("Navigation:")
        dict_tabulate(meta)
    else:
        Printer.print_header("No version found for {}".format(version_info))

    objects = list_dicts_to_tabulate(
        [o.to_dict() for o in response.results],
        humanize_values=True,
        exclude_attrs=[
            "uuid",
            "readme",
            "description",
            "owner",
            "project",
            "role",
            "content",
        ],
    )
    if objects:
        Printer.print_header("Versions:")
        dict_tabulate(objects, is_list_dict=True)


def register_project_version(
    owner: str,
    project_name: str,
    version: str,
    kind: V1ProjectVersionKind,
    description: str = None,
    tags: Optional[Union[str, List[str]]] = None,
    content: str = None,
    run: str = None,
    connection: str = None,
    artifacts: Optional[Union[str, List[str]]] = None,
    force: bool = False,
):
    version = version or "latest"
    fqn_version = get_versioned_entity_full_name(owner, project_name, version)
    polyaxon_client = ProjectClient(owner=owner, project=project_name)

    try:
        _version = polyaxon_client.register_version(
            kind=kind,
            version=version,
            description=description,
            tags=tags,
            content=content,
            run=run,
            connection=connection,
            artifacts=artifacts,
            force=force,
        )
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not create model version `{}`.".format(fqn_version)
        )
        sys.exit(1)

    Printer.print_success(
        "Model version `{}` was created successfully.".format(fqn_version)
    )
    click.echo(
        "You can view this model version on Polyaxon UI: {}".format(
            get_dashboard_url(
                subpath="{}/{}/{}s/{}".format(owner, project_name, kind, version)
            )
        )
    )


def get_project_version(
    owner: str,
    project_name: str,
    kind: V1ProjectVersionKind,
    version: str,
    content_callback: Callable = None,
    client: PolyaxonClient = None,
):
    fqn_version = get_versioned_entity_full_name(owner, project_name, version)
    polyaxon_client = ProjectClient(owner=owner, project=project_name, client=client)

    try:
        response = polyaxon_client.get_version(kind, version)
        get_version_details(response, content_callback)
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e,
            message="Could not get {} version `{}`.".format(
                kind,
                fqn_version,
            ),
            sys_exit=True,
        )


def delete_project_version(
    owner: str, project_name: str, kind: V1ProjectVersionKind, version: str
):
    fqn_version = get_versioned_entity_full_name(owner, project_name, version)
    polyaxon_client = ProjectClient(owner=owner, project=project_name)

    if not click.confirm(
        "Are sure you want to delete {} version `{}`".format(kind, fqn_version)
    ):
        click.echo("Existing without deleting {} version.".format(kind))
        sys.exit(1)

    try:
        polyaxon_client.delete_version(kind, version)
        Printer.print_success(
            "The {} version `{}` was delete successfully".format(kind, fqn_version)
        )
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e,
            message="Could not delete the {} version `{}`.".format(kind, fqn_version),
        )
        sys.exit(1)


def update_project_version(
    owner: str,
    project_name: str,
    kind: V1ProjectVersionKind,
    version: str,
    name: str = None,
    description: str = None,
    tags: Optional[Union[str, List[str]]] = None,
    content_callback: Callable = None,
):
    fqn_version = get_versioned_entity_full_name(owner, project_name, version)
    polyaxon_client = ProjectClient(owner=owner, project=project_name)

    update_dict = {}
    if name:
        update_dict["name"] = name

    if description:
        update_dict["description"] = description

    tags = validate_tags(tags)
    if tags:
        update_dict["tags"] = tags

    if not update_dict:
        Printer.print_warning(
            "No argument was provided to update the {} version {}.".format(
                kind, fqn_version
            )
        )
        sys.exit(1)

    try:
        response = polyaxon_client.patch_version(kind, version, update_dict)
        Printer.print_success("the {} version updated.".format(kind))
        get_version_details(response, content_callback)
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e,
            message="Could not update the {} version `{}`.".format(kind, fqn_version),
        )
        sys.exit(1)


def stage_project_version(
    owner: str,
    project_name: str,
    kind: V1ProjectVersionKind,
    version: str,
    to: V1Stages,
    message: str = None,
):
    fqn_version = get_versioned_entity_full_name(owner, project_name, version)
    polyaxon_client = ProjectClient(owner=owner, project=project_name)

    if not to:
        Printer.print_warning(
            "No argument was provided to update the version stage, "
            "please provide a correct `--to` value."
        )
        sys.exit(1)

    condition = V1StageCondition(type=to, status=True, reason="UserStageUpdate")

    if message:
        condition.message = message

    try:
        polyaxon_client.stage_project_version(kind, version, condition=condition)
        Printer.print_success("The {} version's stage was updated.".format(kind))
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e,
            message="Could not update the stage for {} version `{}`.".format(
                kind, fqn_version
            ),
        )
        sys.exit(1)


def open_project_version_dashboard(
    owner: str,
    project_name: str,
    kind: V1ProjectVersionKind,
    version: str,
    url: str,
    yes: bool = False,
):
    subpath = "{}/{}/{}s/{}".format(owner, project_name, kind, version)

    artifact_url = get_dashboard_url(subpath=subpath)
    if url:
        Printer.print_header("The dashboard is available at: {}".format(artifact_url))
        sys.exit(0)
    if not yes:
        click.confirm(
            "Dashboard page will now open in your browser. Continue?",
            abort=True,
            default=True,
        )
    click.launch(artifact_url)
