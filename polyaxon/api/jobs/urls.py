from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.bookmarks import views as bookmark_views
from api.jobs import views
from constants.urls import JOB_ID_PATTERN, OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, UUID_PATTERN

jobs_urlpatterns = [
    re_path(r'^{}/{}/jobs/{}/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.JobDetailView.as_view()),
    re_path(r'^{}/{}/jobs/{}/archive/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.JobArchiveView.as_view()),
    re_path(r'^{}/{}/jobs/{}/restore/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.JobRestoreView.as_view()),
    re_path(r'^{}/{}/jobs/{}/restart/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.JobRestartView.as_view()),
    re_path(r'^{}/{}/jobs/{}/statuses/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.JobStatusListView.as_view()),
    re_path(r'^{}/{}/jobs/{}/statuses/{}/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN, UUID_PATTERN),
        views.JobStatusDetailView.as_view()),
    re_path(r'^{}/{}/jobs/{}/logs/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.JobLogsView.as_view()),
    re_path(r'^{}/{}/jobs/{}/stop/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.JobStopView.as_view()),
    re_path(r'^{}/{}/jobs/{}/outputs/download/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.JobDownloadOutputsView.as_view()),
    re_path(r'^{}/{}/jobs/{}/outputs/tree/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.JobOutputsTreeView.as_view()),
    re_path(r'^{}/{}/jobs/{}/outputs/files/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.JobOutputsFilesView.as_view()),
    re_path(r'^{}/{}/jobs/{}/_heartbeat/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.JobHeartBeatView.as_view()),
    re_path(r'^{}/{}/jobs/{}/bookmark/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        bookmark_views.JobBookmarkCreateView.as_view()),
    re_path(r'^{}/{}/jobs/{}/unbookmark/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        bookmark_views.JobBookmarkDeleteView.as_view()),
    re_path(r'^{}/{}/jobs/{}/imporsonatetoken/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.JobImpersonateTokenView.as_view()),
]

urlpatterns = format_suffix_patterns(jobs_urlpatterns)
