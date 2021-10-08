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

from django.test import TestCase

from coredb.factories.projects import ProjectFactory
from coredb.factories.runs import RunFactory
from coredb.factories.users import UserFactory
from coredb.managers.statuses import new_run_status
from polyaxon.lifecycle import V1StatusCondition, V1Statuses


class TestStatuses(TestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.project = ProjectFactory()
        self.run = RunFactory(project=self.project, user=self.user)

    def test_new_failed_status_after_stopping(self):
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.STOPPING, status=True, reason="foo"
            ),
        )
        self.run.refresh_from_db()
        assert len(self.run.status_conditions) == 1

        # Same this condition
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.SCHEDULED, status=True, reason="foo"
            ),
        )
        self.run.refresh_from_db()
        assert len(self.run.status_conditions) == 1

        # Different condition's message
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.FAILED, status=True, reason="foo", message="New message"
            ),
        )
        self.run.refresh_from_db()
        assert len(self.run.status_conditions) == 2

    def test_new_stopped_status_after_stopping(self):
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.STOPPING, status=True, reason="foo"
            ),
        )
        self.run.refresh_from_db()
        assert len(self.run.status_conditions) == 1

        # Same this condition
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.RUNNING, status=True, reason="foo"
            ),
        )
        self.run.refresh_from_db()
        assert len(self.run.status_conditions) == 1

        # Different condition's message
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.STOPPED,
                status=True,
                reason="foo",
                message="New message",
            ),
        )
        self.run.refresh_from_db()
        assert len(self.run.status_conditions) == 2

    def test_new_status_equality(self):
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.SCHEDULED, status=True, reason="foo"
            ),
        )
        self.run.refresh_from_db()
        assert len(self.run.status_conditions) == 1

        # Same condition
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.SCHEDULED, status=True, reason="foo"
            ),
        )
        self.run.refresh_from_db()
        assert len(self.run.status_conditions) == 1

        # Different condition's message
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.SCHEDULED,
                status=True,
                reason="foo",
                message="New message",
            ),
        )
        self.run.refresh_from_db()
        assert len(self.run.status_conditions) == 1

        # New condition
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.RUNNING,
                status=True,
                reason="foo",
                message="New message",
            ),
        )
        self.run.refresh_from_db()
        assert len(self.run.status_conditions) == 2

    def test_status_transition(self):
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.SCHEDULED, status=True, reason="foo"
            ),
        )
        self.run.refresh_from_db()
        assert len(self.run.status_conditions) == 1

        # New running condition
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.RUNNING,
                status=True,
                reason="foo",
                message="New message",
            ),
        )
        self.run.refresh_from_db()
        assert len(self.run.status_conditions) == 2

        # New warning condition
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.WARNING,
                status=True,
                reason="foo",
                message="New message",
            ),
        )
        self.run.refresh_from_db()
        assert len(self.run.status_conditions) == 3

        # New running condition
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.RUNNING,
                status=True,
                reason="foo",
                message="New message",
            ),
        )
        self.run.refresh_from_db()
        assert len(self.run.status_conditions) == 4

        # New warning condition
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.WARNING,
                status=True,
                reason="foo",
                message="New message",
            ),
        )
        self.run.refresh_from_db()
        assert len(self.run.status_conditions) == 5

    def test_new_status_set_start_date(self):
        # No status change
        assert self.run.started_at is None
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.CREATED, status=True
            ),
        )
        assert self.run.started_at is None
        assert self.run.finished_at is None
        assert self.run.wait_time is None
        assert self.run.duration is None

        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.COMPILED, status=True
            ),
        )
        self.run.refresh_from_db()
        assert self.run.started_at is None
        assert self.run.finished_at is None
        assert self.run.wait_time is None
        assert self.run.duration is None

        # Set a running status
        self.run.status = V1Statuses.CREATED
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.STARTING, status=True
            ),
        )
        self.run.refresh_from_db()
        assert self.run.started_at is not None
        assert self.run.finished_at is None
        assert self.run.wait_time == int(
            (self.run.started_at - self.run.created_at).total_seconds()
        )
        assert self.run.duration is None
        started_at = self.run.started_at

        self.run.status = V1Statuses.CREATED
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.RUNNING, status=True
            ),
        )
        assert self.run.started_at == started_at
        assert self.run.finished_at is None
        assert self.run.wait_time == int(
            (self.run.started_at - self.run.created_at).total_seconds()
        )
        assert self.run.duration is None
        assert len(self.run.status_conditions) == 3

        condition1 = V1StatusCondition.get_condition(
            type=V1Statuses.STOPPED,
            status="True",
            reason="Run is stopped",
            message="zombie error",
        )
        new_run_status(self.run, condition1)
        self.run.refresh_from_db()
        assert self.run.started_at == started_at
        assert self.run.finished_at is not None
        finished_at = self.run.finished_at
        assert self.run.wait_time == int(
            (self.run.started_at - self.run.created_at).total_seconds()
        )
        assert self.run.duration == int(
            (self.run.finished_at - self.run.started_at).total_seconds()
        )
        assert len(self.run.status_conditions) == 4
        assert self.run.status_conditions[3]["type"] == V1Statuses.STOPPED
        assert self.run.status_conditions[3]["message"] == "zombie error"
        assert self.run.status_conditions[3]["reason"] == "Run is stopped"

        condition2 = V1StatusCondition.get_condition(
            type=V1Statuses.FAILED,
            status="True",
            reason="Run failed",
            message="some error",
        )
        new_run_status(self.run, condition2)
        self.run.refresh_from_db()
        assert self.run.started_at == started_at
        assert self.run.finished_at is not None
        finished_at = self.run.finished_at
        assert self.run.wait_time == int(
            (self.run.started_at - self.run.created_at).total_seconds()
        )
        assert self.run.duration == int(
            (self.run.finished_at - self.run.started_at).total_seconds()
        )
        assert len(self.run.status_conditions) == 4
        assert self.run.status_conditions[3]["type"] == V1Statuses.STOPPED
        assert self.run.status_conditions[3]["message"] == "zombie error"
        assert self.run.status_conditions[3]["reason"] == "Run is stopped"

        # Set force
        new_run_status(self.run, condition2, force=True)
        self.run.refresh_from_db()
        assert self.run.started_at == started_at
        assert self.run.finished_at == finished_at
        assert self.run.wait_time == int(
            (self.run.started_at - self.run.created_at).total_seconds()
        )
        assert self.run.duration == int(
            (self.run.finished_at - self.run.started_at).total_seconds()
        )
        assert len(self.run.status_conditions) == 5
        assert self.run.status_conditions[3]["type"] == V1Statuses.STOPPED
        assert self.run.status_conditions[4]["type"] == V1Statuses.FAILED

        # Update the stopped status force
        condition3 = V1StatusCondition.get_condition(
            type=V1Statuses.STOPPED,
            status="True",
            reason="Run failed",
            message="some error",
        )
        new_run_status(self.run, condition3, force=True)
        self.run.refresh_from_db()
        assert self.run.started_at == started_at
        assert self.run.finished_at == finished_at
        assert self.run.wait_time == int(
            (self.run.started_at - self.run.created_at).total_seconds()
        )
        assert self.run.duration == int(
            (self.run.finished_at - self.run.started_at).total_seconds()
        )
        assert len(self.run.status_conditions) == 6
        assert self.run.status_conditions[3]["type"] == V1Statuses.STOPPED
        assert self.run.status_conditions[4]["type"] == V1Statuses.FAILED
        assert self.run.status_conditions[5]["type"] == V1Statuses.STOPPED
        assert self.run.status_conditions[5]["message"] == "some error"
        assert self.run.status_conditions[5]["reason"] == "Run failed"
