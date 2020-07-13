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

from django.urls import include, re_path

from polyaxon.api import API_V1
from polycommon.apis.index import get_urlpatterns, handler403, handler404, handler500
from polycommon.apis.regex import OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN

api_patterns = [
    re_path(r"", include(("apis.versions.urls", "versions"), namespace="versions")),
]

api_patterns += [
    re_path(
        r"",
        include(
            ("apis.project_resources.urls", "project_resources"),
            namespace="project_resources",
        ),
    ),
    re_path(r"", include(("apis.artifacts.urls", "artifacts"), namespace="artifacts")),
    re_path(r"", include(("apis.runs.urls", "runs"), namespace="runs")),
    re_path(r"", include(("apis.projects.urls", "projects"), namespace="projects")),
]

app_urlpatterns = [
    re_path(
        r"^{}/".format(API_V1), include((api_patterns, "api-v1"), namespace="api-v1")
    ),
]

# UI
projects_urls = "{}/{}".format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN)
orgs_urls = "orgs/{}".format(OWNER_NAME_PATTERN)
ui_urlpatterns = [
    r"^$",
    r"^{}/?".format(orgs_urls),
    r"^{}/projects/?".format(orgs_urls),
    r"^{}/?$".format(projects_urls),
    r"^{}/runs.*/?".format(projects_urls),
    r"^{}/jobs.*/?".format(projects_urls),
    r"^{}/services.*/?".format(projects_urls),
    r"^{}/cli.*/?".format(projects_urls),
    r"^{}/settings/?".format(projects_urls),
    r"^{}/new.*/?".format(projects_urls),
]

handler404 = handler404
handler403 = handler403
handler500 = handler500
urlpatterns = get_urlpatterns(app_urlpatterns, ui_urlpatterns)
