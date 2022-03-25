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

from typing import Dict

from polyaxon.client.init import get_client_or_raise
from polyaxon.polyboard.artifacts import V1ArtifactKind


def create_file_lineage(filepath: str, summary: Dict, kind: str):
    if not filepath:
        return
    filename = os.path.basename(filepath)
    if not kind:
        if "dockerfile" in filename.lower():
            kind = V1ArtifactKind.DOCKERFILE
        else:
            kind = V1ArtifactKind.FILE

    run_client = get_client_or_raise()
    if not run_client:
        return

    run_client.log_artifact_ref(
        path=filepath,
        kind=kind,
        name=filename,
        summary=summary,
        is_input=True,
    )
