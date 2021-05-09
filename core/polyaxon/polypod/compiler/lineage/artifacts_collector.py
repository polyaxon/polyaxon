#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

from typing import Optional

from polyaxon.polyboard.artifacts import V1ArtifactKind, V1RunArtifact
from polyaxon.utils.fqn_utils import to_fqn_name


def collect_lineage_artifacts_path(artifact_path: str) -> Optional[V1RunArtifact]:
    name = os.path.basename(artifact_path)
    return V1RunArtifact(
        name=to_fqn_name(name),
        kind=V1ArtifactKind.DIR,
        path=artifact_path,
        summary={"path": artifact_path},
        is_input=True,
    )
