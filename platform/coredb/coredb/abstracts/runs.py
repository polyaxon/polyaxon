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
from django.conf import settings
from django.core.validators import validate_slug
from django.db import models

from coredb.abstracts.describable import DescribableModel
from coredb.abstracts.diff import DiffModel
from coredb.abstracts.duration import DurationModel
from coredb.abstracts.getter import get_db_model_name
from coredb.abstracts.live_state import LiveStateModel
from coredb.abstracts.nameable import NameableModel
from coredb.abstracts.readme import ReadmeModel
from coredb.abstracts.spec import SpecModel
from coredb.abstracts.status import StatusModel
from coredb.abstracts.tag import TagModel
from coredb.abstracts.uid import UuidModel
from polyaxon.lifecycle import V1Statuses
from polyaxon.polyflow import V1CloningKind, V1RunKind


class BaseRun(
    UuidModel,
    DiffModel,
    DurationModel,
    SpecModel,
    NameableModel,
    DescribableModel,
    ReadmeModel,
    StatusModel,
    TagModel,
    LiveStateModel,
):
    name = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        default=None,
        validators=[validate_slug],
    )
    kind = models.CharField(max_length=12, db_index=True, choices=V1RunKind.CHOICES)
    runtime = models.CharField(max_length=12, db_index=True, null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        get_db_model_name("Project"), on_delete=models.CASCADE, related_name="runs"
    )
    is_managed = models.BooleanField(
        default=True, help_text="If this entity is managed by the platform."
    )
    is_approved = models.BooleanField(
        default=True, help_text="If this entity requires approval before it should run."
    )
    meta_info = models.JSONField(null=True, blank=True, default=dict)
    params = models.JSONField(null=True, blank=True)
    inputs = models.JSONField(null=True, blank=True)
    outputs = models.JSONField(null=True, blank=True)
    original = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clones",
    )
    pipeline = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="pipeline_runs",
    )
    cloning_kind = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        choices=V1CloningKind.CHOICES,
    )
    artifacts = models.ManyToManyField(
        get_db_model_name("Artifact"),
        blank=True,
        through=get_db_model_name("ArtifactLineage"),
        related_name="runs",
    )

    class Meta:
        abstract = True
        indexes = [models.Index(fields=["name"])]

    @property
    def subpath(self):
        return self.uuid.hex

    @property
    def is_clone(self) -> bool:
        return self.original_id is not None

    @property
    def is_restart(self) -> bool:
        return self.is_clone and self.cloning_kind == V1CloningKind.RESTART

    @property
    def is_resume(self) -> bool:
        if not self.status_conditions:
            return False
        return bool(
            [c for c in self.status_conditions if c.get("type") == V1Statuses.RESUMING]
        )

    @property
    def is_copy(self) -> bool:
        return self.is_clone and self.cloning_kind == V1CloningKind.COPY

    @property
    def is_job(self):
        return self.kind == V1RunKind.JOB

    @property
    def is_service(self):
        return self.kind == V1RunKind.SERVICE

    @property
    def is_dag(self):
        return self.kind == V1RunKind.DAG

    @property
    def is_matrix(self):
        return self.kind == V1RunKind.MATRIX

    @property
    def is_schedule(self):
        return self.kind == V1RunKind.SCHEDULE

    @property
    def has_pipeline(self):
        return self.is_dag or self.is_matrix or self.is_schedule
