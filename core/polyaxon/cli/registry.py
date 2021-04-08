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

import click

from polyaxon_sdk import V1ModelRegistry, V1ModelVersion
from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon.cli.dashboard import get_dashboard_url
from polyaxon.cli.errors import handle_cli_error
from polyaxon.cli.options import (
    OPTIONS_MODEL_REGISTRY,
    OPTIONS_MODEL_VERSION,
    OPTIONS_OWNER,
)
from polyaxon.cli.utils import get_entity_details
from polyaxon.client import PolyaxonClient
from polyaxon.env_vars.getters import get_model_info
from polyaxon.env_vars.getters.user import get_local_owner
from polyaxon.exceptions import PolyaxonException
from polyaxon.logger import clean_outputs
from polyaxon.utils.formatting import (
    Printer,
    dict_tabulate,
    dict_to_tabulate,
    get_meta_response,
    list_dicts_to_tabulate,
)
from polyaxon.utils.query_params import get_query_params
from polyaxon.utils.validation import validate_tags


def get_model_version_details(response):
    metadata = response.metadata
    response = dict_to_tabulate(
        response.to_dict(), humanize_values=True, exclude_attrs=["metadata"]
    )

    Printer.print_header("Model version info:")
    dict_tabulate(response)

    if metadata:
        Printer.print_header("Metadata:")
        click.echo(metadata)


def get_info(model: str = None, version: str = None):
    if not any([model, version]):
        Printer.print_error(
            "A model registry or a model version is required.", sys_exit=True
        )
    if all([model, version]):
        Printer.print_error(
            "Only a model registry or a model version is required, not both.",
            sys_exit=True,
        )

    if model:
        entity = model
        entity_name = "model registry"
        is_version = False
    else:
        entity = version
        entity_name = "model version"
        is_version = True

    try:
        owner, model_registry, model_version = get_model_info(
            entity=entity, entity_name=entity_name, is_cli=True
        )
        return owner, model_registry, model_version, is_version
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
def registry():
    """Commands for model registry."""


@registry.command()
@click.option(
    "--name",
    type=str,
    help="The model registry name, e.g. 'model-A' or 'acme/model-A:latest'.",
)
@click.option("--description", type=str, help="Description of the model.")
@click.option("--tags", type=str, help="Tags of the model, comma separated values.")
@click.option(
    "--public", is_flag=True, help="Set the visibility of the model to public."
)
@clean_outputs
def create(name, description, tags, public):
    """Create a new model.

    Example:

    \b
    $ polyaxon registry create --name=kaniko --description="Tool to build container images"

    \b
    $ polyaxon registry create --name=owner/name --description="Model description"
    """
    if not name:
        Printer.print_error(
            "Please provide a name to create a model registry.",
            command_help="registry create",
            sys_exit=True,
        )
    owner, registry_name, _, _ = get_info(name, None)

    tags = validate_tags(tags)

    if not owner or not registry_name:
        Printer.print_error(
            "Please provide a valid model name with --name=owner/registry-name. "
        )
        sys.exit(1)

    try:
        registry_config = V1ModelRegistry(
            name=registry_name, description=description, tags=tags, is_public=public
        )
        polyaxon_client = PolyaxonClient()
        _registry = polyaxon_client.model_registry_v1.create_model_registry(
            owner, registry_config
        )
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not create model registry `{}`.".format(registry_name)
        )
        sys.exit(1)

    Printer.print_success(
        "Model registry `{}` was created successfully.".format(_registry.name)
    )
    click.echo(
        "You can view this model registry on Polyaxon UI: {}".format(
            get_dashboard_url(subpath="{}/registry/{}".format(owner, _registry.name))
        )
    )


@registry.command()
@click.option(
    "--name",
    type=str,
    help="The model version name, e.g. 'kaniko' or 'kaniko:1.2' "
    "or 'acme/kaniko:latest' or 'acme/kaniko:dev'.",
)
@click.option("--description", type=str, help="Description of the version.")
@click.option("--tags", type=str, help="Tags of the version, comma separated values.")
@click.option(
    "--run-uid", "-uid", type=str, help="The run to link to this model version."
)
@clean_outputs
def push(name, description, tags, run_uid):
    """Push a new model version.
    If the name corresponds to an existing model version, it will be updated.

    Example:

    \b
    $ polyaxon registry push -f polyaxonfile.yaml --name=kaniko:latest --description="Tool to build container images"

    \b
    $ polyaxon registry push -f polyaxonfile.yaml --name=owner/name:v1 --description="Model description"
    """
    if not name:
        Printer.print_error(
            "Please provide a name to create a model version.",
            command_help="registry push",
            sys_exit=True,
        )
    owner, registry_name, version, is_version = get_info(None, name)
    tags = validate_tags(tags)

    if not owner or not registry_name or not version:
        Printer.print_error(
            "Please provide a valid model version with --name=owner/registry-name:version. "
        )
        sys.exit(1)

    polyaxon_client = PolyaxonClient()
    try:
        polyaxon_client.model_registry_v1.get_model_version(
            owner, registry_name, version
        )
        to_update = True
    except (ApiException, HTTPError):
        to_update = False

    if to_update:
        if not click.confirm(
            "A model version {}/{}:{} already exists. "
            "Do you want to push force this version?".format(
                owner, registry_name, version
            )
        ):
            click.echo("Existing without pushing model version.")
            sys.exit(1)

    try:
        registry_config = V1ModelVersion(
            name=version,
            description=description,
            tags=tags,
            run=run_uid,
        )
        if to_update:
            _version = polyaxon_client.model_registry_v1.update_model_version(
                owner,
                registry_name,
                version,
                registry_config,
            )
        else:
            _version = polyaxon_client.model_registry_v1.create_model_version(
                owner,
                registry_name,
                registry_config,
            )
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not create model version `{}`.".format(registry_name)
        )
        sys.exit(1)

    Printer.print_success(
        "Model version `{}` was created successfully.".format(_version.name)
    )
    click.echo(
        "You can view this model version on Polyaxon UI: {}".format(
            get_dashboard_url(
                subpath="{}/registry/{}/versions/{}".format(
                    owner, registry_name, _version.name
                )
            )
        )
    )


@registry.command()
@click.option(*OPTIONS_OWNER["args"], **OPTIONS_OWNER["kwargs"])
@click.option(*OPTIONS_MODEL_REGISTRY["args"], **OPTIONS_MODEL_REGISTRY["kwargs"])
@click.option(
    "--query",
    "-q",
    type=str,
    help="To filter the model registry/versions based on this query spec.",
)
@click.option(
    "--sort",
    "-s",
    type=str,
    help="To order the model registry/versions based on the sort spec.",
)
@click.option("--limit", type=int, help="To limit the list of model registry/versions.")
@click.option(
    "--offset", type=int, help="To offset the list of model registry/versions."
)
@clean_outputs
def ls(owner, model, query, sort, limit, offset):
    """List model registry/versions by owner or owner/model."""
    if owner and model:
        Printer.print_error(
            "Only an owner or a model is required, not both.", sys_exit=True
        )
    if model:
        owner, model_registry, model_version, is_version = get_info(model, None)
    elif not owner:
        owner = get_local_owner(is_cli=True)

    if not owner:
        Printer.print_error(
            "Please provide a valid owner --owner/-o or a model --model/-m."
        )
        sys.exit(1)

    def list_versions():
        model_info = "<owner: {}> <model: {}>".format(owner, model_registry)
        try:
            polyaxon_client = PolyaxonClient()
            params = get_query_params(
                limit=limit, offset=offset, query=query, sort=sort
            )
            response = polyaxon_client.model_registry_v1.list_model_versions(
                owner, model_registry, **params
            )
        except (ApiException, HTTPError) as e:
            message = "Could not get list of model version."
            handle_cli_error(e, message=message)
            sys.exit(1)

        meta = get_meta_response(response)
        if meta:
            Printer.print_header("Versions for {}".format(model_info))
            Printer.print_header("Navigation:")
            dict_tabulate(meta)
        else:
            Printer.print_header("No version found for {}".format(model_info))

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
            Printer.print_header("Model versions:")
            dict_tabulate(objects, is_list_dict=True)

    def list_models():
        try:
            polyaxon_client = PolyaxonClient()
            params = get_query_params(
                limit=limit, offset=offset, query=query, sort=sort
            )
            response = polyaxon_client.model_registry_v1.list_model_registries(
                owner, **params
            )
        except (ApiException, HTTPError) as e:
            message = "Could not get list of models."
            handle_cli_error(e, message=message)
            sys.exit(1)

        meta = get_meta_response(response)
        if meta:
            Printer.print_header("Models for owner {}".format(owner))
            Printer.print_header("Navigation:")
            dict_tabulate(meta)
        else:
            Printer.print_header("No model registry found for owner {}".format(owner))

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
            Printer.print_header("Models:")
            dict_tabulate(objects, is_list_dict=True)

    if model:
        list_versions()
    else:
        list_models()


@registry.command()
@click.option(*OPTIONS_MODEL_REGISTRY["args"], **OPTIONS_MODEL_REGISTRY["kwargs"])
@click.option(*OPTIONS_MODEL_VERSION["args"], **OPTIONS_MODEL_VERSION["kwargs"])
@clean_outputs
def get(model, version):
    """Get info for a model registry by name, or owner/registry_name,
    or model version by name, name:tag, owner/name:tag.

    Examples:

    To get a default model registry:

    \b
    $ polyaxon registry get -h tensorboard

    To get by specific owner/name

    \b
    $ polyaxon registry get -p owner/my-model
    """
    owner, model_registry, model_version, is_version = get_info(model, version)

    try:
        polyaxon_client = PolyaxonClient()
        if is_version:
            response = polyaxon_client.model_registry_v1.get_model_version(
                owner, model_registry, model_version
            )
            get_model_version_details(response)
        else:
            response = polyaxon_client.model_registry_v1.get_model_registry(
                owner, model_registry
            )
            response.owner = owner
            get_entity_details(response, "Model registry")
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e,
            message="Could not get `{}`.".format(
                model_version if is_version else model_registry
            ),
            sys_exit=True,
        )


@registry.command()
@click.option(*OPTIONS_MODEL_REGISTRY["args"], **OPTIONS_MODEL_REGISTRY["kwargs"])
@click.option(*OPTIONS_MODEL_VERSION["args"], **OPTIONS_MODEL_VERSION["kwargs"])
@clean_outputs
def delete(model, version):
    """Delete a model registry or a model version."""
    owner, model_registry, model_version, is_version = get_info(model, version)
    full_entity = (
        "{}/{}:{}".format(owner, model_registry, model_version)
        if is_version
        else "{}/{}".format(owner, model_registry)
    )

    if not click.confirm(
        "Are sure you want to delete model {} `{}`".format(
            "version" if is_version else "registry", full_entity
        )
    ):
        click.echo("Existing without deleting model registry.")
        sys.exit(1)

    try:
        polyaxon_client = PolyaxonClient()
        if is_version:
            polyaxon_client.model_registry_v1.delete_model_version(
                owner, model_registry, model_version
            )
        else:
            polyaxon_client.model_registry_v1.delete_model_registry(
                owner, model_registry
            )
        Printer.print_success(
            "Model {} `{}` was delete successfully".format(
                "version" if is_version else "registry", full_entity
            )
        )
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e,
            message="Could not delete model {} `{}`.".format(
                "version" if is_version else "registry", full_entity
            ),
        )
        sys.exit(1)


@registry.command()
@click.option(*OPTIONS_MODEL_REGISTRY["args"], **OPTIONS_MODEL_REGISTRY["kwargs"])
@click.option(*OPTIONS_MODEL_VERSION["args"], **OPTIONS_MODEL_VERSION["kwargs"])
@click.option(
    "--name",
    type=str,
    help="Name of the model registry, must be unique for the same user.",
)
@click.option("--description", type=str, help="Description of the model registry.")
@click.option(
    "--tags", type=str, help="Tags of the run, comma separated values (optional)."
)
@click.option(
    "--private",
    type=bool,
    help="Set the visibility of the model registry to private/public.",
)
@clean_outputs
def update(model, version, name, description, tags, private):
    """Update model registry.

    Uses /docs/core/cli/#caching

    Example:

    \b
    $ polyaxon registry update foobar --description="Image Classification with DL using TensorFlow"

    \b
    $ polyaxon registry update mike1/foobar --description="Image Classification with DL using TensorFlow"

    \b
    $ polyaxon registry update --tags="foo, bar"
    """
    owner, model_registry, model_version, is_version = get_info(model, version)
    full_entity = (
        "{}/{}:{}".format(owner, model_registry, model_version)
        if is_version
        else "{}/{}".format(owner, model_registry)
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
            "No argument was provided to update the model {}.".format(
                "version" if is_version else "registry"
            )
        )
        sys.exit(1)

    try:
        polyaxon_client = PolyaxonClient()
        if is_version:
            response = polyaxon_client.model_registry_v1.patch_model_version(
                owner, model_registry, model_version, body=update_dict
            )
            Printer.print_success("Model version updated.")
            get_model_version_details(response)
        else:
            response = polyaxon_client.model_registry_v1.patch_model_registry(
                owner, model_registry, body=update_dict
            )
            Printer.print_success("Model updated.")
            get_entity_details(response, "Model registry")
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e,
            message="Could not update model {} `{}`.".format(
                "version" if is_version else "registry", full_entity
            ),
        )
        sys.exit(1)


@registry.command()
@click.option(*OPTIONS_MODEL_REGISTRY["args"], **OPTIONS_MODEL_REGISTRY["kwargs"])
@click.option(*OPTIONS_MODEL_VERSION["args"], **OPTIONS_MODEL_VERSION["kwargs"])
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
    help="Print the url of the dashboard for this model registry.",
)
@clean_outputs
def dashboard(model, version, yes, url):
    """Open this operation's dashboard details in browser."""
    owner, model_registry, model_version, is_version = get_info(model, version)
    subpath = (
        "{}/registry/{}/versions?version={}".format(
            owner, model_registry, model_version
        )
        if is_version
        else "{}/registry/{}".format(owner, model_registry)
    )

    registry_url = get_dashboard_url(subpath=subpath)
    if url:
        Printer.print_header("The dashboard is available at: {}".format(registry_url))
        sys.exit(0)
    if not yes:
        click.confirm(
            "Dashboard page will now open in your browser. Continue?",
            abort=True,
            default=True,
        )
    click.launch(registry_url)
