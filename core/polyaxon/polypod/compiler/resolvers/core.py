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

from typing import Dict, Optional

from polyaxon.polyaxonfile import CompiledOperationSpecification
from polyaxon.polyflow import V1CompiledOperation, V1RunKind
from polyaxon.polypod.compiler.resolvers.base import BaseResolver


class CoreResolver(BaseResolver):
    KINDS = {
        V1RunKind.JOB,
        V1RunKind.SERVICE,
        V1RunKind.MPIJOB,
        V1RunKind.TFJOB,
        V1RunKind.PYTORCHJOB,
        V1RunKind.NOTIFIER,
    }

    def __init__(
        self,
        compiled_operation: V1CompiledOperation,
        owner_name: str,
        project_name: str,
        run_name: str,
        run_path: str,
        params: Optional[Dict],
        project_uuid: str = None,
        run_uuid: str = None,
        run=None,
    ):
        super().__init__(
            run=run,
            compiled_operation=compiled_operation,
            owner_name=owner_name,
            project_name=project_name,
            project_uuid=project_uuid or project_name,
            run_name=run_name,
            run_uuid=run_uuid or run_name,
            run_path=run_path,
            params=params,
        )

    def resolve_params(self):
        self.compiled_operation = CompiledOperationSpecification.apply_params(
            config=self.compiled_operation, params=self.params, context=self.globals,
        )
