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

from coredb.factories.runs import RunFactory
from coredb.models.artifacts import Artifact
from polyaxon.polyboard.artifacts.kinds import V1ArtifactKind
from polyaxon.polyboard.artifacts.schemas import V1RunArtifact
from scheduler.tasks.runs import runs_set_artifacts
from tests.base.case import BaseTest


class TestSetArtifacts(BaseTest):
    def test_runs_set_artifacts(self):
        experiment = RunFactory(project=self.project, user=self.user)
        state = experiment.uuid
        assert experiment.artifacts.count() == 0

        metric1 = V1RunArtifact(
            name="accuracy",
            kind=V1ArtifactKind.METRIC,
            path="accuracy",
            summary=dict(last_value=0.77, max_value=0.99, min_value=0.1, max_step=100),
        )
        metric2 = V1RunArtifact(
            name="precision",
            kind=V1ArtifactKind.METRIC,
            path="precision",
            state=state,
            summary=dict(last_value=0.8, max_value=0.99, min_value=0.11, max_step=100),
        )
        runs_set_artifacts(
            run_id=experiment.id, artifacts=[metric1.to_dict(), metric2.to_dict()]
        )

        assert experiment.artifacts.count() == 2
        results = {r.name: V1RunArtifact.from_model(r) for r in Artifact.objects.all()}
        result1 = results["accuracy"].to_dict()
        # State is generated
        assert result1.pop("state") is not None
        assert result1 == metric1.to_dict()
        result2 = results["precision"].to_dict()
        # State is the same
        assert result2 == metric2.to_dict()

        metric1 = V1RunArtifact(
            name="accuracy",
            kind=V1ArtifactKind.METRIC,
            path="accuracy",
            state=state,
            summary=dict(last_value=0.8, max_value=0.99, min_value=0.1, max_step=100),
        )
        metric3 = V1RunArtifact(
            name="recall",
            kind=V1ArtifactKind.METRIC,
            path="recall",
            state=state,
            summary=dict(last_value=0.1, max_value=0.2, min_value=0.1, max_step=100),
        )
        runs_set_artifacts(
            run_id=experiment.id, artifacts=[metric1.to_dict(), metric3.to_dict()]
        )

        assert experiment.artifacts.count() == 3
        results = {r.name: V1RunArtifact.from_model(r) for r in Artifact.objects.all()}
        assert results["accuracy"].to_dict() == metric1.to_dict()
        assert results["precision"].to_dict() == metric2.to_dict()
        assert results["recall"].to_dict() == metric3.to_dict()
