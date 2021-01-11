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

from rest_framework.exceptions import ValidationError

from django.test import TestCase

from coredb.factories.projects import ProjectFactory
from coredb.factories.runs import RunFactory
from coredb.factories.users import UserFactory
from coredb.managers.deleted import ArchivedManager, LiveManager
from coredb.managers.duration import set_finished_at, set_started_at
from coredb.managers.statuses import new_run_status
from coredb.models.runs import Run
from polyaxon.lifecycle import V1StatusCondition, V1Statuses


class TestRunModel(TestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.project = ProjectFactory()
        self.run = RunFactory(project=self.project)

    def test_create_run_with_no_spec_or_params(self):
        assert self.run.tags is None
        assert self.run.inputs is None
        assert self.run.outputs is None

    def test_create_run_with_no_spec_and_params(self):
        run = RunFactory(project=self.project, content=None)
        assert run.content is None

    def test_create_run_without_content_passes(self):
        run = RunFactory(project=self.project)
        assert run.content is None
        assert run.is_managed is False

    def test_create_run_without_content_and_managed_raises(self):
        with self.assertRaises(ValidationError):
            RunFactory(project=self.project, is_managed=True)

    def test_create_run_with_content_and_is_managed(self):
        with self.assertRaises(ValidationError):
            RunFactory(project=self.project, is_managed=True, content="foo")

        RunFactory(project=self.project, is_managed=True, raw_content="foo")

    def test_creation_with_bad_config(self):
        run = RunFactory(project=self.project, content="foo")
        assert run.status == V1Statuses.CREATED
        assert run.content == "foo"

    def test_status_update_results_in_new_updated_at_datetime(self):
        updated_at = self.run.updated_at
        # Create new status
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.STARTING, status=True
            ),
        )
        assert updated_at < self.run.updated_at
        updated_at = self.run.updated_at

        # Create new status
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.STARTING, status=True
            ),
        )
        assert updated_at < self.run.updated_at

    def test_managers(self):
        assert isinstance(Run.objects, LiveManager)
        assert isinstance(Run.archived, ArchivedManager)

    def test_start_at(self):
        assert self.run.started_at is None
        set_started_at(self.run)
        assert self.run.started_at is None

        self.run.status = V1Statuses.STARTING
        set_started_at(self.run)
        assert self.run.started_at is not None

        started_at = self.run.started_at
        self.run.status = V1Statuses.RUNNING
        assert self.run.started_at == started_at

        self.run.started_at = None
        set_started_at(self.run)
        assert self.run.started_at >= started_at

        self.run.started_at = None
        self.run.status = V1Statuses.WARNING
        set_started_at(self.run)
        assert self.run.started_at is None

    def test_finished_at(self):
        assert self.run.finished_at is None
        set_finished_at(self.run)
        assert self.run.finished_at is None

        self.run.status = V1Statuses.STARTING
        set_finished_at(self.run)
        assert self.run.finished_at is None

        self.run.status = V1Statuses.RUNNING
        set_finished_at(self.run)
        assert self.run.finished_at is None

        self.run.status = V1Statuses.SUCCEEDED
        set_finished_at(self.run)
        assert self.run.finished_at is not None

        finished_at = self.run.finished_at

        self.run.status = V1Statuses.FAILED
        set_finished_at(self.run)
        assert self.run.finished_at == finished_at  # No changes

        self.run.finished_at = None
        set_finished_at(self.run)
        assert self.run.finished_at >= finished_at
