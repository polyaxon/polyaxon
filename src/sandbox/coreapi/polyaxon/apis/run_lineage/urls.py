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

from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from apis.run_lineage import views
from polycommon.apis.urls import runs

run_lineages_urlpatterns = [
    re_path(
        runs.URLS_RUNS_ARTIFACTS_LINEAGE_LIST_V0, views.RunArtifactListView.as_view()
    ),
    re_path(
        runs.URLS_RUNS_ARTIFACTS_LINEAGE_NAMES_V0,
        views.RunArtifactNameListView.as_view(),
    ),
    re_path(
        runs.URLS_RUNS_ARTIFACTS_LINEAGE_DETAILS_V0,
        views.RunArtifactDetailView.as_view(),
    ),
    re_path(runs.URLS_RUNS_ARTIFACTS_LINEAGE_LIST, views.RunArtifactListView.as_view()),
    re_path(
        runs.URLS_RUNS_ARTIFACTS_LINEAGE_NAMES, views.RunArtifactNameListView.as_view()
    ),
    re_path(
        runs.URLS_RUNS_ARTIFACTS_LINEAGE_DETAILS, views.RunArtifactDetailView.as_view()
    ),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(run_lineages_urlpatterns)
