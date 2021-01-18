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

from mock import MagicMock, mock, patch

from coredb.factories.runs import RunFactory
from coredb.managers.statuses import new_run_status
from polyaxon.lifecycle import V1StatusCondition, V1Statuses
from polyaxon.polyflow import V1Cache
from scheduler.tasks.runs import runs_prepare
from tests.base.case import BaseTest


class TestRunsPrepare(BaseTest):
    def setUp(self):
        super().setUp()
        patcher = patch("coredb.scheduler.manager.runs_start")
        patcher.start()
        self.addCleanup(patcher.stop)

        patcher = patch("coredb.scheduler.manager.runs_stop")
        patcher.start()
        self.addCleanup(patcher.stop)

    @mock.patch("coredb.scheduler.resolver.resolve")
    def test_prepare_run_of_already_queued_run(self, mock_resolve):
        spec_run = MagicMock(cache=None)
        mock_resolve.return_value = (None, spec_run)

        experiment = RunFactory(project=self.project, user=self.user)
        new_run_status(
            run=experiment,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.QUEUED, status=True
            ),
        )

        new_experiment = RunFactory(project=self.project, user=self.user)
        runs_prepare(run_id=new_experiment.id)

        new_experiment.refresh_from_db()
        assert new_experiment.status == V1Statuses.COMPILED

    @mock.patch("coredb.scheduler.resolver.resolve")
    def test_prepare_run_of_already_stopped_run(self, mock_resolve):
        spec_run = MagicMock(cache=V1Cache(disable=False))
        mock_resolve.return_value = (None, spec_run)

        experiment = RunFactory(project=self.project, user=self.user)
        new_run_status(
            run=experiment,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.STOPPED, status=True
            ),
        )

        new_experiment = RunFactory(project=self.project, user=self.user)
        runs_prepare(run_id=new_experiment.id)

        new_experiment.refresh_from_db()
        assert new_experiment.status == V1Statuses.COMPILED

    @mock.patch("coredb.scheduler.resolver.resolve")
    def test_prepare_run_of_already_stopping_run(self, mock_resolve):
        spec_run = MagicMock(cache=V1Cache(disable=False))
        mock_resolve.return_value = (None, spec_run)

        experiment = RunFactory(project=self.project, user=self.user)
        new_run_status(
            run=experiment,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.STOPPING, status=True
            ),
        )

        new_experiment = RunFactory(project=self.project, user=self.user)
        runs_prepare(run_id=new_experiment.id)

        new_experiment.refresh_from_db()
        assert new_experiment.status == V1Statuses.COMPILED

    @mock.patch("coredb.scheduler.resolver.resolve")
    def test_prepare_run_of_already_skipped_run(self, mock_resolve):
        spec_run = MagicMock(cache=V1Cache(disable=False))
        mock_resolve.return_value = (None, spec_run)

        experiment = RunFactory(project=self.project, user=self.user)
        new_run_status(
            run=experiment,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.SKIPPED, status=True
            ),
        )

        new_experiment = RunFactory(project=self.project, user=self.user)
        runs_prepare(run_id=new_experiment.id)

        new_experiment.refresh_from_db()
        assert new_experiment.status == V1Statuses.COMPILED

    @mock.patch("coredb.scheduler.resolver.resolve")
    def test_prepare_run_of_already_failed_run(self, mock_resolve):
        spec_run = MagicMock(cache=V1Cache(disable=False))
        mock_resolve.return_value = (None, spec_run)

        experiment = RunFactory(project=self.project, user=self.user)
        new_run_status(
            run=experiment,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.FAILED, status=True
            ),
        )

        new_experiment = RunFactory(project=self.project, user=self.user)
        runs_prepare(run_id=new_experiment.id)

        new_experiment.refresh_from_db()
        assert new_experiment.status == V1Statuses.COMPILED

    @mock.patch("scheduler.tasks.runs_start.apply_async")
    @mock.patch("scheduler.tasks.runs_prepare.apply_async")
    @mock.patch("coredb.scheduler.resolver.resolve")
    def test_prepare_run_of_already_failed_run_mock(
        self, mock_resolve, mock_prepare_run, mock_start_run
    ):
        with mock.patch("django.db.transaction.on_commit", lambda t: t()):
            spec_run = MagicMock(cache=V1Cache(disable=True))
            mock_resolve.return_value = (None, spec_run)
            experiment = RunFactory(
                project=self.project, user=self.user, raw_content="test", is_managed=True
            )
            # We are patching the automatic call and executing prepare manually
            runs_prepare(run_id=experiment.id)
            experiment.refresh_from_db()
            assert experiment.status == V1Statuses.COMPILED
            assert mock_prepare_run.call_count == 1  # Automatic call from executor
            assert mock_start_run.call_count == 1
