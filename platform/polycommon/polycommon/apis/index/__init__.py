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

from typing import List

from django.contrib import admin
from django.urls import include, re_path
from django.views.decorators.csrf import ensure_csrf_cookie

from polyaxon.api import ADMIN_V1, UI_V1
from polycommon import conf
from polycommon.apis.index.errors import Handler50xView, Handler403View, Handler404View
from polycommon.apis.index.health import HealthView
from polycommon.apis.index.views import IndexView
from polycommon.options.registry.core import UI_ADMIN_ENABLED


def _handler500(request):
    return Handler50xView.as_view()(request)


handler404 = Handler404View.as_view()
handler403 = Handler403View.as_view()
handler500 = _handler500


def get_ui_urlpatterns(ui_urlpatterns):
    ui_patterns = [
        re_path(pattern, ensure_csrf_cookie(IndexView.as_view()), name="index")
        for pattern in ui_urlpatterns
    ]
    return [
        re_path(r"^$", ensure_csrf_cookie(IndexView.as_view()), name="index"),
        re_path(
            r"^{}$".format(UI_V1), ensure_csrf_cookie(IndexView.as_view()), name="ui"
        ),
        re_path(
            r"^{}/".format(UI_V1), include((ui_patterns, "ui_v1"), namespace="ui_v1")
        ),
    ]


def get_urlpatterns(app_patterns: List, ui_urlpatterns: List):
    if conf.get(UI_ADMIN_ENABLED):
        app_patterns += [re_path(r"^{}/".format(ADMIN_V1), admin.site.urls)]

    urlpatterns = app_patterns + [
        re_path(r"^healthz/?$", HealthView.as_view(), name="health_check"),
    ]
    urlpatterns += get_ui_urlpatterns(ui_urlpatterns)

    return urlpatterns
