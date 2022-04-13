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

import pytest
import random

from coredb.api.artifacts.serializers import (
    RunArtifactLightSerializer,
    RunArtifactSerializer,
)
from coredb.factories.artifacts import ArtifactFactory
from coredb.factories.projects import ProjectFactory
from coredb.factories.runs import RunFactory
from coredb.models.artifacts import Artifact, ArtifactLineage
from polycommon.test_cases.base import PolyaxonBaseTestSerializer


@pytest.mark.serializers_mark
class TestArtifactSerializer(PolyaxonBaseTestSerializer):
    query = ArtifactLineage.objects
    factory_class = ArtifactFactory
    model_class = Artifact
    serializer_class = RunArtifactSerializer
    expected_keys = {
        "name",
        "kind",
        "path",
        "summary",
        "state",
        "is_input",
        "run",
        "meta_info",
    }

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.run = RunFactory(
            project=self.project,
            content="test",
            raw_content="test",
            is_managed=True,
        )
        self.state = self.project.owner.uuid

    def create_one(self):
        i = random.randint(1, 100)
        artifact = self.factory_class(name=f"name{i}", state=self.state)
        return ArtifactLineage.objects.create(artifact=artifact, run=self.run)

    def test_serialize_one(self):
        obj1 = self.create_one()
        data = self.serializer_class(self.query.get(id=obj1.id)).data

        assert set(data.keys()) == self.expected_keys

        assert data.pop("name") == obj1.artifact.name
        assert data.pop("path") == obj1.artifact.path
        assert data.pop("summary") == obj1.artifact.summary
        assert data.pop("state") == obj1.artifact.state.hex
        assert data.pop("run") == obj1.run.uuid.hex
        assert data.pop("kind") == obj1.artifact.kind
        assert data.pop("meta_info") == {
            "run": {"uuid": obj1.run.uuid.hex, "name": obj1.run.name}
        }
        for k, v in data.items():
            assert getattr(obj1, k) == v


@pytest.mark.serializers_mark
class TestArtifactLightSerializer(PolyaxonBaseTestSerializer):
    query = ArtifactLineage.objects
    factory_class = ArtifactFactory
    model_class = Artifact
    serializer_class = RunArtifactLightSerializer
    expected_keys = {"name", "kind", "is_input"}

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.run = RunFactory(
            project=self.project,
            content="test",
            raw_content="test",
            is_managed=True,
        )
        self.state = self.project.owner.uuid

    def create_one(self):
        i = random.randint(1, 100)
        artifact = self.factory_class(name=f"name{i}", state=self.state)
        return ArtifactLineage.objects.create(artifact=artifact, run=self.run)

    def test_serialize_one(self):
        obj1 = self.create_one()
        data = self.serializer_class(self.query.get(id=obj1.id)).data

        assert set(data.keys()) == self.expected_keys

        assert data.pop("name") == obj1.artifact.name
        assert data.pop("kind") == obj1.artifact.kind
        for k, v in data.items():
            assert getattr(obj1, k) == v


del PolyaxonBaseTestSerializer
