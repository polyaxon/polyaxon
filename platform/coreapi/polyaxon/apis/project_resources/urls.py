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

from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from apis.project_resources import views
from polycommon.apis.urls import projects

projects_urlpatterns = [
    re_path(projects.URLS_PROJECTS_RUNS_TAG, views.ProjectRunsTagView.as_view(),),
    re_path(
        projects.URLS_PROJECTS_RUNS_ARTIFACTS_LINEAGE,
        views.ProjectRunsArtifactsView.as_view(),
    ),
    re_path(projects.URLS_PROJECTS_RUNS_STOP, views.ProjectRunsStopView.as_view(),),
    re_path(projects.URLS_PROJECTS_RUNS_DELETE, views.ProjectRunsDeleteView.as_view(),),
    re_path(projects.URLS_PROJECTS_RUNS_LIST, views.ProjectRunsListView.as_view(),),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(projects_urlpatterns)
