# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from versions import views

urlpatterns = [
    url(r'^versions/cli/?$', views.CliVersionView.as_view()),
    url(r'^versions/platform/?$', views.PlatformVersionView.as_view()),
    url(r'^versions/lib/?$', views.LibVersionView.as_view()),
    url(r'^versions/chart/?$', views.ChartVersionView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
