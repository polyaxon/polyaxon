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

from django.db import models

from coredb.abstracts.diff import DiffModel
from coredb.abstracts.getter import get_db_model_name
from coredb.abstracts.state import StateModel
from polyaxon.polyboard.artifacts import V1ArtifactKind


class BaseArtifact(DiffModel, StateModel):
    name = models.CharField(max_length=64, db_index=True)
    kind = models.CharField(
        max_length=12,
        db_index=True,
        choices=V1ArtifactKind.CHOICES,
    )
    path = models.CharField(max_length=256, blank=True, null=True)
    summary = models.JSONField()

    class Meta:
        abstract = True


class BaseArtifactLineage(DiffModel):
    run = models.ForeignKey(
        get_db_model_name("Run"),
        on_delete=models.CASCADE,
        related_name="artifacts_lineage",
    )
    artifact = models.ForeignKey(
        get_db_model_name("Artifact"),
        on_delete=models.CASCADE,
        related_name="runs_lineage",
    )
    is_input = models.BooleanField(null=True, blank=True, default=False)

    class Meta:
        abstract = True
