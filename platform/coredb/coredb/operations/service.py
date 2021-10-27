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
from typing import Dict, List, Optional, Set, Tuple, Union

from coredb.abstracts.getter import get_run_model
from coredb.abstracts.runs import BaseRun
from coredb.managers.statuses import new_run_status
from polyaxon.constants.metadata import (
    META_COPY_ARTIFACTS,
    META_DESTINATION_IMAGE,
    META_HAS_DAGS,
    META_HAS_HOOKS,
    META_HAS_JOBS,
    META_HAS_MATRICES,
    META_HAS_SERVICES,
    META_UPLOAD_ARTIFACTS,
)
from polyaxon.lifecycle import V1StatusCondition, V1Statuses
from polyaxon.polyaxonfile import OperationSpecification
from polyaxon.polyflow import (
    V1CloningKind,
    V1CompiledOperation,
    V1MatrixKind,
    V1Operation,
    V1RunKind,
)
from polyaxon.schemas import V1RunPending
from polyaxon.schemas.types import V1ArtifactsType
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
    __all__ = (
        "init_run",
        "init_and_save_run",
        "resolve_build",
        "save_build_relation",
        "resume_run",
        "restart_run",
        "copy_run",
    )

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
        meta_info: Dict = None,
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
        use_override_patch_strategy: bool = False,
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
                    op_spec,
                    override=override,
                    use_override_patch_strategy=use_override_patch_strategy,
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
            # If the is ab upload we need to check the build process immediately
            if pending == V1RunPending.UPLOAD and compiled_operation.build:
                upload_artifacts = meta_info.pop(META_UPLOAD_ARTIFACTS, None)
                build_instance = self.resolve_build(
                    project_id=project_id,
                    user_id=user_id,
                    compiled_operation=compiled_operation,
                    inputs=inputs,
                    meta_info={META_UPLOAD_ARTIFACTS: upload_artifacts}
                    if upload_artifacts
                    else None,
                    pending=V1RunPending.UPLOAD,
                    **kwargs,
                )
                # Change the pending logic to wait to build and remove build requirements
                compiled_operation.build = None
                pending = V1RunPending.BUILD
            # If the is a clone/resume we need to check the build process and remove it
            if cloning_kind and compiled_operation.build:
                compiled_operation.build = None

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

    def resume_run(
        self,
        run: BaseRun,
        user_id: int = None,
        name: str = None,
        description: str = None,
        content: str = None,
        readme: str = None,
        tags: List[str] = None,
        supported_kinds: Set[str] = None,
        message=None,
        **kwargs,
    ):
        op_spec = V1Operation.read(run.raw_content)
        instance = self.init_run(
            project_id=run.project_id,
            user_id=user_id or run.user_id,
            name=name or run.name,
            description=description or run.description,
            readme=readme or run.readme,
            op_spec=op_spec,
            tags=tags or run.tags,
            override=content,
            supported_kinds=supported_kinds,
            cloning_kind=V1CloningKind.RESTART,  # To clean the build if any
            use_override_patch_strategy=True,
            **kwargs,
        ).instance

        run.user_id = instance.user_id
        run.name = instance.name
        run.description = instance.description
        run.readme = instance.readme
        run.content = instance.content
        run.raw_content = instance.raw_content
        run.tags = instance.tags
        run.save()
        new_run_status(
            run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.RESUMING,
                status=True,
                reason="ResumeManager",
                message=message,
            ),
            force=True,
        )
        return run

    def _clone_build(self, original_run: BaseRun, run: BaseRun):
        pass

    def _clone_run(
        self,
        run: BaseRun,
        cloning_kind: str,
        user_id: int = None,
        name: str = None,
        description: str = None,
        content: str = None,
        readme: str = None,
        tags: List[int] = None,
        supported_kinds: Set[str] = None,
        supported_owners: Set[str] = None,
        **kwargs,
    ) -> BaseRun:
        op_spec = V1Operation.read(run.raw_content)
        meta_info = kwargs.pop("meta_info", {}) or {}
        original_meta_info = run.meta_info or {}
        original_uuid = run.uuid.hex
        upload_artifacts = original_meta_info.get(META_UPLOAD_ARTIFACTS)
        build_destination = original_meta_info.get(META_DESTINATION_IMAGE)
        if build_destination:
            meta_info[META_DESTINATION_IMAGE] = build_destination
        if upload_artifacts:
            meta_info[META_UPLOAD_ARTIFACTS] = upload_artifacts
        if cloning_kind == V1CloningKind.COPY and META_COPY_ARTIFACTS not in meta_info:
            # Handle default copy mode
            meta_info[META_COPY_ARTIFACTS] = V1ArtifactsType(
                dirs=[original_uuid]
            ).to_dict()
        if META_COPY_ARTIFACTS not in meta_info and upload_artifacts:
            # Handle default copy mode
            meta_info[META_COPY_ARTIFACTS] = V1ArtifactsType(
                dirs=["{}/{}".format(original_uuid, upload_artifacts)]
            ).to_dict()

        instance = self.init_run(
            project_id=run.project_id,
            user_id=user_id or run.user_id,
            name=name or run.name,
            description=description or run.description,
            readme=readme or run.readme,
            op_spec=op_spec,
            original_id=run.id,
            cloning_kind=cloning_kind,
            tags=tags or run.tags,
            override=content,
            supported_kinds=supported_kinds,
            supported_owners=supported_owners,
            meta_info=meta_info,
            use_override_patch_strategy=True,
            **kwargs,
        ).instance
        instance.save()
        if build_destination:
            self._clone_build(original_run=run, run=instance)
        return instance

    def restart_run(
        self,
        run: BaseRun,
        user_id: int = None,
        name: str = None,
        description: str = None,
        content: str = None,
        readme: str = None,
        tags: List[int] = None,
        supported_kinds: Set[str] = None,
        supported_owners: Set[str] = None,
        **kwargs,
    ) -> BaseRun:
        return self._clone_run(
            run=run,
            cloning_kind=V1CloningKind.RESTART,
            user_id=user_id,
            name=name,
            description=description,
            content=content,
            readme=readme,
            tags=tags,
            supported_kinds=supported_kinds,
            supported_owners=supported_owners,
            **kwargs,
        )

    def copy_run(
        self,
        run: BaseRun,
        user_id: int = None,
        name: str = None,
        description: str = None,
        content: str = None,
        readme: str = None,
        tags: List[int] = None,
        supported_kinds: Set[str] = None,
        supported_owners: Set[str] = None,
        **kwargs,
    ) -> BaseRun:
        return self._clone_run(
            run=run,
            cloning_kind=V1CloningKind.COPY,
            user_id=user_id,
            name=name,
            description=description,
            content=content,
            readme=readme,
            tags=tags,
            supported_kinds=supported_kinds,
            supported_owners=supported_owners,
            **kwargs,
        )
