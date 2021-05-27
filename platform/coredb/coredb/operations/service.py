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

from collections import namedtuple
from typing import Dict, Optional, Set, Tuple, Union

from coredb.abstracts.getter import get_run_model
from polyaxon.constants.metadata import (
    META_HAS_DAGS,
    META_HAS_HOOKS,
    META_HAS_JOBS,
    META_HAS_MATRICES,
    META_HAS_SERVICES,
)
from polyaxon.lifecycle import V1StatusCondition, V1Statuses
from polyaxon.polyaxonfile import OperationSpecification
from polyaxon.polyflow import V1CompiledOperation, V1MatrixKind, V1Operation, V1RunKind
from polyaxon.schemas import V1RunPending
from polycommon.service_interface import Service


class OperationInitSpec(
    namedtuple(
        "OperationInitSpec",
        "compiled_operation instance related_instance",
    )
):
    def update(self, compiled_operation=None, instance=None, related_instance=None):
        compiled_operation = compiled_operation or self.compiled_operation
        instance = instance or self.instance
        related_instance = related_instance or self.related_instance
        return OperationInitSpec(compiled_operation, instance, related_instance)


class OperationsService(Service):
    SUPPORTS_OP_BUILD = False
    DEFAULT_KINDS = V1RunKind.default_runtime_values
    __all__ = ("init_run", "init_and_save_run", "resolve_build", "save_build_relation")

    @staticmethod
    def set_spec(spec: V1Operation, **kwargs) -> Tuple[V1Operation, Dict]:
        kwargs["raw_content"] = spec.to_dict(dump=True)
        return spec, kwargs

    @staticmethod
    def get_kind(compiled_operation: V1CompiledOperation) -> Tuple[str, Optional[str]]:
        if compiled_operation.is_tf_job_run:
            return V1RunKind.JOB, V1RunKind.TFJOB
        elif compiled_operation.is_pytorch_job_run:
            return V1RunKind.JOB, V1RunKind.PYTORCHJOB
        elif compiled_operation.is_mpi_job_run:
            return V1RunKind.JOB, V1RunKind.MPIJOB
        elif compiled_operation.is_dask_run:
            return V1RunKind.JOB, V1RunKind.DASK
        elif compiled_operation.is_spark_run:
            return V1RunKind.JOB, V1RunKind.SPARK
        elif compiled_operation.is_tuner_run:
            return V1RunKind.JOB, V1RunKind.TUNER
        elif compiled_operation.is_notifier_run:
            return V1RunKind.JOB, V1RunKind.NOTIFIER
        # Default case
        kind = compiled_operation.run.kind
        return kind, kind

    @classmethod
    def supports_kind(
        cls, kind: str, runtime: str, supported_kinds: Set[str], is_managed: bool
    ) -> bool:
        supported_kinds = supported_kinds or cls.DEFAULT_KINDS
        error_message = (
            "You cannot create this operation. This can happen if "
            "the current project has runtime restrictions, "
            "your account has reached the allowed quota, "
            "or your plan does not support operations of kind: {}"
        )
        if kind not in supported_kinds:
            if is_managed or kind not in V1RunKind.eager_values:
                raise ValueError(error_message.format(kind))
        if runtime and runtime not in supported_kinds:
            if is_managed or runtime not in V1MatrixKind.eager_values:
                raise ValueError(error_message.format(runtime))
        return True

    @classmethod
    def _finalize_meta_info(cls, meta_info: Dict, **kwargs):
        return meta_info

    @classmethod
    def get_meta_info(
        cls,
        compiled_operation: V1CompiledOperation,
        kind: str,
        runtime: str,
        meta_info: Dict = None,
        **kwargs,
    ) -> Tuple[str, str, Dict]:
        meta_info = meta_info or {}
        if compiled_operation.hooks:
            meta_info[META_HAS_HOOKS] = True
        if compiled_operation.schedule:
            if compiled_operation.matrix:
                meta_info[META_HAS_MATRICES] = True
            elif kind == V1RunKind.JOB:
                meta_info[META_HAS_JOBS] = True
            elif kind == V1RunKind.SERVICE:
                meta_info[META_HAS_SERVICES] = True
            elif kind == V1RunKind.DAG:
                meta_info[META_HAS_DAGS] = True
            kind = V1RunKind.SCHEDULE
            runtime = compiled_operation.schedule.kind
        elif compiled_operation.matrix:
            if kind == V1RunKind.JOB:
                meta_info[META_HAS_JOBS] = True
            elif kind == V1RunKind.SERVICE:
                meta_info[META_HAS_SERVICES] = True
            elif kind == V1RunKind.DAG:
                meta_info[META_HAS_DAGS] = True
            kind = V1RunKind.MATRIX
            runtime = compiled_operation.matrix.kind

        meta_info = cls._finalize_meta_info(meta_info=meta_info, **kwargs)
        return kind, runtime, meta_info

    @staticmethod
    def sanitize_kwargs(**kwargs):
        results = {}
        if kwargs.get("raw_content"):
            results["raw_content"] = kwargs["raw_content"]
        if kwargs.get("content"):
            results["content"] = kwargs["content"]

        return results

    def is_valid(self, compiled_operation: V1CompiledOperation):
        compiled_operation.validate_build()
        if compiled_operation.build and not self.SUPPORTS_OP_BUILD:
            raise ValueError(
                "You cannot create this operation. "
                "The build section is not supported in your plan."
            )

    def resolve_build(
        self,
        project_id: int,
        user_id: int,
        compiled_operation: V1CompiledOperation,
        inputs: Dict,
        pending: str = None,
        **kwargs,
    ):
        raise ValueError(
            "You cannot create this operation. "
            "The build section is not supported in your plan."
        )

    @staticmethod
    def save_build_relation(run_init_spec: OperationInitSpec):
        pass

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
        params: Dict = None,
        readme: str = None,
        original_id: int = None,
        cloning_kind: str = None,
        is_managed: bool = True,
        pending: str = None,
        meta_info: Dict = None,
        supported_kinds: Set[str] = None,
        **kwargs,
    ) -> OperationInitSpec:
        if op_spec:
            op_spec, kwargs = self.set_spec(op_spec, **kwargs)
        if op_spec:
            if not compiled_operation or override:
                compiled_operation = OperationSpecification.compile_operation(
                    op_spec, override=override
                )
            params = op_spec.params

        params = params or {}
        inputs = {p: pv.value for p, pv in params.items() if pv.is_literal}
        params = {p: pv.to_dict() for p, pv in params.items()}
        kind = None
        meta_info = meta_info or {}
        build_instance = None
        runtime = None
        if compiled_operation:
            self.is_valid(compiled_operation)
            # If the user is uploading we need to check the build process immediately
            if pending == V1RunPending.UPLOAD and compiled_operation.build:
                build_instance = self.resolve_build(
                    project_id=project_id,
                    user_id=user_id,
                    compiled_operation=compiled_operation,
                    inputs=inputs,
                    pending=V1RunPending.UPLOAD,
                    **kwargs,
                )
                # Change the pending logic to wait to build and remove build requirements
                compiled_operation.build = None
                pending = V1RunPending.BUILD

            if pending is None and compiled_operation.is_approved is False:
                pending = V1RunPending.APPROVAL
            name = name or compiled_operation.name
            description = description or compiled_operation.description
            tags = tags or compiled_operation.tags
            kind, runtime = self.get_kind(compiled_operation)
            kind, runtime, meta_info = self.get_meta_info(
                compiled_operation, kind, runtime, meta_info, **kwargs
            )
            self.supports_kind(kind, runtime, supported_kinds, is_managed)
            kwargs["content"] = compiled_operation.to_dict(dump=True)
        instance = get_run_model()(
            project_id=project_id,
            user_id=user_id,
            name=name,
            description=description,
            tags=tags,
            readme=readme,
            params=params,
            inputs=inputs,
            kind=kind,
            runtime=runtime,
            meta_info=meta_info,
            original_id=original_id,
            cloning_kind=cloning_kind,
            is_managed=is_managed,
            pending=pending,
            status_conditions=[
                V1StatusCondition.get_condition(
                    type=V1Statuses.CREATED,
                    status="True",
                    reason=kwargs.pop("reason", "OperationServiceInit"),
                    message=kwargs.pop("message", "Run is created"),
                ).to_dict()
            ],
            **self.sanitize_kwargs(**kwargs),
        )
        return OperationInitSpec(compiled_operation, instance, build_instance)

    def init_and_save_run(
        self,
        project_id: int,
        user_id: int,
        op_spec: V1Operation = None,
        compiled_operation: V1CompiledOperation = None,
        name: str = None,
        description: str = None,
        tags: str = None,
        override: Union[str, Dict] = None,
        params: Dict = None,
        readme: str = None,
        is_managed: bool = True,
        pending: str = None,
        meta_info: Dict = None,
        pipeline_id: int = None,
        controller_id: int = None,
        supported_kinds: Set[str] = None,
        supported_owners: Set[str] = None,
    ):
        run_init_spec = self.init_run(
            project_id=project_id,
            user_id=user_id,
            name=name,
            description=description,
            op_spec=op_spec,
            compiled_operation=compiled_operation,
            override=override,
            params=params,
            readme=readme,
            pipeline_id=pipeline_id,
            controller_id=controller_id,
            tags=tags,
            is_managed=is_managed,
            pending=pending,
            meta_info=meta_info,
            supported_kinds=supported_kinds,
            supported_owners=supported_owners,
        )
        run_init_spec.instance.save()
        if run_init_spec.related_instance:
            self.save_build_relation(run_init_spec)
        return run_init_spec.instance
