# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from projects import views

urlpatterns = [
    url(r'^projects/?$', views.ProjectListView.as_view()),
    url(r'^projects/(?P<pk>[0-9]+)/?$', views.ProjectDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
