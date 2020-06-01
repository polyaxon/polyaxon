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

from django.contrib.postgres.fields import JSONField
from django.db import models

from coredb.abstracts.diff import DiffModel
from coredb.abstracts.state import StateModel
from polyaxon.polyboard.artifacts import V1ArtifactKind


class Artifact(DiffModel, StateModel):
    runs = models.ManyToManyField(
        "coredb.Run",
        blank=True,
        through="coredb.ArtifactLineage",
        related_name="artifacts",
        help_text="list of runs related to this artifact (inputs/outputs).",
    )
    owner = models.ForeignKey(
        "coredb.Owner", on_delete=models.CASCADE, related_name="+"
    )
    name = models.CharField(max_length=64, db_index=True)
    kind = models.CharField(
        max_length=12, db_index=True, choices=V1ArtifactKind.CHOICES,
    )
    path = models.CharField(max_length=256, blank=True, null=True)
    summary = JSONField()

    class Meta:
        unique_together = (("name", "state"),)
        app_label = "coredb"
        db_table = "db_artifact"


class ArtifactLineage(DiffModel):
    run = models.ForeignKey(
        "coredb.Run", on_delete=models.CASCADE, related_name="artifacts_lineage"
    )
    artifact = models.ForeignKey(
        "coredb.Artifact", on_delete=models.CASCADE, related_name="runs_lineage"
    )
    is_input = models.NullBooleanField(null=True, blank=True, default=False)

    class Meta:
        unique_together = (("run", "artifact", "is_input"),)
        app_label = "coredb"
        db_table = "db_artifact_lineage"
