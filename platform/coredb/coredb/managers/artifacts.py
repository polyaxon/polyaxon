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

from typing import List

from django.db import transaction

from coredb.models.artifacts import Artifact, ArtifactLineage
from coredb.models.projects import Owner
from coredb.models.runs import Run
from polyaxon.polyboard.artifacts import V1RunArtifact


@transaction.atomic
def set_artifacts(run: Run, artifacts: List[V1RunArtifact]):
    if not artifacts:
        return

    namespace = Owner.uuid

    artifacts_by_names = {m.name: m for m in artifacts}
    artifacts_names = list(artifacts_by_names.keys())
    to_update = Artifact.objects.filter(name__in=artifacts_names)
    to_create = {m for m in artifacts_names if m not in {m.name for m in to_update}}

    if to_create:
        artifacts_to_create = [artifacts_by_names[m] for m in to_create]
        Artifact.objects.bulk_create(
            [
                Artifact(
                    name=m.name,
                    kind=m.kind,
                    path=m.path,
                    state=m.get_state(namespace=namespace),
                    summary=m.summary,
                )
                for m in artifacts_to_create
            ]
        )
    updated = []
    for m in to_update:
        artifact = artifacts_by_names[m.name]
        m.kind = artifact.kind
        m.path = artifact.path
        m.state = artifact.get_state(namespace=namespace)
        m.summary = artifact.summary
        updated.append(m)
    Artifact.objects.bulk_update(updated, ["kind", "path", "summary", "state"])

    # Link artifacts to runs
    artifacts_to_link = Artifact.objects.filter(name__in=artifacts_names).only(
        "id", "name"
    )
    for m in artifacts_to_link:
        ArtifactLineage.objects.get_or_create(
            artifact_id=m.id,
            run_id=run.id,
            is_input=artifacts_by_names[m.name].is_input,
        )
