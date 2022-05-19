#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from urllib3.exceptions import HTTPError

from polyaxon.cli.dashboard import get_dashboard_url
from polyaxon.cli.errors import handle_cli_error
from polyaxon.client import PolyaxonClient, ProjectClient
from polyaxon.lifecycle import V1ProjectVersionKind
from polyaxon.utils.formatting import (
    Printer,
    dict_tabulate,
    dict_to_tabulate,
    get_meta_response,
    list_dicts_to_tabulate,
)
from polyaxon.utils.fqn_utils import get_versioned_entity_full_name
from polyaxon.utils.query_params import get_query_params
from polyaxon.utils.validation import validate_tags
from polyaxon_sdk.rest import ApiException


def get_version_details(response, content_callback: Callable = None):
    content = response.content
    meta_info = response.meta_info
    readme = response.readme
    response = dict_to_tabulate(
        response.to_dict(),
        humanize_values=True,
        exclude_attrs=["content", "meta_info", "stage_conditions", "readme"],
    )

    Printer.print_heading("Version info:")
    dict_tabulate(response)

    if meta_info:
        artifacts = meta_info.pop("artifacts", None)
        lineage = meta_info.pop("lineage", artifacts)
        if meta_info:
            Printer.print_heading("Version meta info:")
            dict_tabulate(meta_info)

        if lineage:
            Printer.print_heading("Version artifacts lineage:")
            Printer.print_json(lineage)

    if readme:
        Printer.print_heading("Version readme:")
        Printer.print_md(readme)

    def get_content(_content: str):
        if _content:
            Printer.print_heading("Content:")
            Printer.print_yaml(_content)

    content_callback = content_callback or get_content
    content_callback(content)


def get_version_stages_table(stage, conditions):
    table = Printer.get_table()

    if not conditions:
        Printer.print(table)
        return

    Printer.print(
        "Latest stage: {}".format(
            Printer.add_status_color({"stage": stage}, status_key="stage")["stage"]
        )
    )
    objects = [
        dict_to_tabulate(Printer.add_status_color(o.to_dict(), status_key="type"))
        for o in conditions
    ]

    if not objects:
        Printer.print(table)
        return

    if not table.columns:
        for c in objects[0].keys():
            table.add_column(c)
    if objects:
        for o in objects:
            table.add_row(*o.values())

    Printer.print(table)


def list_project_versions_response(
    owner: str,
    project_name: str,
    kind: V1ProjectVersionKind,
    limit: str = None,
    offset: str = None,
    query: str = None,
    sort: str = None,
    client: PolyaxonClient = None,
):
    polyaxon_client = ProjectClient(owner=owner, project=project_name, client=client)
    params = get_query_params(limit=limit, offset=offset, query=query, sort=sort)
    try:
        return polyaxon_client.list_versions(kind=kind, **params)
    except (ApiException, HTTPError) as e:
        message = "Could not get list of {} versions for {}/{}.".format(
            kind, owner, project_name
        )
        handle_cli_error(e, message=message)
        sys.exit(1)


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
    response = list_project_versions_response(
        owner=owner,
        project_name=project_name,
        kind=kind,
        limit=limit,
        offset=offset,
        query=query,
        sort=sort,
        client=client,
    )
    meta = get_meta_response(response)
    if meta:
        Printer.print_heading("Versions for {}".format(version_info))
        Printer.print_heading("Navigation:")
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
            "connection",
            "meta_info",
            "run",
            "artifacts",
            "stage_conditions",
        ],
    )
    if objects:
        Printer.print_heading("Versions:")
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
            e, message="Could not create version `{}`.".format(fqn_version)
        )
        sys.exit(1)

    Printer.print_success("Version `{}` was created successfully.".format(fqn_version))
    Printer.print(
        "You can view this version on Polyaxon UI: {}".format(
            get_dashboard_url(
                subpath="{}/{}/{}s/{}".format(owner, project_name, kind, version)
            )
        )
    )


def copy_project_version(
    owner: str,
    project_name: str,
    version: str,
    kind: V1ProjectVersionKind,
    to_project: str = None,
    name: str = None,
    description: str = None,
    tags: Optional[Union[str, List[str]]] = None,
    content: str = None,
    force: bool = False,
):
    version = version or "latest"
    fqn_version = get_versioned_entity_full_name(owner, project_name, version)
    polyaxon_client = ProjectClient(owner=owner, project=project_name)

    try:
        _version = polyaxon_client.copy_version(
            kind=kind,
            version=version,
            to_project=to_project,
            name=name,
            description=description,
            tags=tags,
            content=content,
            force=force,
        )
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not copy version `{}`.".format(fqn_version))
        sys.exit(1)

    fqn_copied_version = get_versioned_entity_full_name(
        owner,
        to_project or project_name,
        _version.name,
    )
    Printer.print_success(
        "Version `{}` was copied successfully to `{}`.".format(
            fqn_version, fqn_copied_version
        )
    )
    Printer.print(
        "You can view this version on Polyaxon UI: {}".format(
            get_dashboard_url(
                subpath="{}/{}/{}s/{}".format(
                    owner, to_project or project_name, kind, _version.name
                )
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


def get_project_version_stages(
    owner: str,
    project_name: str,
    kind: V1ProjectVersionKind,
    version: str,
    client: PolyaxonClient = None,
):
    fqn_version = get_versioned_entity_full_name(owner, project_name, version)
    polyaxon_client = ProjectClient(owner=owner, project=project_name, client=client)

    try:
        stage, stage_conditions = polyaxon_client.get_version_stages(kind, version)
        get_version_stages_table(stage, stage_conditions)
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
    owner: str,
    project_name: str,
    kind: V1ProjectVersionKind,
    version: str,
    yes: bool = False,
):
    fqn_version = get_versioned_entity_full_name(owner, project_name, version)
    polyaxon_client = ProjectClient(owner=owner, project=project_name)

    if not yes and not click.confirm(
        "Are sure you want to delete {} version `{}`".format(kind, fqn_version)
    ):
        Printer.print("Exiting without deleting {} version.".format(kind))
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

    tags = validate_tags(tags, validate_yaml=True)
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
        Printer.print_success("The {} version updated.".format(kind))
        get_version_details(response, content_callback)
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e,
            message="Could not update the {} version `{}`.".format(kind, fqn_version),
        )
        sys.exit(1)


def transfer_project_version(
    owner: str,
    project_name: str,
    kind: V1ProjectVersionKind,
    version: str,
    to_project: str,
):
    fqn_version = get_versioned_entity_full_name(owner, project_name, version)
    polyaxon_client = ProjectClient(owner=owner, project=project_name)

    try:
        polyaxon_client.transfer_version(kind, version, to_project)
        Printer.print_success(
            "The `{}` version was transferred to `{}`.".format(kind, to_project)
        )
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e,
            message="Could not transfer the {} version `{}` to `{}`.".format(
                kind, fqn_version, to_project
            ),
        )
        sys.exit(1)


def stage_project_version(
    owner: str,
    project_name: str,
    kind: V1ProjectVersionKind,
    version: str,
    to: str,
    reason: str = None,
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

    try:
        polyaxon_client.stage_version(
            kind, version, stage=to, reason=reason or "CliStageUpdate", message=message
        )
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
    if yes or click.confirm(
        "Dashboard page will now open in your browser. Continue?",
        default=True,
    ):
        click.launch(artifact_url)


def pull_project_version(
    owner: str,
    project_name: str,
    kind: V1ProjectVersionKind,
    version: str,
    path: str,
    download_artifacts: bool = True,
):
    fqn_version = get_versioned_entity_full_name(owner, project_name, version)
    polyaxon_client = ProjectClient(owner=owner, project=project_name)

    try:
        Printer.print_header(
            "Pulling {} version [white]`{}`[/white] ...".format(kind, fqn_version),
        )
        path = polyaxon_client.pull_version(
            kind,
            version,
            path=path,
            download_artifacts=download_artifacts,
        )
        Printer.print_success(
            "Finished pulling the {} version `{}` to `{}`".format(
                kind, fqn_version, path
            )
        )
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e,
            message="Could not pull the {} version `{}`".format(kind, fqn_version),
        )


def pull_one_or_many_project_versions(
    owner: str,
    project_name: str,
    kind: V1ProjectVersionKind,
    version: str,
    all_versions: bool = None,
    query: str = None,
    limit: int = None,
    offset: int = None,
    path: str = None,
    download_artifacts: bool = True,
):
    def _pull(version_name: str):
        pull_project_version(
            owner=owner,
            project_name=project_name,
            kind=kind,
            version=version_name,
            path=path,
            download_artifacts=download_artifacts,
        )

    if all_versions or any([query, limit, offset]):
        limit = 1000 if all_versions else limit
        versions = list_project_versions_response(
            owner=owner,
            project_name=project_name,
            kind=kind,
            limit=limit,
            offset=offset,
            query=query,
        ).results
        Printer.print_header(f"Pulling {kind} versions (total: {len(versions)}) ...")
        for idx, version in enumerate(versions):
            Printer.print_heading(f"Pulling version {idx + 1}/{len(versions)} ...")
            _pull(version.name)
    elif version:
        _pull(version)
    else:
        Printer.print_error(
            "Please provide a version name, provide a query to filter versions to pull, "
            "or pass the flag `-a/--all` to pull versions.",
            sys_exit=True,
        )
