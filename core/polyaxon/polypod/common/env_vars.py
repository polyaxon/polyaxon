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

import json

from typing import Any, Iterable, List, Optional

from polyaxon.connections.reader import (
    get_connection_context_path_env_name,
    get_connection_schema_env_name,
)
from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_API_VERSION,
    POLYAXON_KEYS_AUTH_TOKEN,
    POLYAXON_KEYS_AUTHENTICATION_TYPE,
    POLYAXON_KEYS_HEADER,
    POLYAXON_KEYS_HEADER_SERVICE,
    POLYAXON_KEYS_HOST,
    POLYAXON_KEYS_IS_MANAGED,
    POLYAXON_KEYS_K8S_NAMESPACE,
    POLYAXON_KEYS_K8S_NODE_NAME,
    POLYAXON_KEYS_K8S_POD_ID,
    POLYAXON_KEYS_RUN_INSTANCE,
    POLYAXON_KEYS_SECRET_INTERNAL_TOKEN,
    POLYAXON_KEYS_SECRET_KEY,
)
from polyaxon.exceptions import PolypodException
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common.accelerators import requests_gpu
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType
from polyaxon.services.headers import PolyaxonServiceHeaders


def get_str_var(value: Any) -> str:
    if value is not None and not isinstance(value, str):
        try:
            value = json.dumps(value)
        except (ValueError, TypeError) as e:
            raise PolypodException(e)
    return value or ""


def get_env_var(name: str, value: Any) -> k8s_schemas.V1EnvVar:
    if not isinstance(value, str):
        try:
            value = json.dumps(value)
        except (ValueError, TypeError) as e:
            raise PolypodException(e)

    return k8s_schemas.V1EnvVar(name=name, value=value)


def get_kv_env_vars(kv_env_vars: List[List]) -> List[k8s_schemas.V1EnvVar]:
    env_vars = []
    if not kv_env_vars:
        return env_vars

    for kv_env_var in kv_env_vars:
        if not kv_env_var or not len(kv_env_var) == 2:
            raise PolypodException(
                "Received a wrong a key value env var `{}`".format(kv_env_var)
            )
        env_vars.append(get_env_var(name=kv_env_var[0], value=kv_env_var[1]))

    return env_vars


def get_resources_env_vars(
    resources: k8s_schemas.V1ResourceRequirements,
) -> List[k8s_schemas.V1EnvVar]:
    env_vars = []
    has_gpu = requests_gpu(resources)

    # Fix https://github.com/kubernetes/kubernetes/issues/59629
    # When resources.gpu.limits is not set or set to 0, we explicitly
    # pass NVIDIA_VISIBLE_DEVICES=none into container to avoid exposing GPUs.
    if not has_gpu:
        env_vars.append(
            k8s_schemas.V1EnvVar(name="NVIDIA_VISIBLE_DEVICES", value="none")
        )

    return env_vars


def get_from_config_map(
    key_name: str, config_map_key_name: str, config_map_ref_name: str
) -> k8s_schemas.V1EnvVar:
    config_map_ref_name = config_map_ref_name
    config_map_key_ref = k8s_schemas.V1ConfigMapKeySelector(
        name=config_map_ref_name, key=config_map_key_name
    )
    value_from = k8s_schemas.V1EnvVarSource(config_map_key_ref=config_map_key_ref)
    return k8s_schemas.V1EnvVar(name=key_name, value_from=value_from)


def get_from_secret(
    key_name: str, secret_key_name: str, secret_ref_name: str
) -> k8s_schemas.V1EnvVar:
    secret_ref_name = secret_ref_name
    secret_key_ref = k8s_schemas.V1SecretKeySelector(
        name=secret_ref_name, key=secret_key_name
    )
    value_from = k8s_schemas.V1EnvVarSource(secret_key_ref=secret_key_ref)
    return k8s_schemas.V1EnvVar(name=key_name, value_from=value_from)


def get_items_from_secret(secret: V1K8sResourceType) -> List[k8s_schemas.V1EnvVar]:
    items_from = []
    if not secret or not secret.schema.items or secret.schema.mount_path:
        return items_from

    for item in secret.schema.items:
        items_from.append(
            get_from_secret(
                key_name=item, secret_key_name=item, secret_ref_name=secret.schema.name
            )
        )
    return items_from


def get_items_from_config_map(
    config_map: V1K8sResourceType,
) -> List[k8s_schemas.V1EnvVar]:
    items_from = []
    if not config_map or not config_map.schema.items:
        return items_from

    for item in config_map.schema.items:
        items_from.append(
            get_from_config_map(
                key_name=item,
                config_map_key_name=item,
                config_map_ref_name=config_map.schema.name,
            )
        )
    return items_from


def get_from_field_ref(name: str, field_path: str) -> k8s_schemas.V1EnvVar:
    field_ref = k8s_schemas.V1ObjectFieldSelector(field_path=field_path)
    value_from = k8s_schemas.V1EnvVarSource(field_ref=field_ref)
    return k8s_schemas.V1EnvVar(name=name, value_from=value_from)


def get_env_vars_from_k8s_resources(
    secrets: Iterable[V1K8sResourceType], config_maps: Iterable[V1K8sResourceType]
) -> List[k8s_schemas.V1EnvVar]:
    secrets = secrets or []
    config_maps = config_maps or []

    env_vars = []
    for secret in secrets:
        env_vars += get_items_from_secret(secret=secret)
    for config_map in config_maps:
        env_vars += get_items_from_config_map(config_map=config_map)

    return env_vars


def get_env_from_secret(
    secret: V1K8sResourceType,
) -> Optional[k8s_schemas.V1EnvFromSource]:
    if not secret or secret.schema.items or secret.schema.mount_path:
        return None

    return k8s_schemas.V1EnvFromSource(secret_ref={"name": secret.schema.name})


def get_env_from_secrets(
    secrets: Iterable[V1K8sResourceType],
) -> List[k8s_schemas.V1EnvFromSource]:
    secrets = secrets or []
    results = [get_env_from_secret(secret=secret) for secret in secrets]
    return [r for r in results if r]


def get_env_from_config_map(
    config_map: V1K8sResourceType,
) -> Optional[k8s_schemas.V1EnvFromSource]:
    if not config_map or config_map.schema.items or config_map.schema.mount_path:
        return None

    return k8s_schemas.V1EnvFromSource(config_map_ref={"name": config_map.schema.name})


def get_env_from_config_maps(
    config_maps: Iterable[V1K8sResourceType],
) -> List[k8s_schemas.V1EnvFromSource]:
    config_maps = config_maps or []
    results = [
        get_env_from_config_map(config_map=config_map) for config_map in config_maps
    ]
    return [r for r in results if r]


def get_env_from_k8s_resources(
    secrets: Iterable[V1K8sResourceType], config_maps: Iterable[V1K8sResourceType]
) -> List[k8s_schemas.V1EnvFromSource]:
    secrets = secrets or []
    config_maps = config_maps or []

    env_vars = []
    env_vars += get_env_from_secrets(secrets=secrets)
    env_vars += get_env_from_config_maps(config_maps=config_maps)
    return env_vars


def get_base_env_vars():
    return [
        get_from_field_ref(
            name=POLYAXON_KEYS_K8S_NODE_NAME, field_path="spec.nodeName"
        ),
        get_from_field_ref(
            name=POLYAXON_KEYS_K8S_NAMESPACE, field_path="metadata.namespace"
        ),
        get_from_field_ref(name=POLYAXON_KEYS_K8S_POD_ID, field_path="metadata.name"),
    ]


def get_service_env_vars(
    header: str,
    service_header: str,
    include_secret_key: bool,
    include_internal_token: bool,
    include_agent_token: bool,
    authentication_type: str,
    polyaxon_default_secret_ref: str,
    polyaxon_agent_secret_ref: str,
    api_host: str,
    api_version: str,
    run_instance: str,
) -> List[k8s_schemas.V1EnvVar]:
    env_vars = get_base_env_vars() + [
        get_env_var(name=POLYAXON_KEYS_HOST, value=api_host),
        get_env_var(name=POLYAXON_KEYS_IS_MANAGED, value=True),
        get_env_var(name=POLYAXON_KEYS_API_VERSION, value=api_version),
        get_run_instance_env_var(run_instance),
    ]
    if header:
        env_vars.append(
            get_env_var(
                name=POLYAXON_KEYS_HEADER,
                value=PolyaxonServiceHeaders.get_header(header),
            )
        )
    if service_header:
        env_vars.append(
            get_env_var(name=POLYAXON_KEYS_HEADER_SERVICE, value=service_header)
        )
    if include_secret_key:
        env_vars.append(
            get_from_secret(
                key_name=POLYAXON_KEYS_SECRET_KEY,
                secret_key_name=POLYAXON_KEYS_SECRET_KEY,
                secret_ref_name=polyaxon_default_secret_ref,
            )
        )
    internal = False
    if include_internal_token and polyaxon_default_secret_ref:
        internal = True
        env_vars.append(
            get_from_secret(
                POLYAXON_KEYS_SECRET_INTERNAL_TOKEN,
                POLYAXON_KEYS_SECRET_INTERNAL_TOKEN,
                secret_ref_name=polyaxon_default_secret_ref,
            )
        )
    if include_agent_token and polyaxon_agent_secret_ref:
        if internal:
            raise PolypodException(
                "A service cannot have internal token and agent token."
            )
        env_vars.append(
            get_from_secret(
                POLYAXON_KEYS_AUTH_TOKEN,
                POLYAXON_KEYS_AUTH_TOKEN,
                secret_ref_name=polyaxon_agent_secret_ref,
            )
        )
    if authentication_type:
        env_vars.append(
            get_env_var(
                name=POLYAXON_KEYS_AUTHENTICATION_TYPE, value=authentication_type
            )
        )
    return env_vars


def get_run_instance_env_var(run_instance: str) -> k8s_schemas.V1EnvVar:
    return get_env_var(name=POLYAXON_KEYS_RUN_INSTANCE, value=run_instance)


def get_connection_env_var(
    connection: V1ConnectionType, secret: Optional[V1K8sResourceType]
):
    env_vars = []
    if not connection:
        return env_vars

    connection_schema_env_name = get_connection_schema_env_name(connection.name)
    env_vars = [get_env_var(connection_schema_env_name, connection.to_dict())]

    if not secret or not secret.schema.mount_path:
        return env_vars

    context_secret_env_name = get_connection_context_path_env_name(connection.name)
    env_vars += [get_env_var(context_secret_env_name, secret.schema.mount_path)]

    return env_vars
