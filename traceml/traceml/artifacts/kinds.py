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

import polyaxon_sdk


class V1ArtifactKind(polyaxon_sdk.V1ArtifactKind):
    @classmethod
    def is_single_file_event(cls, kind: str) -> bool:
        return kind in {
            V1ArtifactKind.HTML,
            V1ArtifactKind.TEXT,
            V1ArtifactKind.HISTOGRAM,
            V1ArtifactKind.CHART,
            V1ArtifactKind.CONFUSION,
            V1ArtifactKind.CURVE,
            V1ArtifactKind.METRIC,
            V1ArtifactKind.SYSTEM,
        }

    @classmethod
    def is_single_or_multi_file_event(cls, kind: str) -> bool:
        return kind in {
            V1ArtifactKind.MODEL,
            V1ArtifactKind.DATAFRAME,
            V1ArtifactKind.AUDIO,
            V1ArtifactKind.VIDEO,
            V1ArtifactKind.IMAGE,
            V1ArtifactKind.CSV,
            V1ArtifactKind.TSV,
            V1ArtifactKind.PSV,
            V1ArtifactKind.SSV,
        }

    @classmethod
    def is_dir(cls, kind: str) -> bool:
        return kind in {
            V1ArtifactKind.TENSORBOARD,
            V1ArtifactKind.DIR,
        }

    @classmethod
    def is_file(cls, kind: str) -> bool:
        return kind in {
            V1ArtifactKind.DOCKERFILE,
            V1ArtifactKind.FILE,
            V1ArtifactKind.ENV,
        }

    @classmethod
    def is_file_or_dir(cls, kind: str) -> bool:
        return kind in {
            V1ArtifactKind.DATA,
            V1ArtifactKind.MODEL,
        }
