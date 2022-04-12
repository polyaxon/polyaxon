#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from django.contrib.admin import site
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from coredb.abstracts.getter import get_artifact_model, get_project_model, get_run_model
from coredb.administration.artifacts import ArtifactAdmin
from coredb.administration.projects import ProjectAdmin
from coredb.administration.runs import RunLightAdmin

site.register(get_user_model(), UserAdmin)
site.register(get_artifact_model(), ArtifactAdmin)
site.register(get_project_model(), ProjectAdmin)
site.register(get_run_model(), RunLightAdmin)
