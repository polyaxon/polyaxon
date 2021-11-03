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
from datetime import datetime
from typing import List, Optional

from marshmallow import ValidationError as MarshmallowValidationError
from rest_framework.exceptions import ValidationError

from coredb.abstracts.runs import BaseRun
from coredb.managers.artifacts import set_artifacts
from polyaxon.constants.metadata import (
    META_COPY_ARTIFACTS,
    META_DESTINATION_IMAGE,
    META_REWRITE_PATH,
    META_UPLOAD_ARTIFACTS,
)
from polyaxon.exceptions import PolyaxonCompilerError, PolyaxonSchemaError
from polyaxon.polyaxonfile import CompiledOperationSpecification
from polyaxon.polyflow import V1CompiledOperation, V1Init, V1Operation
from polyaxon.polypod.compiler import resolver
from polyaxon.polypod.compiler.lineage.artifacts_collector import (
    collect_lineage_artifacts_path,
)
from polyaxon.schemas import V1RunPending
from polyaxon.schemas.types import V1ArtifactsType
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

    def _get_meta_artifacts_presets(self) -> List:
        if not self.run.meta_info or META_COPY_ARTIFACTS not in self.run.meta_info:
            return []

        artifacts = self.run.meta_info.pop(META_COPY_ARTIFACTS)
        artifacts = V1ArtifactsType.read(artifacts)

        def get_relative_to_run_artifacts(v: str):
            paths = v.split("/")[1:]
            paths = ["{{ globals.run_artifacts_path }}"] + paths
            return "/".join(paths)

        # Populate all paths
        if artifacts.dirs:
            artifacts.dirs = [
                [d, get_relative_to_run_artifacts(d)] for d in artifacts.dirs
            ]
        if artifacts.files:
            artifacts.files = [
                [d, get_relative_to_run_artifacts(d)] for d in artifacts.files
            ]
        init = V1Init(artifacts=artifacts)
        return [{"runPatch": {"init": [init.to_dict()]}}]

    def _get_meta_destination_image(self) -> Optional[str]:
        meta_info = self.run.meta_info or {}
        return meta_info.get(META_DESTINATION_IMAGE)

    def resolve_presets(self):
        for preset in self._get_meta_artifacts_presets():
            self.compiled_operation = CompiledOperationSpecification.apply_preset(
                config=self.compiled_operation, preset=preset
            )

    def _persist_artifacts(self):
        if self.artifacts:
            set_artifacts(self.run, self.artifacts)

    def _resolve_artifacts_lineage_state(self):
        self.artifacts = self.artifacts or []
        # Check upload and add it as a lineage
        if self.run.meta_info and META_UPLOAD_ARTIFACTS in self.run.meta_info:
            artifacts_path = self.run.meta_info[META_UPLOAD_ARTIFACTS]
            if artifacts_path:
                upload_artifact = collect_lineage_artifacts_path(artifacts_path)
                self.artifacts.append(upload_artifact)
        self._persist_artifacts()

    def _check_approval(self):
        if self.compiled_operation.is_approved is False and self.run.pending is None:
            self.run.pending = V1RunPending.APPROVAL
            return True
        return False

    def persist_state(self):
        self.run.content = self.compiled_operation.to_dict(dump=True)
        if (
            self.compiled_operation.is_service_run
            and self.compiled_operation.run.rewrite_path
        ):
            self.run.meta_info[META_REWRITE_PATH] = True
        update_fields = ["content", "inputs", "outputs", "meta_info"]
        if self._check_approval():
            update_fields.append("pending")
        self.run.save(update_fields=update_fields)
        self._resolve_artifacts_lineage_state()


def resolve(
    run: BaseRun, compiled_at: datetime = None, eager: bool = False, resolver_cls=None
):
    resolver_cls = resolver_cls or CorePlatformResolver
    try:
        compiled_operation = V1CompiledOperation.read(run.content)
        project = run.project
        return resolver.resolve(
            run=run,
            compiled_operation=compiled_operation,
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
            is_independent=bool(run.pipeline_id),
            eager=eager,
        )
    except (
        AccessNotAuthorized,
        AccessNotFound,
    ) as e:
        raise PolyaxonCompilerError("Access Error: %s" % e) from e
    except (
        AccessNotAuthorized,
        AccessNotFound,
        MarshmallowValidationError,
        PolyaxonSchemaError,
        ValidationError,
    ) as e:
        raise PolyaxonCompilerError("Compilation Error: %s" % e) from e


def resolve_hooks(run: BaseRun, resolver_cls=None) -> List[V1Operation]:
    resolver_cls = resolver_cls or CorePlatformResolver
    try:
        compiled_operation = V1CompiledOperation.read(run.content)
        project = run.project
        return resolver.resolve_hooks(
            run=run,
            compiled_operation=compiled_operation,
            owner_name=project.owner.name,
            project_name=project.name,
            project_uuid=project.uuid.hex,
            run_uuid=run.uuid.hex,
            run_name=run.name,
            run_path=run.subpath,
            resolver_cls=resolver_cls,
            params=None,
            compiled_at=None,
            created_at=run.created_at,
            cloning_kind=run.cloning_kind,
            original_uuid=run.original.uuid.hex if run.original_id else None,
        )
    except (
        AccessNotAuthorized,
        AccessNotFound,
    ) as e:
        raise PolyaxonCompilerError("Access Error: %s" % e) from e
    except (
        AccessNotAuthorized,
        AccessNotFound,
        MarshmallowValidationError,
        PolyaxonSchemaError,
        ValidationError,
    ) as e:
        raise PolyaxonCompilerError("Compilation Error: %s" % e) from e
