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

from typing import Dict, List

from polyaxon import settings
from polyaxon.client import RunClient
from polyaxon.env_vars.getters import get_run_info
from polyaxon.exceptions import PolyaxonClientException, PolyaxonContainerException
from polyaxon.polyboard.artifacts import V1ArtifactKind, V1RunArtifact
from polyaxon.utils.np_utils import sanitize_np_types


def _sanitize_suggestion(s: Dict):
    return {k: sanitize_np_types(v) for k, v in s.items()}


def create_iteration_lineage(iteration: int, suggestions: List[Dict]):
    if not settings.CLIENT_CONFIG.no_api:
        try:
            owner, project, run_uuid = get_run_info()
        except PolyaxonClientException as e:
            raise PolyaxonContainerException(e)

        artifact_run = V1RunArtifact(
            name=iteration,
            kind=V1ArtifactKind.ITERATION,
            summary=[_sanitize_suggestion(s) for s in suggestions],
            is_input=False,
        )
        RunClient(owner=owner, project=project, run_uuid=run_uuid).log_artifact_lineage(
            artifact_run
        )
