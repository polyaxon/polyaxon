# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from libs.urls import NAME_PATTERN, USERNAME_PATTERN
from plugins import views

plugin_urlpatterns = [
    url(r'^notebook/{}/{}/?(?P<path>.*)/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
        views.NotebookView.as_view()),
    url(r'^tensorboard/{}/{}/?(?P<path>.*)/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
        views.TensorboardView.as_view()),
]

urlpatterns = format_suffix_patterns(plugin_urlpatterns)
