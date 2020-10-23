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
from typing import Dict

from polyaxon.polyaxonfile import CompiledOperationSpecification, OperationSpecification
from polyaxon.polypod.compiler import converter, make
from polyaxon.polypod.compiler.config import PolypodConfig
from polyaxon.polypod.compiler.converters import PLATFORM_CONVERTERS


def convert(
    owner_name: str,
    project_name: str,
    run_name: str,
    run_uuid: str,
    content: str,
    default_auth: bool,
) -> Dict:
    polypod_config = PolypodConfig()
    compiled_operation = CompiledOperationSpecification.read(content)

    polypod_config.resolve(compiled_operation=compiled_operation)
    return converter.convert(
        compiled_operation=compiled_operation,
        owner_name=owner_name,
        project_name=project_name,
        run_name=run_name,
        run_uuid=run_uuid,
        namespace=polypod_config.namespace,
        polyaxon_init=polypod_config.polyaxon_init,
        polyaxon_sidecar=polypod_config.polyaxon_sidecar,
        run_path=run_uuid,
        artifacts_store=polypod_config.artifacts_store,
        connection_by_names=polypod_config.connection_by_names,
        secrets=polypod_config.secrets,
        config_maps=polypod_config.config_maps,
        default_sa=polypod_config.default_sa,
        converters=PLATFORM_CONVERTERS,
        default_auth=default_auth,
    )


def make_and_convert(
    owner_name: str,
    project_name: str,
    run_uuid: str,
    run_name: str,
    content: str,
    default_auth: bool = False,
):
    operation = OperationSpecification.read(content)
    compiled_operation = OperationSpecification.compile_operation(operation)
    return make(
        owner_name=owner_name,
        project_name=project_name,
        project_uuid=project_name,
        run_uuid=run_uuid,
        run_name=run_name,
        run_path=run_uuid,
        compiled_operation=compiled_operation,
        params=operation.params,
        converters=PLATFORM_CONVERTERS,
        default_auth=default_auth,
    )
