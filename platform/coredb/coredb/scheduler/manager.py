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

import logging

from typing import Dict, List, Optional

from coredb.abstracts.getter import get_run_model
from coredb.abstracts.runs import BaseRun
from coredb.managers.artifacts import set_artifacts
from coredb.managers.statuses import new_run_status, new_run_stop_status
from coredb.scheduler import resolver
from polyaxon.agents import manager
from polyaxon.exceptions import PolyaxonCompilerError, PolyaxonK8SError
from polyaxon.lifecycle import LifeCycle, V1StatusCondition, V1Statuses
from polyaxon.polyboard.artifacts import V1RunArtifact
from polycommon import conf
from polycommon.options.registry.k8s import K8S_IN_CLUSTER, K8S_NAMESPACE

_logger = logging.getLogger("polyaxon.scheduler")


def get_run(run_id: int, run: BaseRun) -> Optional[BaseRun]:
    run_model = get_run_model()
    if run:
        return run

    try:
        return run_model.objects.get(id=run_id)
    except run_model.DoesNotExist:
        _logger.info(
            "Something went wrong, " "the run `%s` does not exist anymore.", run_id
        )


def runs_delete(run_id: int, run: Optional[BaseRun]):
    run = get_run(run_id=run_id, run=run)
    if not run:
        return

    runs_stop(run_id=run_id, run=run, update_status=False)
    run.delete()


def runs_prepare(run_id: int, run: Optional[BaseRun], eager: bool = False):
    run = get_run(run_id=run_id, run=run)
    if not run:
        return

    if not LifeCycle.is_compilable(run.status):
        _logger.info(
            "Run `%s` cannot transition from `%s` to `%s`.",
            run_id,
            run.status,
            V1Statuses.COMPILED,
        )
        return None

    try:
        _, compiled_operation = resolver.resolve(run=run)
    except PolyaxonCompilerError as e:
        condition = V1StatusCondition.get_condition(
            type=V1Statuses.FAILED,
            status="True",
            reason="PolyaxonRunFailed",
            message=f"Run compilation error: {e}",
        )
        new_run_status(run=run, condition=condition)
        return None

    condition = V1StatusCondition.get_condition(
        type=V1Statuses.COMPILED,
        status="True",
        reason="PolyaxonRunCompiler",
        message="Run is compiled",
    )
    new_run_status(run=run, condition=condition)

    if eager:
        runs_start(run_id=run.id, run=run)
        return


def runs_start(run_id: int, run: Optional[BaseRun]):
    run = get_run(run_id=run_id, run=run)
    if not run:
        return

    if not run.is_managed:
        return

    if not LifeCycle.is_compiled(run.status):
        _logger.info(
            "Run `%s` cannot transition from `%s` to `%s`.",
            run_id,
            run.status,
            V1Statuses.QUEUED,
        )
        return

    condition = V1StatusCondition.get_condition(
        type=V1Statuses.QUEUED,
        status="True",
        reason="PolyaxonRunQueued",
        message="Run is queued",
    )
    new_run_status(run=run, condition=condition)

    try:
        in_cluster = conf.get(K8S_IN_CLUSTER)
        if in_cluster and (run.is_service or run.is_job):
            manager.start(
                content=run.content,
                owner_name=run.project.owner.name,
                project_name=run.project.name,
                run_name=run.name,
                run_uuid=run.uuid.hex,
                run_kind=run.kind,
                namespace=conf.get(K8S_NAMESPACE),
                in_cluster=in_cluster,
            )
    except PolyaxonK8SError as e:
        condition = V1StatusCondition.get_condition(
            type=V1Statuses.FAILED,
            status="True",
            reason="PolyaxonRunFailed",
            message="Could not start the job {}".format(e),
        )
        new_run_status(run=run, condition=condition)


def runs_set_artifacts(run_id: int, run: Optional[BaseRun], artifacts: List[Dict]):
    run = get_run(run_id=run_id, run=run)
    if not run:
        return

    artifacts = [V1RunArtifact.from_dict(a) for a in artifacts]
    set_artifacts(run=run, artifacts=artifacts)


def runs_stop(
    run_id: int, run: Optional[BaseRun], update_status=False, message=None
) -> bool:
    run = get_run(run_id=run_id, run=run)
    if not run:
        return True

    stopped = True
    if run.is_managed and LifeCycle.is_k8s_stoppable(run.status):
        in_cluster = conf.get(K8S_IN_CLUSTER)
        if in_cluster and (run.is_service or run.is_job):
            stopped = manager.stop(
                run_uuid=run.uuid.hex,
                run_kind=run.kind,
                namespace=conf.get(K8S_NAMESPACE),
                in_cluster=in_cluster,
            )

    if not stopped:
        return False

    if not update_status:
        return True

    new_run_stop_status(run=run, message=message)
    return True
