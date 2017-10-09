# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from experiments import views

urlpatterns = [
    url(r'^experiments/?$', views.ExperimentListView.as_view()),
    url(r'^experiments/(?P<uuid>\w+)/?$', views.ExperimentDetailView.as_view()),
    url(r'^experiments/(?P<uuid>\w+)/start/?$', views.ExperimentStartView.as_view()),
    url(r'^experiments/(?P<uuid>\w+)/status/?$', views.ExperimentStartView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
