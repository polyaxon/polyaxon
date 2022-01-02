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


from coredb.abstracts.artifacts import BaseArtifact, BaseArtifactLineage


class Artifact(BaseArtifact):
    class Meta:
        app_label = "coredb"
        unique_together = (("name", "state"),)
        db_table = "db_artifact"


class ArtifactLineage(BaseArtifactLineage):
    class Meta:
        app_label = "coredb"
        unique_together = (("run", "artifact", "is_input"),)
        db_table = "db_artifactlineage"
