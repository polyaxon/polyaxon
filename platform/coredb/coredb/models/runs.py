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
from coredb.abstracts.is_managed import IsManagedModel
from coredb.abstracts.nameable import NameableModel
from coredb.abstracts.readme import ReadmeModel
from coredb.abstracts.runtime import RunTimeModel
from coredb.abstracts.spec import SpecModel
from coredb.abstracts.state import OptionalStateModel
from coredb.abstracts.status import StatusModel
from coredb.abstracts.tag import TagModel
from coredb.abstracts.uid import UuidModel
from polyaxon.lifecycle import V1Statuses
from polyaxon.polyflow import V1CloningKind, V1RunKind


class Run(
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
    OptionalStateModel,
):
    kind = models.CharField(max_length=12, db_index=True, choices=V1RunKind.CHOICES)
    project = models.ForeignKey(
        "coredb.Project", on_delete=models.CASCADE, related_name="runs"
    )
    meta_info = JSONField(null=True, blank=True, default=dict,)
    pipeline = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="pipeline_runs",
    )
    controller = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="controller_runs",
    )
    upstream_runs = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        through="coredb.RunEdge",
        related_name="downstream_runs",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+"
    )
    params = JSONField(null=True, blank=True)
    inputs = JSONField(null=True, blank=True)
    outputs = JSONField(null=True, blank=True)
    original = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="clones",
    )
    cloning_kind = models.CharField(
        max_length=12, blank=True, null=True, choices=V1CloningKind.CHOICES,
    )

    class Meta:
        app_label = "coredb"
        db_table = "db_run"
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
    def is_dag(self):
        return self.kind == V1RunKind.DAG

    @property
    def is_service(self):
        return self.kind == V1RunKind.SERVICE

    @property
    def is_matrix(self):
        return self.kind == V1RunKind.MATRIX

    @property
    def has_pipeline(self):
        return self.is_dag or self.is_matrix
