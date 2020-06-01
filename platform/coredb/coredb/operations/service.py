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

from typing import Dict, Optional, Tuple, Union

from coredb.models.runs import Run
from polyaxon.lifecycle import V1StatusCondition, V1Statuses
from polyaxon.polyaxonfile import OperationSpecification
from polyaxon.polyflow import V1CompiledOperation, V1Operation, V1RunKind
from polycommon.service_interface import Service


class OperationsService(Service):
    __all__ = ("init_run",)

    @staticmethod
    def set_spec(spec: V1Operation) -> V1Operation:
        return spec

    @staticmethod
    def get_kind(compiled_operation: V1CompiledOperation) -> Tuple[str, Optional[str]]:
        if compiled_operation.is_job_run:
            return V1RunKind.JOB, V1RunKind.JOB
        elif compiled_operation.is_tf_job_run:
            return V1RunKind.JOB, V1RunKind.TFJOB
        elif compiled_operation.is_pytorch_job_run:
            return V1RunKind.JOB, V1RunKind.PYTORCHJOB
        elif compiled_operation.is_mpi_job_run:
            return V1RunKind.JOB, V1RunKind.MPIJOB
        elif compiled_operation.is_dask_run:
            return V1RunKind.JOB, V1RunKind.DASK
        elif compiled_operation.is_spark_run:
            return V1RunKind.JOB, V1RunKind.SPARK
        else:
            return compiled_operation.run.kind, None

    @staticmethod
    def get_meta_info(
        compiled_operation: V1CompiledOperation, kind: str, meta_kind: str
    ) -> Tuple[str, Dict]:
        return kind, {"meta_kind": meta_kind}

    def init_run(
        self,
        project_id: int,
        user_id: int,
        op_spec: V1Operation = None,
        compiled_operation: V1CompiledOperation = None,
        name: str = None,
        description: str = None,
        tags: str = None,
        override: Union[str, Dict] = None,
        override_post: bool = True,
        params: Dict = None,
        readme: str = None,
        pipeline_id: int = None,
        controller_id: int = None,
        original_id: int = None,
        cloning_kind: str = None,
    ) -> Tuple[V1CompiledOperation, Run]:
        content = None
        raw_content = None
        if op_spec:
            op_spec = self.set_spec(op_spec)
            raw_content = op_spec.to_dict(dump=True)
        if op_spec:
            if not compiled_operation or override:
                compiled_operation = OperationSpecification.compile_operation(
                    op_spec, override=override, override_post=override_post
                )
            params = op_spec.params

        params = params or {}
        inputs = {p: pv.value for p, pv in params.items() if pv.is_literal}
        params = {p: pv.to_dict() for p, pv in params.items()}
        kind = None
        meta_info = {}
        if compiled_operation:
            content = compiled_operation.to_dict(dump=True)
            name = name or compiled_operation.name
            description = description or compiled_operation.description
            tags = tags or compiled_operation.tags
            kind, meta_kind = self.get_kind(compiled_operation)
            kind, meta_info = self.get_meta_info(compiled_operation, kind, meta_kind)
        instance = Run(
            project_id=project_id,
            user_id=user_id,
            name=name,
            description=description,
            tags=tags,
            readme=readme,
            raw_content=raw_content,
            content=content,
            params=params,
            inputs=inputs,
            pipeline_id=pipeline_id,
            kind=kind,
            meta_info=meta_info,
            controller_id=controller_id,
            original_id=original_id,
            cloning_kind=cloning_kind,
            status_conditions=[
                V1StatusCondition.get_condition(
                    type=V1Statuses.CREATED,
                    status="True",
                    reason="PolyaxonRunCreated",
                    message="Run is created",
                ).to_dict()
            ],
        )
        return compiled_operation, instance
