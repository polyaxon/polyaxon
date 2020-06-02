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
from polyaxon.lifecycle import V1Statuses
from scheduler.tasks.runs import runs_stop
from tests.base.case import BaseTest


class TestRunsStop(BaseTest):
    @mock.patch("coredb.scheduler.manager.runs_stop")
    @mock.patch("coredb.scheduler.manager.runs_prepare")
    def test_stop_managed_run(self, runs_prepare, managed_stop):
        managed_stop.return_value = True
        experiment = RunFactory(
            project=self.project, user=self.user, is_managed=True, raw_content="test"
        )
        assert runs_prepare.call_count == 1
        experiment.refresh_from_db()
        assert experiment.status == V1Statuses.CREATED
        runs_stop(run_id=experiment.id, update_status=True)
        assert managed_stop.call_count == 1

    def test_stop_non_managed_run(self):
        experiment = RunFactory(project=self.project, user=self.user, is_managed=False)
        runs_stop(run_id=experiment.id, update_status=True)
        experiment.refresh_from_db()
        assert experiment.status == V1Statuses.STOPPED

    @mock.patch("scheduler.tasks.runs_stop.retry")
    @mock.patch("coredb.scheduler.manager.runs_stop")
    @mock.patch("coredb.scheduler.resolver.resolve")
    def test_stop_managed_wrong_stop_retries(
        self, mock_resolve, managed_stop, mock_stop_run
    ):
        managed_stop.return_value = False
        experiment = RunFactory(
            project=self.project, user=self.user, is_managed=True, raw_content="test"
        )
        runs_stop(run_id=experiment.id)
        assert mock_stop_run.call_count == 1
        assert managed_stop.call_count == 1
        experiment.refresh_from_db()
        assert experiment.status == V1Statuses.CREATED
