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
from datetime import datetime

from marshmallow import ValidationError

from coredb.abstracts.runs import BaseRun
from coredb.managers.artifacts import set_artifacts
from polyaxon.exceptions import PolyaxonCompilerError, PolyaxonSchemaError
from polyaxon.polyflow import V1CompiledOperation
from polyaxon.polypod.compiler import resolver
from polycommon.exceptions import AccessNotAuthorized, AccessNotFound


class CorePlatformResolver(resolver.BaseResolver):
    def resolve_params(self):
        self.params = self.run.params or {}

    def resolve_io(self):
        if self.compiled_operation.inputs:
            self.run.inputs = {
                io.name: io.value for io in self.compiled_operation.inputs
            }
        if self.compiled_operation.outputs:
            self.run.outputs = {
                io.name: io.value for io in self.compiled_operation.outputs
            }

    def _resolve_artifacts_lineage_state(self):
        if self.artifacts:
            set_artifacts(self.run, self.artifacts)

    def resolve_state(self):
        self.run.content = self.compiled_operation.to_dict(dump=True)
        if (
            self.compiled_operation.is_service_run
            and self.compiled_operation.run.rewrite_path
        ):
            self.run.meta_info["rewrite_path"] = True
        self.run.save(update_fields=["content", "inputs", "outputs", "meta_info"])
        self._resolve_artifacts_lineage_state()


def resolve(run: BaseRun, compiled_at: datetime = None, resolver_cls=None):
    resolver_cls = resolver_cls or CorePlatformResolver
    try:
        project = run.project
        return resolver.resolve(
            run=run,
            compiled_operation=V1CompiledOperation.read(run.content),
            owner_name=project.owner.name,
            project_name=project.name,
            project_uuid=project.uuid.hex,
            run_uuid=run.uuid.hex,
            run_name=run.name,
            run_path=run.subpath,
            resolver_cls=resolver_cls,
            params=None,
            compiled_at=compiled_at,
            created_at=run.created_at,
            cloning_kind=run.cloning_kind,
            original_uuid=run.original.uuid.hex if run.original_id else None,
        )
    except (
        AccessNotAuthorized,
        AccessNotFound,
        ValidationError,
        PolyaxonSchemaError,
    ) as e:
        raise PolyaxonCompilerError("Compilation Error: %s" % e) from e
