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
from coredb.managers.operations import compile_operation_run
from coredb.managers.runs import copy_run, restart_run, resume_run
from polyaxon.lifecycle import V1Statuses
from polyaxon.polyaxonfile import CompiledOperationSpecification, OperationSpecification
from polyaxon.polyflow import V1CloningKind
from polycommon.events.registry import run as run_events
from polycommon.test_cases.fixtures.jobs import get_fxt_job_with_inputs


class TestRunManager(TestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.project = ProjectFactory()
        op_spec = OperationSpecification.read(values=get_fxt_job_with_inputs())
        self.run = compile_operation_run(
            project_id=self.project.id, op_spec=op_spec, user_id=self.user.id
        )

    @patch("polycommon.auditor.record")
    def test_create_run(self, auditor_record):
        run = RunFactory(project=self.project, user=self.user)
        assert auditor_record.call_count == 1
        call_args, call_kwargs = auditor_record.call_args
        assert call_kwargs["event_type"] == run_events.RUN_CREATED

        assert run.user == self.user
        assert run.project == self.project
        assert run.name is None
        assert run.description is None
        assert run.content is None
        assert run.readme is None
        assert run.tags is None
        assert run.cloning_kind is None
        assert run.original is None

    @patch("polycommon.auditor.record")
    def test_copy_run(self, auditor_record):
        run = copy_run(run=self.run)
        assert auditor_record.call_count == 1
        call_args, call_kwargs = auditor_record.call_args
        assert call_kwargs["event_type"] == run_events.RUN_CREATED
        assert run.user == self.run.user
        assert run.kind == self.run.kind
        assert run.project == self.run.project
        assert run.name == self.run.name
        assert run.description == self.run.description
        assert run.content != self.run.content
        config = CompiledOperationSpecification.read(run.content)
        original_config = CompiledOperationSpecification.read(self.run.content)
        assert len(config.run.init or []) == len(original_config.run.init or []) + 1
        assert run.raw_content == self.run.raw_content
        assert run.readme == self.run.readme
        assert run.tags == self.run.tags
        assert run.cloning_kind == V1CloningKind.COPY
        assert run.original == self.run
        assert run.inputs == {"image": "foo/bar"}

        run = copy_run(
            run=self.run,
            user_id=self.user2.id,
            name="new-name",
            description="new-description",
            content={"trigger": "all_done"},
            readme="new-readme",
            tags=["tag1", "tag2"],
        )
        assert run.user != self.run.user
        assert run.user == self.user2
        assert run.project == self.project
        assert run.name == "new-name"
        assert run.description == "new-description"
        assert run.content != self.run.content
        assert run.raw_content == self.run.raw_content
        assert run.readme == "new-readme"
        assert set(run.tags) == {"tag1", "tag2"}
        assert run.inputs == {"image": "foo/bar"}
        assert run.cloning_kind == V1CloningKind.COPY
        assert run.original == self.run

    @patch("polycommon.auditor.record")
    def test_resume_run(self, auditor_record):
        run = resume_run(run=self.run)
        assert auditor_record.call_count == 2
        call_args_list = auditor_record.call_args_list
        assert call_args_list[0][0] == ()
        assert call_args_list[1][0] == ()
        assert call_args_list[0][1]["event_type"] == run_events.RUN_NEW_STATUS
        assert call_args_list[1][1]["event_type"] == run_events.RUN_RESUMED
        assert run.user == self.run.user
        assert run.kind == self.run.kind
        assert run.project == self.run.project
        assert run.name == self.run.name
        assert run.description == self.run.description
        assert run.content == self.run.content
        assert run.raw_content == self.run.raw_content
        assert run.readme == self.run.readme
        assert run.tags == self.run.tags
        assert run.status == V1Statuses.RESUMING
        assert run.cloning_kind is None
        assert run.original is None
        assert run.inputs == {"image": "foo/bar"}

        user = UserFactory()
        run = resume_run(
            run=self.run,
            user_id=user.id,
            name="new-name",
            description="new-description",
            content={"trigger": "all_done"},
            readme="new-readme",
            tags=["tag1", "tag2"],
        )
        assert run.user == user
        assert run.project == self.project
        assert run.name == "new-name"
        assert run.description == "new-description"
        assert run.content == self.run.content
        assert run.raw_content == self.run.raw_content
        assert run.readme == "new-readme"
        assert set(run.tags) == {"tag1", "tag2"}
        assert run.cloning_kind is None
        assert run.original is None

    @patch("polycommon.auditor.record")
    def test_restart_run(self, auditor_record):
        run = restart_run(run=self.run)
        assert auditor_record.call_count == 1
        call_args, call_kwargs = auditor_record.call_args
        assert call_kwargs["event_type"] == run_events.RUN_CREATED
        assert run.kind == self.run.kind
        assert run.user == self.run.user
        assert run.project == self.run.project
        assert run.name == self.run.name
        assert run.description == self.run.description
        assert run.content == self.run.content
        assert run.readme == self.run.readme
        assert run.tags == self.run.tags
        assert run.cloning_kind == V1CloningKind.RESTART
        assert run.original == self.run

        run = restart_run(
            run=self.run,
            user_id=self.user.id,
            name="new-name",
            description="new-description",
            content={"trigger": "all_done"},
            readme="new-readme",
        )
        assert run.user == self.user
        assert run.project == self.project
        assert run.name == "new-name"
        assert run.description == "new-description"
        assert run.content != self.run.content
        assert run.raw_content == self.run.raw_content
        assert run.readme == "new-readme"
        assert set(run.tags) == {"tag1", "tag2"}
        assert run.cloning_kind == V1CloningKind.RESTART
        assert run.original == self.run
