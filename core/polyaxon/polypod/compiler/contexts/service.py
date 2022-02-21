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

from typing import Dict

from polyaxon.api import (
    EXTERNAL_V1_LOCATION,
    REWRITE_EXTERNAL_V1_LOCATION,
    REWRITE_SERVICES_V1_LOCATION,
    SERVICES_V1_LOCATION,
)
from polyaxon.polyflow import V1CompiledOperation
from polyaxon.polypod.compiler.contexts.base import BaseContextsManager
from polyaxon.schemas.types import V1ConnectionType
from polyaxon.utils.urls_utils import get_proxy_run_url


class ServiceContextsManager(BaseContextsManager):
    @classmethod
    def resolve(
        cls,
        namespace: str,
        owner_name: str,
        project_name: str,
        run_uuid: str,
        contexts: Dict,
        compiled_operation: V1CompiledOperation,
        connection_by_names: Dict[str, V1ConnectionType],
    ) -> Dict:
        contexts = cls._resolver_replica(
            contexts=contexts,
            init=compiled_operation.run.init,
            connections=compiled_operation.run.connections,
            connection_by_names=connection_by_names,
        )
        if compiled_operation.is_service_run:
            contexts["globals"]["ports"] = compiled_operation.run.ports
            if compiled_operation.run.is_external:
                service = (
                    REWRITE_EXTERNAL_V1_LOCATION
                    if compiled_operation.run.rewrite_path
                    else EXTERNAL_V1_LOCATION
                )
            else:
                service = (
                    REWRITE_SERVICES_V1_LOCATION
                    if compiled_operation.run.rewrite_path
                    else SERVICES_V1_LOCATION
                )
            base_url = get_proxy_run_url(
                service=service,
                namespace=namespace,
                owner=owner_name,
                project=project_name,
                run_uuid=run_uuid,
            )
            contexts["globals"]["base_url"] = base_url

        return contexts
