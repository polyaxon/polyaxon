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

from polycommon.celeryp.queues import CeleryCoreQueues
from polycommon.celeryp.tasks import CoreSchedulerCeleryTasks

SCHEDULER_CORE_ROUTES = {
    # Scheduler health
    CoreSchedulerCeleryTasks.SCHEDULER_HEALTH: {
        "queue": CeleryCoreQueues.SCHEDULER_HEALTH
    },
    # Scheduler runs
    CoreSchedulerCeleryTasks.RUNS_START: {"queue": CeleryCoreQueues.SCHEDULER_RUNS},
    CoreSchedulerCeleryTasks.RUNS_STOP: {"queue": CeleryCoreQueues.SCHEDULER_RUNS},
    CoreSchedulerCeleryTasks.RUNS_DELETE: {"queue": CeleryCoreQueues.SCHEDULER_RUNS},
    CoreSchedulerCeleryTasks.RUNS_PREPARE: {"queue": CeleryCoreQueues.SCHEDULER_RUNS},
    # Scheduler artifacts
    CoreSchedulerCeleryTasks.RUNS_SET_ARTIFACTS: {
        "queue": CeleryCoreQueues.SCHEDULER_ARTIFACTS
    },
}


def get_routes():
    routes = {}
    routes.update(SCHEDULER_CORE_ROUTES)
    return routes
