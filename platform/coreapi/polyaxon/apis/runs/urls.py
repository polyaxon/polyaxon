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

from apis.runs import views
from polycommon.apis.urls import runs

runs_urlpatterns = [
    re_path(runs.URLS_RUNS_DETAILS, views.RunDetailView.as_view()),
    re_path(runs.URLS_RUNS_RESTART, views.RunRestartView.as_view()),
    re_path(runs.URLS_RUNS_RESUME, views.RunResumeView.as_view()),
    re_path(runs.URLS_RUNS_COPY, views.RunCopyView.as_view()),
    re_path(runs.URLS_RUNS_STOP, views.RunStopView.as_view()),
    re_path(runs.URLS_RUNS_STATUSES, views.RunStatusListView.as_view()),
    re_path(runs.URLS_RUNS_NAMESPACE, views.RunNamespaceView.as_view()),
]

urlpatterns = format_suffix_patterns(runs_urlpatterns)
