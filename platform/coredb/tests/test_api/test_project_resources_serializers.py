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

import pytest

from coredb.api.project_resources.serializers import (
    OfflineRunSerializer,
    OperationCreateSerializer,
    RunSerializer,
)
from coredb.factories.runs import RunFactory
from coredb.models.runs import Run
from polyaxon.lifecycle import V1Statuses
from polyaxon.polyflow import V1CloningKind
from polycommon import conf
from polycommon.options.registry.k8s import K8S_NAMESPACE
from tests.test_api.base import BaseTestRunSerializer


@pytest.mark.serializers_mark
class TestRunSerializer(BaseTestRunSerializer):
    serializer_class = RunSerializer
    model_class = Run
    factory_class = RunFactory
    expected_keys = {
        "uuid",
        "name",
        "created_at",
        "updated_at",
        "started_at",
        "finished_at",
        "wait_time",
        "duration",
        "status",
        "kind",
        "runtime",
        "meta_info",
        "pipeline",
        "original",
        "is_managed",
        "pending",
        "tags",
        "inputs",
        "outputs",
        "settings",
    }
    query = Run.objects

    def create_one(self):
        return self.factory_class(project=self.project, user=self.user)

    def create_one_with_related(self):
        run = self.factory_class(project=self.project, user=self.user)
        return self.factory_class(
            project=self.project,
            pipeline=run,
            original=run,
            cloning_kind=V1CloningKind.CACHE,
            status=V1Statuses.RUNNING,
        )

    def test_serialize_one(self):
        obj1 = self.create_one_with_related()

        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop("uuid") == obj1.uuid.hex
        assert data.pop("original") == {
            "uuid": obj1.original.uuid.hex,
            "name": obj1.original.name,
            "kind": obj1.cloning_kind,
        }
        assert data.pop("pipeline") == {
            "uuid": obj1.pipeline.uuid.hex,
            "name": obj1.pipeline.name,
            "kind": obj1.pipeline.kind,
        }
        assert data.pop("settings") == {"namespace": conf.get(K8S_NAMESPACE)}
        data.pop("created_at")
        data.pop("updated_at")
        data.pop("started_at", None)
        data.pop("finished_at", None)

        for k, v in data.items():
            assert getattr(obj1, k) == v


@pytest.mark.projects_resources_mark
class TestOperationCreateSerializer(BaseTestRunSerializer):
    serializer_class = OperationCreateSerializer
    model_class = Run
    factory_class = RunFactory
    expected_keys = {"uuid", "name", "description", "content", "is_managed", "tags"}
    query = Run.objects

    def create_one(self):
        return self.factory_class(project=self.project)

    def create_one_with_related(self):
        return self.factory_class(project=self.project, user=self.user)

    def test_serialize_one(self):
        obj1 = self.create_one_with_related()

        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop("uuid") == obj1.uuid.hex

        for k, v in data.items():
            assert getattr(obj1, k) == v


@pytest.mark.projects_resources_mark
class TestOfflineRunSerializer(BaseTestRunSerializer):
    serializer_class = OfflineRunSerializer
    model_class = Run
    factory_class = RunFactory
    expected_keys = {
        "uuid",
        "name",
        "description",
        "tags",
        "created_at",
        "updated_at",
        "started_at",
        "finished_at",
        "wait_time",
        "duration",
        "kind",
        "runtime",
        "meta_info",
        "status",
        "status_conditions",
        "is_managed",
        "inputs",
        "outputs",
    }
    query = Run.objects

    def create_one(self):
        return self.factory_class(project=self.project)

    def test_serialize_one(self):
        obj1 = self.create_one()

        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop("uuid") == obj1.uuid.hex
        assert data.pop("created_at") is not None
        assert data.pop("updated_at") is not None

        for k, v in data.items():
            assert getattr(obj1, k) == v


del BaseTestRunSerializer
