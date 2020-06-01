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

from coredb.api.projects.serializers import (
    ProjectDetailSerializer,
    ProjectNameSerializer,
    ProjectSerializer,
)
from tests.test_api.base import BaseTestProjectSerializer


@pytest.mark.serializers_mark
class TestProjectNameSerializer(BaseTestProjectSerializer):
    serializer_class = ProjectNameSerializer
    expected_keys = {"name"}

    def test_serialize_one(self):
        obj1 = self.create_one()
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        for k, v in data.items():
            assert getattr(obj1, k) == v


@pytest.mark.serializers_mark
class TestProjectSerializer(BaseTestProjectSerializer):
    serializer_class = ProjectSerializer
    expected_keys = {
        "uuid",
        "name",
        "description",
        "tags",
        "created_at",
        "updated_at",
        "is_public",
        "deleted",
    }

    def test_serialize_one(self):
        obj1 = self.create_one()
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        data.pop("created_at")
        data.pop("updated_at")
        assert data.pop("uuid") == obj1.uuid.hex

        for k, v in data.items():
            assert getattr(obj1, k) == v


@pytest.mark.serializers_mark
class TestProjectDetailSerializer(TestProjectSerializer):
    serializer_class = ProjectDetailSerializer
    expected_keys = TestProjectSerializer.expected_keys | {
        "readme",
    }

    def test_serialize_one(self):
        obj1 = self.create_one()
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        data.pop("created_at")
        data.pop("updated_at")
        assert data.pop("uuid") == obj1.uuid.hex

        for k, v in data.items():
            assert getattr(obj1, k) == v


del BaseTestProjectSerializer
