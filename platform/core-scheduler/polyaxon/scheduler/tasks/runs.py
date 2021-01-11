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

import logging

from typing import Dict, List

from coredb.scheduler import manager
from polycommon import workers
from polycommon.celeryp.tasks import CoreSchedulerCeleryTasks
from polyconf.settings import Intervals

_logger = logging.getLogger("polyaxon.scheduler")


@workers.app.task(name=CoreSchedulerCeleryTasks.RUNS_PREPARE, ignore_result=True)
def runs_prepare(run_id):
    if manager.runs_prepare(run_id=run_id, run=None):
        workers.send(CoreSchedulerCeleryTasks.RUNS_START, kwargs={"run_id": run_id})


@workers.app.task(name=CoreSchedulerCeleryTasks.RUNS_START, ignore_result=True)
def runs_start(run_id):
    manager.runs_start(run_id=run_id, run=None)


@workers.app.task(name=CoreSchedulerCeleryTasks.RUNS_SET_ARTIFACTS, ignore_result=True)
def runs_set_artifacts(run_id, artifacts: List[Dict]):
    manager.runs_set_artifacts(run_id=run_id, run=None, artifacts=artifacts)


@workers.app.task(
    name=CoreSchedulerCeleryTasks.RUNS_STOP,
    bind=True,
    max_retries=3,
    ignore_result=True,
)
def runs_stop(self, run_id, update_status=False, message=None):
    stopped = manager.runs_stop(
        run_id=run_id, run=None, update_status=update_status, message=message
    )
    if not stopped and self.request.retries < 2:
        _logger.info("Trying again to delete job `%s` in run.", run_id)
        self.retry(countdown=Intervals.RUNS_SCHEDULER)
        return


@workers.app.task(name=CoreSchedulerCeleryTasks.RUNS_DELETE, ignore_result=True)
def runs_delete(run_id):
    manager.runs_delete(run_id=run_id, run=None)
