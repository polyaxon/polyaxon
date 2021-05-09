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
import os
import sys

import click

from polyaxon_sdk import V1ComponentHub, V1ComponentVersion
from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon import settings
from polyaxon.cli.dashboard import get_dashboard_url
from polyaxon.cli.errors import handle_cli_error
from polyaxon.cli.options import (
    OPTIONS_COMPONENT_HUB,
    OPTIONS_COMPONENT_VERSION,
    OPTIONS_OWNER,
)
from polyaxon.cli.utils import get_entity_details
from polyaxon.client import PolyaxonClient
from polyaxon.constants.globals import DEFAULT_HUB, NO_AUTH
from polyaxon.env_vars.getters import get_component_info
from polyaxon.exceptions import PolyaxonException
from polyaxon.logger import clean_outputs
from polyaxon.polyaxonfile import get_specification
from polyaxon.schemas.cli.client_config import ClientConfig
from polyaxon.utils.formatting import (
    Printer,
    dict_tabulate,
    dict_to_tabulate,
    get_meta_response,
    list_dicts_to_tabulate,
)
from polyaxon.utils.query_params import get_query_params
from polyaxon.utils.validation import validate_tags


def get_current_or_public_client():
    if settings.CLI_CONFIG.is_ce:
        return PolyaxonClient(config=ClientConfig(), token=NO_AUTH)

    return PolyaxonClient()


def get_specification_details(specification):
    if specification.inputs:
        Printer.print_header("Component inputs:")
        objects = list_dicts_to_tabulate([i.to_dict() for i in specification.inputs])
        dict_tabulate(objects, is_list_dict=True)

    if specification.outputs:
        Printer.print_header("Component outputs:")
        objects = list_dicts_to_tabulate([o.to_dict() for o in specification.outputs])
        dict_tabulate(objects, is_list_dict=True)

    Printer.print_header("Content:")
    click.echo(specification.to_dict())


def get_component_version_details(response):
    content = response.content
    response = dict_to_tabulate(
        response.to_dict(), humanize_values=True, exclude_attrs=["content"]
    )

    Printer.print_header("Component info:")
    dict_tabulate(response)

    if content:
        specification = get_specification(data=content)
        get_specification_details(specification)
    else:
        Printer.print_warning(
            "This component version does not have any polyaxonfile content!"
        )


def get_info(component: str = None, version: str = None):
    if not any([component, version]):
        Printer.print_error(
            "A component or a component version is required.", sys_exit=True
        )
    if all([component, version]):
        Printer.print_error(
            "Only a component or a component version is required, not both.",
            sys_exit=True,
        )

    if component:
        entity = component
        entity_name = "component"
        is_version = False
    else:
        entity = version
        entity_name = "component version"
        is_version = True

    try:
        owner, component_hub, component_version = get_component_info(entity)
        return owner, component_hub, component_version, is_version
    except PolyaxonException as e:
        handle_cli_error(
            e,
            message="Could not resolve the {} from the value `{}`.".format(
                entity_name, entity
            ),
            sys_exit=True,
        )


@click.group()
@clean_outputs
def hub():
    """Commands for component hub."""


@hub.command()
@click.option(
    "--name", type=str, help="The component hub name, e.g. 'kaniko' or 'acme/kaniko'."
)
@click.option("--description", type=str, help="Description of the component.")
@click.option("--tags", type=str, help="Tags of the component, comma separated values.")
@click.option(
    "--public", is_flag=True, help="Set the visibility of the component to public."
)
@clean_outputs
def create(name, description, tags, public):
    """Create a new component.

    Example:

    \b
    $ polyaxon hub create --name=kaniko --description="Tool to build container images"

    \b
    $ polyaxon hub create --name=owner/name --description="Component description"
    """
    if not name:
        Printer.print_error(
            "Please provide a name to create a component hub.",
            command_help="hub create",
            sys_exit=True,
        )
    owner, hub_name, _, _ = get_info(name, None)

    tags = validate_tags(tags)

    if not owner or not hub_name:
        Printer.print_error(
            "Please provide a valid component name with --name=owner/hub-name. "
        )
        sys.exit(1)

    try:
        hub_config = V1ComponentHub(
            name=hub_name, description=description, tags=tags, is_public=public
        )
        polyaxon_client = PolyaxonClient()
        _hub = polyaxon_client.component_hub_v1.create_component_hub(owner, hub_config)
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not create component hub `{}`.".format(hub_name)
        )
        sys.exit(1)

    Printer.print_success(
        "Component hub `{}` was created successfully.".format(_hub.name)
    )
    click.echo(
        "You can view this component hub on Polyaxon UI: {}".format(
            get_dashboard_url(subpath="{}/hub/{}".format(owner, _hub.name))
        )
    )


@hub.command()
@click.option(
    "-f",
    "--file",
    "polyaxonfile",
    type=click.Path(exists=True),
    help="The component spec version to push.",
)
@click.option(
    "--name",
    type=str,
    help="The component version name, e.g. 'kaniko' or 'kaniko:1.2' "
    "or 'acme/kaniko:latest' or 'acme/kaniko:dev'.",
)
@click.option("--description", type=str, help="Description of the version.")
@click.option("--tags", type=str, help="Tags of the version, comma separated values.")
@clean_outputs
def push(polyaxonfile, name, description, tags):
    """Push a new component version.
    If the name corresponds to an existing component version, it will be updated.

    Example:

    \b
    $ polyaxon hub push -f polyaxonfile.yaml --name=kaniko:latest --description="Tool to build container images"

    \b
    $ polyaxon hub push -f polyaxonfile.yaml --name=owner/name:v1 --description="Component description"
    """
    if not name:
        Printer.print_error(
            "Please provide a name to create a component version.",
            command_help="hub push",
            sys_exit=True,
        )
    owner, hub_name, version, is_version = get_info(None, name)
    tags = validate_tags(tags)

    if not polyaxonfile or not os.path.isfile(polyaxonfile):
        Printer.print_error(
            "Please provide a path to a polyaxonfile to create a component version.",
            command_help="hub push",
            sys_exit=True,
        )
    try:
        plx_file = get_specification(data=polyaxonfile)
    except Exception as e:
        handle_cli_error(e, message="Polyaxonfile is not valid.")
        sys.exit(1)

    if not owner or not hub_name or not version:
        Printer.print_error(
            "Please provide a valid component version with --name=owner/hub-name:version. "
        )
        sys.exit(1)

    polyaxon_client = PolyaxonClient()
    try:
        polyaxon_client.component_hub_v1.get_component_version(owner, hub_name, version)
        to_update = True
    except (ApiException, HTTPError):
        to_update = False

    if to_update:
        if not click.confirm(
            "A component version {}/{}:{} already exists. "
            "Do you want to push force this version?".format(owner, hub_name, version)
        ):
            click.echo("Existing without pushing component version.")
            sys.exit(1)

    try:
        hub_config = V1ComponentVersion(
            name=version,
            description=description,
            tags=tags,
            content=plx_file.to_dict(dump=True),
        )
        if to_update:
            _version = polyaxon_client.component_hub_v1.update_component_version(
                owner,
                hub_name,
                version,
                hub_config,
            )
        else:
            _version = polyaxon_client.component_hub_v1.create_component_version(
                owner,
                hub_name,
                hub_config,
            )
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not create component version `{}`.".format(hub_name)
        )
        sys.exit(1)

    Printer.print_success(
        "Component version `{}` was created successfully.".format(_version.name)
    )
    click.echo(
        "You can view this component version on Polyaxon UI: {}".format(
            get_dashboard_url(
                subpath="{}/hub/{}/versions/{}".format(owner, hub_name, _version.name)
            )
        )
    )


@hub.command()
@click.option(*OPTIONS_OWNER["args"], **OPTIONS_OWNER["kwargs"])
@click.option(*OPTIONS_COMPONENT_HUB["args"], **OPTIONS_COMPONENT_HUB["kwargs"])
@click.option(
    "--query",
    "-q",
    type=str,
    help="To filter the component hub/versions based on this query spec.",
)
@click.option(
    "--sort",
    "-s",
    type=str,
    help="To order the component hub/versions based on the sort spec.",
)
@click.option("--limit", type=int, help="To limit the list of component hub/versions.")
@click.option(
    "--offset", type=int, help="To offset the list of component hub/versions."
)
@clean_outputs
def ls(owner, component, query, sort, limit, offset):
    """List component hub/versions by owner or owner/component."""
    if owner and component:
        Printer.print_error(
            "Only an owner or a component is required, not both.", sys_exit=True
        )
    if component:
        owner, component_hub, component_version, is_version = get_info(component, None)
    else:
        owner = owner or DEFAULT_HUB
        component_hub = None
    if not owner:
        Printer.print_error(
            "Please provide a valid owner --owner/-o or a component --component/-c."
        )
        sys.exit(1)

    def list_versions():
        component_info = "<owner: {}> <component: {}>".format(owner, component_hub)
        try:
            polyaxon_client = get_current_or_public_client()
            params = get_query_params(
                limit=limit, offset=offset, query=query, sort=sort
            )
            response = polyaxon_client.component_hub_v1.list_component_versions(
                owner, component_hub, **params
            )
        except (ApiException, HTTPError) as e:
            message = "Could not get list of component version."
            handle_cli_error(e, message=message)
            sys.exit(1)

        meta = get_meta_response(response)
        if meta:
            Printer.print_header("Versions for {}".format(component_info))
            Printer.print_header("Navigation:")
            dict_tabulate(meta)
        else:
            Printer.print_header("No version found for {}".format(component_info))

        objects = list_dicts_to_tabulate(
            [o.to_dict() for o in response.results],
            humanize_values=True,
            exclude_attrs=[
                "uuid",
                "readme",
                "description",
                "owner",
                "owner",
                "role",
                "settings",
                "content",
                "live_state",
            ],
        )
        if objects:
            Printer.print_header("Component versions:")
            dict_tabulate(objects, is_list_dict=True)

    def list_components():
        try:
            polyaxon_client = get_current_or_public_client()
            params = get_query_params(
                limit=limit, offset=offset, query=query, sort=sort
            )
            response = polyaxon_client.component_hub_v1.list_component_hubs(
                owner, **params
            )
        except (ApiException, HTTPError) as e:
            message = "Could not get list of components."
            handle_cli_error(e, message=message)
            sys.exit(1)

        meta = get_meta_response(response)
        if meta:
            Printer.print_header("Components for owner {}".format(owner))
            Printer.print_header("Navigation:")
            dict_tabulate(meta)
        else:
            Printer.print_header("No component hub found for owner {}".format(owner))

        objects = list_dicts_to_tabulate(
            [o.to_dict() for o in response.results],
            humanize_values=True,
            exclude_attrs=[
                "uuid",
                "readme",
                "description",
                "owner",
                "role",
                "settings",
                "live_state",
            ],
        )
        if objects:
            Printer.print_header("Components:")
            dict_tabulate(objects, is_list_dict=True)

    if component:
        list_versions()
    else:
        list_components()


@hub.command()
@click.option(*OPTIONS_COMPONENT_HUB["args"], **OPTIONS_COMPONENT_HUB["kwargs"])
@click.option(*OPTIONS_COMPONENT_VERSION["args"], **OPTIONS_COMPONENT_VERSION["kwargs"])
@clean_outputs
def get(component, version):
    """Get info for a component hub by name, or owner/hub_name,
    or component version by name, name:tag, owner/name:tag.

    Examples:

    To get a default component hub:

    \b
    $ polyaxon hub get -h tensorboard

    To get by specific owner/name

    \b
    $ polyaxon hub get -p owner/my-component
    """
    owner, component_hub, component_version, is_version = get_info(component, version)

    try:
        polyaxon_client = get_current_or_public_client()
        if is_version:
            response = polyaxon_client.component_hub_v1.get_component_version(
                owner, component_hub, component_version
            )
            get_component_version_details(response)
        else:
            response = polyaxon_client.component_hub_v1.get_component_hub(
                owner, component_hub
            )
            response.owner = owner
            get_entity_details(response, "Component hub")
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e,
            message="Could not get `{}`.".format(
                component_version if is_version else component_hub
            ),
            sys_exit=True,
        )


@hub.command()
@click.option(*OPTIONS_COMPONENT_HUB["args"], **OPTIONS_COMPONENT_HUB["kwargs"])
@click.option(*OPTIONS_COMPONENT_VERSION["args"], **OPTIONS_COMPONENT_VERSION["kwargs"])
@clean_outputs
def delete(component, version):
    """Delete a component hub or a component version."""
    owner, component_hub, component_version, is_version = get_info(component, version)
    full_entity = (
        "{}/{}:{}".format(owner, component_hub, component_version)
        if is_version
        else "{}/{}".format(owner, component_hub)
    )

    if not click.confirm(
        "Are sure you want to delete component {} `{}`".format(
            "version" if is_version else "hub", full_entity
        )
    ):
        click.echo("Existing without deleting component hub.")
        sys.exit(1)

    try:
        polyaxon_client = PolyaxonClient()
        if is_version:
            polyaxon_client.component_hub_v1.delete_component_version(
                owner, component_hub, component_version
            )
        else:
            polyaxon_client.component_hub_v1.delete_component_hub(owner, component_hub)
        Printer.print_success(
            "Component {} `{}` was delete successfully".format(
                "version" if is_version else "hub", full_entity
            )
        )
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e,
            message="Could not delete component {} `{}`.".format(
                "version" if is_version else "hub", full_entity
            ),
        )
        sys.exit(1)


@hub.command()
@click.option(*OPTIONS_COMPONENT_HUB["args"], **OPTIONS_COMPONENT_HUB["kwargs"])
@click.option(*OPTIONS_COMPONENT_VERSION["args"], **OPTIONS_COMPONENT_VERSION["kwargs"])
@click.option(
    "--name",
    type=str,
    help="Name of the component hub, must be unique for the same user.",
)
@click.option("--description", type=str, help="Description of the component hub.")
@click.option(
    "--tags", type=str, help="Tags of the run, comma separated values (optional)."
)
@click.option(
    "--private",
    type=bool,
    help="Set the visibility of the component hub to private/public.",
)
@clean_outputs
def update(component, version, name, description, tags, private):
    """Update component hub.

    Uses /docs/core/cli/#caching

    Example:

    \b
    $ polyaxon hub update foobar --description="Image Classification with DL using TensorFlow"

    \b
    $ polyaxon hub update mike1/foobar --description="Image Classification with DL using TensorFlow"

    \b
    $ polyaxon hub update --tags="foo, bar"
    """
    owner, component_hub, component_version, is_version = get_info(component, version)
    full_entity = (
        "{}/{}:{}".format(owner, component_hub, component_version)
        if is_version
        else "{}/{}".format(owner, component_hub)
    )

    update_dict = {}
    if name:
        update_dict["name"] = name

    if description:
        update_dict["description"] = description

    tags = validate_tags(tags)
    if tags:
        update_dict["tags"] = tags

    if private is not None:
        update_dict["is_public"] = not private

    if not update_dict:
        Printer.print_warning(
            "No argument was provided to update the component {}.".format(
                "version" if is_version else "hub"
            )
        )
        sys.exit(1)

    try:
        polyaxon_client = PolyaxonClient()
        if is_version:
            response = polyaxon_client.component_hub_v1.patch_component_version(
                owner, component_hub, component_version, body=update_dict
            )
            Printer.print_success("Component version updated.")
            get_component_version_details(response)
        else:
            response = polyaxon_client.component_hub_v1.patch_component_hub(
                owner, component_hub, body=update_dict
            )
            Printer.print_success("Component updated.")
            get_entity_details(response, "Component hub")
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e,
            message="Could not update component {} `{}`.".format(
                "version" if is_version else "hub", full_entity
            ),
        )
        sys.exit(1)


@hub.command()
@click.option(*OPTIONS_COMPONENT_HUB["args"], **OPTIONS_COMPONENT_HUB["kwargs"])
@click.option(*OPTIONS_COMPONENT_VERSION["args"], **OPTIONS_COMPONENT_VERSION["kwargs"])
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
    help="Print the url of the dashboard for this component hub.",
)
@clean_outputs
def dashboard(component, version, yes, url):
    """Open this operation's dashboard details in browser."""
    owner, component_hub, component_version, is_version = get_info(component, version)
    subpath = (
        "{}/hub/{}/versions?version={}".format(owner, component_hub, component_version)
        if is_version
        else "{}/hub/{}".format(owner, component_hub)
    )

    hub_url = get_dashboard_url(subpath=subpath, use_cloud=settings.CLI_CONFIG.is_ce)
    if url:
        Printer.print_header("The dashboard is available at: {}".format(hub_url))
        sys.exit(0)
    if not yes:
        click.confirm(
            "Dashboard page will now open in your browser. Continue?",
            abort=True,
            default=True,
        )
    click.launch(hub_url)
