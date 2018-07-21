from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.activitylogs import views
from constants.urls import NAME_PATTERN, USERNAME_PATTERN

build_jobs_urlpatterns = [
    re_path(r'^activitylogs/?$',
            views.ActivityLogsView.as_view()),
    re_path(r'^activitylogs/{}/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.ProjectActivityLogsView.as_view()),
]

urlpatterns = format_suffix_patterns(build_jobs_urlpatterns)
