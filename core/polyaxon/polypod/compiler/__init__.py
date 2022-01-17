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
from typing import Any, Dict, Optional

from polyaxon.polyflow import V1CompiledOperation
from polyaxon.polypod.compiler import converter, resolver


def make(
    owner_name: str,
    project_name: str,
    project_uuid: str,
    run_name: str,
    run_uuid: str,
    run_path: str,
    compiled_operation: V1CompiledOperation,
    params: Optional[Dict],
    default_sa: str = None,
    internal_auth: bool = False,
    default_auth: bool = False,
    converters: Dict[str, Any] = converter.CORE_CONVERTERS,
):
    resolver_obj, compiled_operation = resolver.resolve(
        compiled_operation=compiled_operation,
        owner_name=owner_name,
        project_name=project_name,
        project_uuid=project_uuid,
        run_name=run_name,
        run_path=run_path,
        run_uuid=run_uuid,
        params=params,
    )
    return converter.convert(
        namespace=resolver_obj.namespace,
        owner_name=resolver_obj.owner_name,
        project_name=resolver_obj.project_name,
        run_name=resolver_obj.run_name,
        run_path=resolver_obj.run_path,
        run_uuid=resolver_obj.run_uuid,
        compiled_operation=compiled_operation,
        connection_by_names=resolver_obj.connection_by_names,
        internal_auth=internal_auth,
        artifacts_store=resolver_obj.artifacts_store,
        secrets=resolver_obj.secrets,
        config_maps=resolver_obj.config_maps,
        polyaxon_sidecar=resolver_obj.polyaxon_sidecar,
        polyaxon_init=resolver_obj.polyaxon_init,
        default_sa=default_sa,
        converters=converters,
        default_auth=default_auth,
    )
