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

from mock import mock

from coredb.factories.runs import RunFactory
from coredb.managers.statuses import new_run_status
from polyaxon.lifecycle import V1StatusCondition, V1Statuses
from scheduler.tasks.runs import runs_start
from tests.base.case import BaseTest


class TestRunsStart(BaseTest):
    @mock.patch("polyaxon.agents.manager.start")
    def test_start_run_not_queued(self, manager_start):
        experiment = RunFactory(project=self.project, user=self.user)
        runs_start(run_id=experiment.id)
        assert manager_start.call_count == 0
        new_run_status(
            run=experiment,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.RUNNING, status=True
            ),
        )
        runs_start(run_id=experiment.id)
        assert manager_start.call_count == 0

    @mock.patch("coredb.scheduler.manager.runs_start")
    def test_start_run(self, manager_start):
        experiment = RunFactory(project=self.project, user=self.user)
        new_run_status(
            run=experiment,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.COMPILED, status=True
            ),
        )
        runs_start(run_id=experiment.id)
        assert manager_start.call_count == 1
