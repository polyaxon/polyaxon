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

from coredb.scheduler import manager
from polycommon import conf
from polycommon.celeryp.tasks import CoreSchedulerCeleryTasks
from polycommon.options.registry.core import SCHEDULER_ENABLED


def handle_run_created(workers_backend, event: "Event") -> None:  # noqa: F821
    """Handles creation, resume, and restart"""
    eager = False
    if event.instance and (event.instance.meta_info or {}).get("eager"):
        eager = True
    if not eager:
        eager = (
            not event.data["is_managed"] and event.instance and event.instance.content
        )
    # Run is not managed by Polyaxon
    if not event.data["is_managed"] and not eager:
        return
    # Run is managed by a pipeline
    if event.data.get("pipeline_id") is not None:
        return

    if conf.get(SCHEDULER_ENABLED) and not eager:
        workers_backend.send(
            CoreSchedulerCeleryTasks.RUNS_PREPARE, kwargs={"run_id": event.instance_id}
        )
        return

    # Eager mode
    manager.runs_prepare(run_id=event.instance_id, run=event.instance, eager=True)


def handle_run_approved_triggered(
    workers_backend, event: "Event"
) -> None:  # noqa: F821
    run = manager.get_run(run_id=event.instance_id, run=event.instance)
    if not run:
        return

    if run.is_managed and conf.get(SCHEDULER_ENABLED):
        workers_backend.send(
            CoreSchedulerCeleryTasks.RUNS_START, kwargs={"run_id": event.instance_id}
        )
        return

    manager.runs_start(run_id=event.instance_id, run=event.instance)


def handle_run_stopped_triggered(workers_backend, event: "Event") -> None:  # noqa: F821
    run = manager.get_run(run_id=event.instance_id, run=event.instance)
    if not run:
        return

    if run.is_managed and conf.get(SCHEDULER_ENABLED):
        workers_backend.send(
            CoreSchedulerCeleryTasks.RUNS_STOP, kwargs={"run_id": event.instance_id}
        )
        return

    manager.runs_stop(run_id=event.instance_id, run=event.instance)


def handle_new_artifacts(workers_backend, event: "Event") -> None:  # noqa: F821
    artifacts = event.data.get("artifacts")
    if not artifacts:
        return

    if conf.get(SCHEDULER_ENABLED):
        workers_backend.send(
            CoreSchedulerCeleryTasks.RUNS_SET_ARTIFACTS,
            kwargs={"run_id": event.instance_id, "artifacts": artifacts},
        )
        return

    manager.runs_set_artifacts(
        run_id=event.instance_id, run=event.instance, artifacts=artifacts
    )


def handle_run_deleted(workers_backend, event: "Event") -> None:  # noqa: F821
    if conf.get(SCHEDULER_ENABLED):
        workers_backend.send(
            CoreSchedulerCeleryTasks.RUNS_DELETE, kwargs={"run_id": event.instance_id}
        )
        return

    manager.runs_delete(run_id=event.instance_id, run=event.instance)
