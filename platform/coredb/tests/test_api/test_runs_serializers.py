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

import pytest

from coredb.api.runs.serializers import (
    RunDetailSerializer,
    RunSerializer,
    RunStatusSerializer,
)
from coredb.factories.runs import RunFactory
from coredb.managers.statuses import new_run_status, new_run_stop_status
from coredb.models.runs import Run
from polyaxon.lifecycle import V1StatusCondition, V1Statuses
from polyaxon.polyflow import V1CloningKind
from tests.test_api.base import BaseTestRunSerializer


@pytest.mark.serializers_mark
class TestRunSerializer(BaseTestRunSerializer):
    serializer_class = RunSerializer
    model_class = Run
    factory_class = RunFactory
    expected_keys = {
        "uuid",
        "name",
        "project",
        "description",
        "created_at",
        "updated_at",
        "started_at",
        "finished_at",
        "run_time",
        "status",
        "kind",
        "meta_info",
        "original",
        "is_managed",
        "tags",
        "inputs",
        "outputs",
    }
    query = Run.objects

    def create_one(self):
        return self.factory_class(project=self.project, user=self.user)

    def create_one_with_related(self):
        run = self.factory_class(project=self.project, user=self.user)
        run = self.factory_class(
            project=self.project,
            original=run,
            cloning_kind=V1CloningKind.CACHE,
            status=V1Statuses.RUNNING,
        )
        return run

    def test_serialize_one(self):
        obj1 = self.create_one_with_related()

        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop("uuid") == obj1.uuid.hex
        assert data.pop("project") == obj1.project.name
        assert data.pop("original") == {
            "uuid": obj1.original.uuid.hex,
            "name": obj1.original.name,
            "kind": obj1.cloning_kind,
        }
        data.pop("created_at")
        data.pop("updated_at")
        data.pop("started_at", None)
        data.pop("finished_at", None)

        for k, v in data.items():
            assert getattr(obj1, k) == v


@pytest.mark.serializers_mark
class TestRunDetailSerializer(TestRunSerializer):
    serializer_class = RunDetailSerializer
    model_class = Run
    factory_class = RunFactory
    expected_keys = TestRunSerializer.expected_keys | {
        "readme",
        "content",
    }

    def test_serialize_one(self):
        obj1 = self.create_one_with_related()
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop("uuid") == obj1.uuid.hex
        assert data.pop("project") == obj1.project.name
        assert data.pop("original") == {
            "uuid": obj1.original.uuid.hex,
            "name": obj1.original.name,
            "kind": obj1.cloning_kind,
        }
        data.pop("created_at")
        data.pop("updated_at")
        data.pop("started_at", None)
        data.pop("finished_at", None)

        for k, v in data.items():
            assert getattr(obj1, k) == v

        _ = self.serializer_class(obj1.original).data


@pytest.mark.serializers_mark
class TestRunStatusSerializer(TestRunSerializer):
    serializer_class = RunStatusSerializer
    model_class = Run
    factory_class = RunFactory
    expected_keys = {"uuid", "status", "status_conditions"}

    def create_one(self):
        run = super().create_one()
        condition = V1StatusCondition.get_condition(
            type=V1Statuses.RUNNING,
            status="True",
            reason="Run is running",
            message="foo",
        )
        new_run_status(run, condition)
        new_run_stop_status(run, "stopping")
        return run

    def test_serialize_one(self):
        obj1 = self.create_one()
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop("uuid") == obj1.uuid.hex

        for k, v in data.items():
            assert getattr(obj1, k) == v

    def test_serialize_many(self):
        pass


del BaseTestRunSerializer
