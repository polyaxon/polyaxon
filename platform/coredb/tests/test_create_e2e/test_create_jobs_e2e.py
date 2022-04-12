#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from coredb import operations
from coredb.factories.projects import ProjectFactory
from coredb.factories.users import UserFactory
from coredb.models.runs import Run
from polyaxon.polyaxonfile import CompiledOperationSpecification, OperationSpecification
from polyaxon.polyflow import V1RunKind
from polycommon.test_cases.fixtures import get_fxt_job, get_fxt_job_with_inputs


class TestCreateJobs(TestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.project = ProjectFactory()

    def test_create_run_with_job_spec(self):
        count = Run.objects.count()
        config_dict = get_fxt_job()
        spec = OperationSpecification.read(values=config_dict)
        run = operations.init_and_save_run(
            project_id=self.project.id, user_id=self.user.id, op_spec=spec
        )
        assert Run.objects.count() == count + 1
        assert run.pending is None
        assert run.kind == V1RunKind.JOB
        assert run.name == "foo"
        assert run.description == "a description"
        assert set(run.tags) == {"tag1", "tag2"}
        # Check compiled operation passes
        compiled_operation = CompiledOperationSpecification.read(run.content)
        compiled_operation = CompiledOperationSpecification.apply_params(
            compiled_operation
        )
        CompiledOperationSpecification.apply_runtime_contexts(compiled_operation)
        # Check job
        job_spec = CompiledOperationSpecification.read(run.content)
        assert job_spec.run.container.image == "test"
        job_spec = CompiledOperationSpecification.apply_operation_contexts(job_spec)
        assert job_spec.run.container.image == "test"

    def test_create_run_with_templated_job_spec(self):
        count = Run.objects.count()
        config_dict = get_fxt_job_with_inputs()
        spec = OperationSpecification.read(values=config_dict)
        run = operations.init_and_save_run(
            project_id=self.project.id, user_id=self.user.id, op_spec=spec
        )
        assert Run.objects.count() == count + 1
        assert run.pending is None
        assert run.kind == V1RunKind.JOB
        assert run.name == "foo"
        assert run.description == "a description"
        assert set(run.tags) == {"tag1", "tag2"}  # From template
        compiled_operation = CompiledOperationSpecification.read(run.content)
        compiled_operation = CompiledOperationSpecification.apply_params(
            compiled_operation, params=spec.params
        )
        compiled_operation = CompiledOperationSpecification.apply_operation_contexts(
            compiled_operation
        )
        CompiledOperationSpecification.apply_runtime_contexts(compiled_operation)
        run.content = compiled_operation.to_dict(dump=True)
        run.save(update_fields=["content"])
        job_spec = CompiledOperationSpecification.read(run.content)
        assert job_spec.run.container.image == "{{ image }}"
        job_spec = CompiledOperationSpecification.apply_runtime_contexts(job_spec)
        assert job_spec.run.container.image == "foo/bar"
