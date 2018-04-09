from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from datasets import views
from libs.urls import NAME_PATTERN, USERNAME_PATTERN

urlpatterns = [
    re_path(r'^{}/{}/datasets/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.DatasetDetailView.as_view()),
    re_path(r'^{}/{}/datasets/upload/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.UploadDataView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
