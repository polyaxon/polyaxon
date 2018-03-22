# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from libs.urls import USERNAME_PATTERN, NAME_PATTERN
from datasets import views

urlpatterns = [
    re_path(r'^{}/{}/datasets/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.DatasetDetailView.as_view()),
    re_path(r'^{}/{}/datasets/upload/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.UploadDataView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
