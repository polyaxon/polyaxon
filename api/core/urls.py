# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from core import views

urlpatterns = [
    url(r'^experiments/?$', views.ExperimentListView.as_view()),
    url(r'^experiments/(?P<pk>[0-9]+)/?$', views.ExperimentDetailView.as_view()),
    url(r'^experiments/(?P<pk>[0-9]+)/estimator/?$', views.ExperimentEstimatorDetailView.as_view()),
    url(r'^experiments/(?P<pk>[0-9]+)/model/?$', views.ExperimentModelDetailView.as_view()),
    url(r'^experiments/(?P<pk>[0-9]+)/start/?$', views.ExperimentStartView.as_view()),
    url(r'^experiments/(?P<pk>[0-9]+)/status/?$', views.ExperimentStartView.as_view()),
    url(r'^estimators/?$', views.EstimatorListView.as_view()),
    url(r'^estimators/(?P<pk>[0-9]+)/?$', views.EstimatorDetailView.as_view()),
    url(r'^models/?$', views.PolyaxonModelListView.as_view()),
    url(r'^models/(?P<pk>[0-9]+)/?$', views.PolyaxonModelDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
