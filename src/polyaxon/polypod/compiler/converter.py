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

from typing import Any, Dict, Iterable, Optional

from kubernetes import client as k8s_client

from polyaxon.auxiliaries import V1PolyaxonInitContainer, V1PolyaxonSidecarContainer
from polyaxon.exceptions import PolyaxonCompilerError
from polyaxon.polyflow import V1CompiledOperation
from polyaxon.polypod.compiler.converters import CORE_CONVERTERS
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType


def convert(
    namespace: str,
    owner_name: str,
    project_name: str,
    run_name: str,
    run_uuid: str,
    run_path: str,
    compiled_operation: V1CompiledOperation,
    artifacts_store: Optional[V1ConnectionType],
    connection_by_names: Optional[Dict[str, V1ConnectionType]],
    secrets: Optional[Iterable[V1K8sResourceType]],
    config_maps: Optional[Iterable[V1K8sResourceType]],
    polyaxon_sidecar: V1PolyaxonSidecarContainer = None,
    polyaxon_init: V1PolyaxonInitContainer = None,
    default_sa: str = None,
    converters: Dict[str, Any] = CORE_CONVERTERS,
    internal_auth: bool = False,
    default_auth: bool = False,
) -> Dict:
    if compiled_operation.has_pipeline:
        raise PolyaxonCompilerError(
            "Converter Error. "
            "Specification with matrix/dag/schedule section is not supported in this function."
        )

    run_kind = compiled_operation.get_run_kind()
    if run_kind not in converters:
        raise PolyaxonCompilerError(
            "Converter Error. "
            "Specification with run kind: {} is not supported in this deployment version.".format(
                run_kind
            )
        )

    converter = converters[run_kind](
        owner_name=owner_name,
        project_name=project_name,
        run_name=run_name,
        run_uuid=run_uuid,
        namespace=namespace,
        polyaxon_init=polyaxon_init,
        polyaxon_sidecar=polyaxon_sidecar,
        internal_auth=internal_auth,
        run_path=run_path,
    )
    if converter:
        resource = converter.get_resource(
            compiled_operation=compiled_operation,
            artifacts_store=artifacts_store,
            connection_by_names=connection_by_names,
            secrets=secrets,
            config_maps=config_maps,
            default_sa=default_sa,
            default_auth=default_auth,
        )
        api = k8s_client.ApiClient()
        return api.sanitize_for_serialization(resource)
