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

from unittest.mock import patch

from django.test import TestCase

from coredb.factories.projects import ProjectFactory
from coredb.factories.runs import RunFactory
from coredb.factories.users import UserFactory
from coredb.managers.statuses import new_run_status
from polyaxon.lifecycle import V1StatusCondition, V1Statuses
from polycommon.events.registry import run as run_events


class TestRunStatusManager(TestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.project = ProjectFactory()
        self.run = RunFactory(project=self.project)

    @patch("polycommon.auditor.record")
    def test_new_run_status_created(self, auditor_record):
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.CREATED, status=True
            ),
        )
        assert auditor_record.call_count == 0

    @patch("polycommon.auditor.record")
    def test_new_run_status_scheduled(self, auditor_record):
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.SCHEDULED, status=True
            ),
        )
        assert auditor_record.call_count == 1
        call_args, call_kwargs = auditor_record.call_args
        assert call_args == ()
        assert call_kwargs["event_type"] == run_events.RUN_NEW_STATUS

    @patch("polycommon.auditor.record")
    def test_new_run_status_stopped(self, auditor_record):
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.STOPPED, status=True
            ),
        )
        assert auditor_record.call_count == 3
        call_args_list = auditor_record.call_args_list
        assert call_args_list[0][0] == ()
        assert call_args_list[1][0] == ()
        assert call_args_list[2][0] == ()
        assert call_args_list[0][1]["event_type"] == run_events.RUN_NEW_STATUS
        assert call_args_list[1][1]["event_type"] == run_events.RUN_STOPPED
        assert call_args_list[2][1]["event_type"] == run_events.RUN_DONE

    @patch("polycommon.auditor.record")
    def test_new_run_status_failed(self, auditor_record):
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.FAILED, status=True
            ),
        )
        assert auditor_record.call_count == 3
        call_args_list = auditor_record.call_args_list
        assert call_args_list[0][0] == ()
        assert call_args_list[1][0] == ()
        assert call_args_list[2][0] == ()
        assert call_args_list[0][1]["event_type"] == run_events.RUN_NEW_STATUS
        assert call_args_list[1][1]["event_type"] == run_events.RUN_FAILED
        assert call_args_list[2][1]["event_type"] == run_events.RUN_DONE

    @patch("polycommon.auditor.record")
    def test_new_run_status_succeeded(self, auditor_record):
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.SUCCEEDED, status=True
            ),
        )
        assert auditor_record.call_count == 3
        call_args_list = auditor_record.call_args_list
        assert call_args_list[0][0] == ()
        assert call_args_list[1][0] == ()
        assert call_args_list[2][0] == ()
        assert call_args_list[0][1]["event_type"] == run_events.RUN_NEW_STATUS
        assert call_args_list[1][1]["event_type"] == run_events.RUN_SUCCEEDED
        assert call_args_list[2][1]["event_type"] == run_events.RUN_DONE

    @patch("polycommon.auditor.record")
    def test_new_run_status_skipped(self, auditor_record):
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.SKIPPED, status=True
            ),
        )
        assert auditor_record.call_count == 3
        call_args_list = auditor_record.call_args_list
        assert call_args_list[0][0] == ()
        assert call_args_list[1][0] == ()
        assert call_args_list[2][0] == ()
        assert call_args_list[0][1]["event_type"] == run_events.RUN_NEW_STATUS
        assert call_args_list[1][1]["event_type"] == run_events.RUN_SKIPPED
        assert call_args_list[2][1]["event_type"] == run_events.RUN_DONE
