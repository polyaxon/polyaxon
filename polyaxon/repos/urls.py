from django.urls import re_path

from rest_framework.urlpatterns import format_suffix_patterns

from libs.urls import USERNAME_PATTERN, NAME_PATTERN
from repos import views

urlpatterns = [
    re_path(r'^{}/{}/repo/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.RepoDetailView.as_view()),
    re_path(r'^{}/{}/repo/upload/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.UploadFilesView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
