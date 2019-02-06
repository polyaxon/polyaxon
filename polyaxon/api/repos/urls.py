from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.repos import views
from constants.urls import ID_PATTERN, OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN

urlpatterns = [
    re_path(r'^{}/{}/repo/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.RepoDetailView.as_view()),
    re_path(r'^{}/{}/repo/upload/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.UploadFilesView.as_view()),
    re_path(r'^{}/{}/repo/download/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.DownloadFilesView.as_view()),
    re_path(r'^{}/{}/repo/external/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.SetExternalRepoView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
