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

import polyaxon_sdk


class V1ArtifactKind(polyaxon_sdk.V1ArtifactKind):
    CHOICES = (
        (polyaxon_sdk.V1ArtifactKind.MODEL, polyaxon_sdk.V1ArtifactKind.MODEL),
        (polyaxon_sdk.V1ArtifactKind.AUDIO, polyaxon_sdk.V1ArtifactKind.AUDIO),
        (polyaxon_sdk.V1ArtifactKind.VIDEO, polyaxon_sdk.V1ArtifactKind.VIDEO),
        (polyaxon_sdk.V1ArtifactKind.HISTOGRAM, polyaxon_sdk.V1ArtifactKind.HISTOGRAM),
        (polyaxon_sdk.V1ArtifactKind.IMAGE, polyaxon_sdk.V1ArtifactKind.IMAGE),
        (polyaxon_sdk.V1ArtifactKind.TENSOR, polyaxon_sdk.V1ArtifactKind.TENSOR),
        (polyaxon_sdk.V1ArtifactKind.DATAFRAME, polyaxon_sdk.V1ArtifactKind.DATAFRAME),
        (polyaxon_sdk.V1ArtifactKind.CHART, polyaxon_sdk.V1ArtifactKind.CHART),
        (polyaxon_sdk.V1ArtifactKind.CSV, polyaxon_sdk.V1ArtifactKind.CSV),
        (polyaxon_sdk.V1ArtifactKind.TSV, polyaxon_sdk.V1ArtifactKind.TSV),
        (polyaxon_sdk.V1ArtifactKind.PSV, polyaxon_sdk.V1ArtifactKind.PSV),
        (polyaxon_sdk.V1ArtifactKind.SSV, polyaxon_sdk.V1ArtifactKind.SSV),
        (polyaxon_sdk.V1ArtifactKind.METRIC, polyaxon_sdk.V1ArtifactKind.METRIC),
        (polyaxon_sdk.V1ArtifactKind.ENV, polyaxon_sdk.V1ArtifactKind.ENV),
        (polyaxon_sdk.V1ArtifactKind.HTML, polyaxon_sdk.V1ArtifactKind.HTML),
        (polyaxon_sdk.V1ArtifactKind.TEXT, polyaxon_sdk.V1ArtifactKind.TEXT),
        (polyaxon_sdk.V1ArtifactKind.FILE, polyaxon_sdk.V1ArtifactKind.FILE),
        (polyaxon_sdk.V1ArtifactKind.DIR, polyaxon_sdk.V1ArtifactKind.DIR),
        (
            polyaxon_sdk.V1ArtifactKind.TENSORBOARD,
            polyaxon_sdk.V1ArtifactKind.TENSORBOARD,
        ),
        (
            polyaxon_sdk.V1ArtifactKind.DOCKERFILE,
            polyaxon_sdk.V1ArtifactKind.DOCKERFILE,
        ),
        (
            polyaxon_sdk.V1ArtifactKind.DOCKER_IMAGE,
            polyaxon_sdk.V1ArtifactKind.DOCKER_IMAGE,
        ),
        (polyaxon_sdk.V1ArtifactKind.DATA, polyaxon_sdk.V1ArtifactKind.DATA),
        (polyaxon_sdk.V1ArtifactKind.CODEREF, polyaxon_sdk.V1ArtifactKind.CODEREF),
        (polyaxon_sdk.V1ArtifactKind.TABLE, polyaxon_sdk.V1ArtifactKind.TABLE),
        (polyaxon_sdk.V1ArtifactKind.CURVE, polyaxon_sdk.V1ArtifactKind.CURVE),
    )
