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
from django.contrib.postgres.fields import JSONField
from django.db import models

from coredb.abstracts.deleted import DeletedModel
from coredb.abstracts.describable import DescribableModel
from coredb.abstracts.diff import DiffModel
from coredb.abstracts.getter import get_db_model_name
from coredb.abstracts.is_managed import IsManagedModel
from coredb.abstracts.nameable import NameableModel
from coredb.abstracts.readme import ReadmeModel
from coredb.abstracts.runtime import RunTimeModel
from coredb.abstracts.spec import SpecModel
from coredb.abstracts.status import StatusModel
from coredb.abstracts.tag import TagModel
from coredb.abstracts.uid import UuidModel
from polyaxon.lifecycle import V1Statuses
from polyaxon.polyflow import V1CloningKind, V1RunKind


class BaseRun(
    UuidModel,
    DiffModel,
    RunTimeModel,
    SpecModel,
    IsManagedModel,
    NameableModel,
    DescribableModel,
    ReadmeModel,
    StatusModel,
    TagModel,
    DeletedModel,
):
    kind = models.CharField(max_length=12, db_index=True, choices=V1RunKind.CHOICES)
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
    meta_info = JSONField(null=True, blank=True, default=dict,)
    params = JSONField(null=True, blank=True)
    inputs = JSONField(null=True, blank=True)
    outputs = JSONField(null=True, blank=True)
    original = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="clones",
    )
    cloning_kind = models.CharField(
        max_length=12, blank=True, null=True, choices=V1CloningKind.CHOICES,
    )
    artifacts = models.ManyToManyField(
        get_db_model_name("Artifact"),
        blank=True,
        through=get_db_model_name("ArtifactLineage"),
        related_name="runs",
    )

    class Meta:
        abstract = True

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
