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

from django.test import TestCase

from coredb.factories.projects import ProjectFactory
from coredb.factories.runs import RunFactory
from coredb.factories.users import UserFactory
from coredb.managers.artifacts import set_artifacts
from coredb.models.artifacts import Artifact
from polyaxon.polyboard.artifacts.kinds import V1ArtifactKind
from polyaxon.polyboard.artifacts.schemas import V1RunArtifact


class TestArtifacts(TestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.project = ProjectFactory()
        self.run = RunFactory(project=self.project)

    def test_set_metric_artifacts(self):
        state = self.run.uuid
        assert Artifact.objects.count() == 0
        metric1 = V1RunArtifact(
            name="accuracy",
            kind=V1ArtifactKind.METRIC,
            path="accuracy",
            summary=dict(last_value=0.9, max_value=0.9, min_value=0.1),
        )
        metric2 = V1RunArtifact(
            name="precision",
            kind=V1ArtifactKind.METRIC,
            path="precision",
            state=state,
            summary=dict(last_value=0.8, max_value=0.9, min_value=0.1),
        )
        set_artifacts(run=self.run, artifacts=[metric1, metric2])
        assert Artifact.objects.count() == 2
        results = {r.name: V1RunArtifact.from_model(r) for r in Artifact.objects.all()}
        result1 = results["accuracy"].to_dict()
        # State is generated
        assert result1.pop("state") is not None
        assert result1 == metric1.to_dict()
        result2 = results["precision"].to_dict()
        assert result2 == metric2.to_dict()

        metric1 = V1RunArtifact(
            name="accuracy",
            kind=V1ArtifactKind.METRIC,
            path="accuracy",
            state=state,
            summary=dict(last_value=0.9, max_value=0.99, min_value=0.1, max_step=100),
        )
        metric2 = V1RunArtifact(
            name="precision",
            kind=V1ArtifactKind.METRIC,
            path="precision",
            state=state,
            summary=dict(last_value=0.8, max_value=0.99, min_value=0.1, max_step=100),
        )
        set_artifacts(run=self.run, artifacts=[metric1, metric2])
        assert Artifact.objects.count() == 2
        results = {r.name: V1RunArtifact.from_model(r) for r in Artifact.objects.all()}
        assert results["accuracy"].to_dict() == metric1.to_dict()
        assert results["precision"].to_dict() == metric2.to_dict()

        metric1 = V1RunArtifact(
            name="accuracy",
            kind=V1ArtifactKind.METRIC,
            path="accuracy",
            state=state,
            summary=dict(last_value=0.77, max_value=0.99, min_value=0.1, max_step=100),
        )
        metric3 = V1RunArtifact(
            name="new",
            kind=V1ArtifactKind.METRIC,
            path="new",
            state=state,
            summary=dict(last_value=0.8, max_value=0.99, min_value=0.11, max_step=100),
        )
        set_artifacts(run=self.run, artifacts=[metric1, metric3])
        assert Artifact.objects.count() == 3
        results = {r.name: V1RunArtifact.from_model(r) for r in Artifact.objects.all()}
        assert results["accuracy"].to_dict() == metric1.to_dict()
        assert results["precision"].to_dict() == metric2.to_dict()
        assert results["new"].to_dict() == metric3.to_dict()

    def test_set_artifacts(self):
        state = self.run.uuid
        assert Artifact.objects.count() == 0
        artifact1 = V1RunArtifact(
            name="histo",
            path="histo",
            state=state,
            kind=V1ArtifactKind.HISTOGRAM,
            summary=dict(max_step=9, min_step=1),
        )
        artifact2 = V1RunArtifact(
            name="dataframe",
            path="df",
            state=state,
            kind=V1ArtifactKind.DATAFRAME,
            summary=dict(max_step=9, min_step=1),
        )
        set_artifacts(run=self.run, artifacts=[artifact1, artifact2])
        assert Artifact.objects.count() == 2
        results = {r.name: V1RunArtifact.from_model(r) for r in Artifact.objects.all()}
        assert (results["histo"]).to_dict() == artifact1.to_dict()
        assert results["dataframe"].to_dict() == artifact2.to_dict()

        artifact1 = V1RunArtifact(
            name="histo",
            path="histo",
            state=state,
            kind=V1ArtifactKind.HISTOGRAM,
            summary=dict(max_step=90, min_step=1),
        )
        artifact2 = V1RunArtifact(
            name="dataframe",
            path="df",
            state=state,
            kind=V1ArtifactKind.DATAFRAME,
            summary=dict(max_step=90, min_step=1),
        )
        set_artifacts(run=self.run, artifacts=[artifact1, artifact2])
        assert Artifact.objects.count() == 2
        results = {r.name: V1RunArtifact.from_model(r) for r in Artifact.objects.all()}
        assert results["histo"].to_dict() == artifact1.to_dict()
        assert results["dataframe"].to_dict() == artifact2.to_dict()

        artifact1 = V1RunArtifact(
            name="histo",
            path="histo",
            state=state,
            kind=V1ArtifactKind.HISTOGRAM,
            summary=dict(max_step=900, min_step=1),
        )
        artifact3 = V1RunArtifact(
            name="audio",
            path="audio",
            state=state,
            kind=V1ArtifactKind.AUDIO,
            summary=dict(max_step=900, min_step=1),
        )
        set_artifacts(run=self.run, artifacts=[artifact1, artifact3])
        assert Artifact.objects.count() == 3
        results = {r.name: V1RunArtifact.from_model(r) for r in Artifact.objects.all()}
        assert results["histo"].to_dict() == artifact1.to_dict()
        assert results["dataframe"].to_dict() == artifact2.to_dict()
        assert results["audio"].to_dict() == artifact3.to_dict()
