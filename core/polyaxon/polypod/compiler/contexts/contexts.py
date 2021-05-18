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
from typing import Dict

from polyaxon.containers import contexts
from polyaxon.contexts import keys as contexts_keys
from polyaxon.contexts import sections as contexts_sections
from polyaxon.exceptions import PolyaxonCompilerError
from polyaxon.polyflow import V1CloningKind, V1CompiledOperation, V1Plugins, V1RunKind
from polyaxon.polypod.compiler.contexts.job import JobContextsManager
from polyaxon.polypod.compiler.contexts.kubeflow import (
    MPIJobContextsManager,
    PytorchJobContextsManager,
    TfJobContextsManager,
)
from polyaxon.polypod.compiler.contexts.service import ServiceContextsManager
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1ConnectionType
from polyaxon.utils.fqn_utils import get_project_instance, get_run_instance
from polyaxon.utils.path_utils import get_path

CONTEXTS_MANAGERS = {
    V1RunKind.CLEANER: JobContextsManager,
    V1RunKind.NOTIFIER: JobContextsManager,
    V1RunKind.TUNER: JobContextsManager,
    V1RunKind.WATCHDOG: JobContextsManager,
    V1RunKind.JOB: JobContextsManager,
    V1RunKind.SERVICE: ServiceContextsManager,
    V1RunKind.MPIJOB: MPIJobContextsManager,
    V1RunKind.TFJOB: TfJobContextsManager,
    V1RunKind.PYTORCHJOB: PytorchJobContextsManager,
}


def resolve_globals_contexts(
    namespace: str,
    owner_name: str,
    project_name: str,
    project_uuid: str,
    run_uuid: str,
    run_name: str,
    run_path: str,
    iteration: int,
    created_at: datetime,
    compiled_at: datetime,
    schedule_at: datetime = None,
    started_at: datetime = None,
    finished_at: datetime = None,
    duration: int = None,
    plugins: V1Plugins = None,
    artifacts_store: V1ConnectionType = None,
    cloning_kind: V1CloningKind = None,
    original_uuid: str = None,
) -> Dict:

    resolved_contexts = {
        contexts_sections.GLOBALS: {
            contexts_keys.OWNER_NAME: owner_name,
            contexts_keys.PROJECT_NAME: project_name,
            contexts_keys.PROJECT_UNIQUE_NAME: get_project_instance(
                owner_name, project_name
            ),
            contexts_keys.PROJECT_UUID: project_uuid,
            contexts_keys.RUN_INFO: get_run_instance(
                owner_name, project_name, run_uuid
            ),
            contexts_keys.NAME: run_name,
            contexts_keys.UUID: run_uuid,
            contexts_keys.NAMESPACE: namespace,
            contexts_keys.ITERATION: iteration,
            contexts_keys.CONTEXT_PATH: contexts.CONTEXT_ROOT,
            contexts_keys.ARTIFACTS_PATH: contexts.CONTEXT_MOUNT_ARTIFACTS,
            contexts_keys.CREATED_AT: created_at,
            contexts_keys.COMPILED_AT: compiled_at,
            contexts_keys.SCHEDULE_AT: schedule_at,
            contexts_keys.STARTED_AT: started_at,
            contexts_keys.FINISHED_AT: finished_at,
            contexts_keys.DURATION: duration,
            contexts_keys.CLONING_KIND: cloning_kind,
            contexts_keys.ORIGINAL_UUID: original_uuid,
            contexts_keys.STORE_PATH: "",
        },
    }

    contexts_spec = PluginsContextsSpec.from_config(plugins)

    if contexts_spec.collect_artifacts:
        run_artifacts_path = contexts.CONTEXT_MOUNT_ARTIFACTS_FORMAT.format(run_path)
        run_outputs_path = contexts.CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT.format(run_path)
        resolved_contexts[contexts_sections.GLOBALS][
            contexts_keys.RUN_ARTIFACTS_PATH
        ] = run_artifacts_path
        resolved_contexts[contexts_sections.GLOBALS][
            contexts_keys.RUN_OUTPUTS_PATH
        ] = run_outputs_path
    elif artifacts_store:
        run_artifacts_path = get_path(artifacts_store.store_path, run_path)
        run_outputs_path = get_path(run_artifacts_path, "outputs")
        resolved_contexts[contexts_sections.GLOBALS][
            contexts_keys.RUN_ARTIFACTS_PATH
        ] = run_artifacts_path
        resolved_contexts[contexts_sections.GLOBALS][
            contexts_keys.RUN_OUTPUTS_PATH
        ] = run_outputs_path

    if contexts_spec.mount_artifacts_store and artifacts_store:
        resolved_contexts[contexts_sections.GLOBALS][
            contexts_keys.STORE_PATH
        ] = artifacts_store.store_path
    return resolved_contexts


def resolve_contexts(
    namespace: str,
    owner_name: str,
    project_name: str,
    project_uuid: str,
    run_uuid: str,
    run_name: str,
    run_path: str,
    compiled_operation: V1CompiledOperation,
    artifacts_store: V1ConnectionType,
    connection_by_names: Dict[str, V1ConnectionType],
    iteration: int,
    created_at: datetime,
    compiled_at: datetime,
    schedule_at: datetime = None,
    started_at: datetime = None,
    finished_at: datetime = None,
    duration: int = None,
    cloning_kind: V1CloningKind = None,
    original_uuid: str = None,
) -> Dict:
    run_kind = compiled_operation.get_run_kind()
    if run_kind not in CONTEXTS_MANAGERS:
        raise PolyaxonCompilerError(
            "Contexts manager Error. "
            "Specification with run kind: {} is not supported in this deployment version".format(
                run_kind
            )
        )

    resolved_contexts = resolve_globals_contexts(
        namespace=namespace,
        owner_name=owner_name,
        project_name=project_name,
        project_uuid=project_uuid,
        run_uuid=run_uuid,
        run_name=run_name,
        run_path=run_path,
        iteration=iteration,
        created_at=created_at,
        compiled_at=compiled_at,
        schedule_at=schedule_at,
        started_at=started_at,
        finished_at=finished_at,
        duration=duration,
        plugins=compiled_operation.plugins,
        artifacts_store=artifacts_store,
        cloning_kind=cloning_kind,
        original_uuid=original_uuid,
    )

    return CONTEXTS_MANAGERS[run_kind].resolve(
        namespace=namespace,
        owner_name=owner_name,
        project_name=project_name,
        run_uuid=run_uuid,
        contexts=resolved_contexts,
        compiled_operation=compiled_operation,
        connection_by_names=connection_by_names,
    )
