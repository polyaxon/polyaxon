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

from polycommon import conf
from polycommon.celery.tasks import CoreSchedulerCeleryTasks
from polycommon.options.registry.core import SCHEDULER_ENABLED


def handle_run_created(workers_backend, event: "Event") -> None:  # noqa: F821
    """Handles creation, resume, and restart"""
    # Run is not managed by Polyaxon
    if not event.data["is_managed"]:
        return
    # Run is managed by a pipeline
    if event.data.get("pipeline_id") is not None:
        return

    if conf.get(SCHEDULER_ENABLED):
        workers_backend.send(
            CoreSchedulerCeleryTasks.RUNS_PREPARE, kwargs={"run_id": event.instance_id}
        )
        return


def handle_run_cleaned_triggered(workers_backend, event: "Event") -> None:  # noqa: F821
    # Run is not managed by Polyaxon
    if not event.data["is_managed"]:
        return

    if conf.get(SCHEDULER_ENABLED):
        workers_backend.send(
            CoreSchedulerCeleryTasks.RUNS_CLEAN, kwargs={"run_id": event.instance_id}
        )
        return


def handle_run_stopped_triggered(workers_backend, event: "Event") -> None:  # noqa: F821
    if conf.get(SCHEDULER_ENABLED):
        workers_backend.send(
            CoreSchedulerCeleryTasks.RUNS_STOP, kwargs={"run_id": event.instance_id}
        )
        return
