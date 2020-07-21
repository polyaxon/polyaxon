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
import os

from typing import Dict

from polyaxon import settings
from polyaxon.client import RunClient
from polyaxon.env_vars.getters import get_run_info
from polyaxon.exceptions import PolyaxonClientException, PolyaxonContainerException
from polyaxon.polyboard.artifacts import V1ArtifactKind, V1RunArtifact


def create_dockerfile_lineage(dockerfile_path: str, summary: Dict):
    if not dockerfile_path:
        return
    filename = os.path.basename(dockerfile_path)

    if not settings.CLIENT_CONFIG.no_api:
        try:
            owner, project, run_uuid = get_run_info()
        except PolyaxonClientException as e:
            raise PolyaxonContainerException(e)

        artifact_run = V1RunArtifact(
            name=filename,
            kind=V1ArtifactKind.DOCKERFILE,
            path=RunClient.get_rel_asset_path(dockerfile_path),
            summary=summary,
            is_input=True,
        )
        RunClient(owner=owner, project=project, run_uuid=run_uuid).log_artifact_lineage(
            artifact_run
        )
