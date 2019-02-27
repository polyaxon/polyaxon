from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.bookmarks import views as bookmark_views
from api.experiments import views
from constants.urls import (
    EXPERIMENT_ID_PATTERN,
    ID_PATTERN,
    JOB_ID_PATTERN,
    OWNER_NAME_PATTERN,
    PROJECT_NAME_PATTERN,
    UUID_PATTERN
)

experiments_urlpatterns = [
    # Get all experiments
    re_path(r'^experiments/?$', views.ExperimentListView.as_view()),
    re_path(r'^{}/{}/experiments/stop/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.ExperimentStopManyView.as_view()),
    re_path(r'^{}/{}/experiments/delete/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.ExperimentDeleteManyView.as_view()),
    re_path(r'^{}/{}/experiments/{}/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentDetailView.as_view()),
    re_path(r'^{}/{}/experiments/{}/archive/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentArchiveView.as_view()),
    re_path(r'^{}/{}/experiments/{}/restore/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentRestoreView.as_view()),
    re_path(r'^{}/{}/experiments/{}/restart/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentRestartView.as_view()),
    re_path(r'^{}/{}/experiments/{}/resume/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentResumeView.as_view()),
    re_path(r'^{}/{}/experiments/{}/copy/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentCopyView.as_view()),
    re_path(r'^{}/{}/experiments/{}/coderef/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentCodeReferenceView.as_view()),
    re_path(r'^{}/{}/experiments/{}/statuses/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentStatusListView.as_view()),
    re_path(r'^{}/{}/experiments/{}/statuses/{}/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN, UUID_PATTERN),
        views.ExperimentStatusDetailView.as_view()),
    re_path(r'^{}/{}/experiments/{}/metrics/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentMetricListView.as_view()),
    re_path(r'^{}/{}/experiments/{}/chartviews/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentChartViewListView.as_view()),
    re_path(r'^{}/{}/experiments/{}/chartviews/{}/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN, ID_PATTERN),
        views.ExperimentChartViewDetailView.as_view()),
    re_path(r'^{}/{}/experiments/{}/jobs/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentJobListView.as_view()),
    re_path(r'^{}/{}/experiments/{}/logs/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentLogsView.as_view()),
    re_path(r'^{}/{}/experiments/{}/stop/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentStopView.as_view()),
    re_path(r'^{}/{}/experiments/{}/outputs/download/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentDownloadOutputsView.as_view()),
    re_path(r'^{}/{}/experiments/{}/outputs/tree/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentOutputsTreeView.as_view()),
    re_path(r'^{}/{}/experiments/{}/outputs/files/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentOutputsFilesView.as_view()),
    re_path(r'^{}/{}/experiments/{}/bookmark/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        bookmark_views.ExperimentBookmarkCreateView.as_view()),
    re_path(r'^{}/{}/experiments/{}/unbookmark/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        bookmark_views.ExperimentBookmarkDeleteView.as_view()),
    re_path(r'^{}/{}/experiments/{}/token/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentEphemeralTokenView.as_view()),  # TODO: deprecate until v0.5
    re_path(r'^{}/{}/experiments/{}/ephemeraltoken/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentEphemeralTokenView.as_view()),
    re_path(r'^{}/{}/experiments/{}/imporsonatetoken/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentImpersonateTokenView.as_view()),
    re_path(r'^{}/{}/experiments/{}/_heartbeat/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.ExperimentHeartBeatView.as_view()),
]

jobs_urlpatterns = [
    re_path(r'^{}/{}/experiments/{}/jobs/{}/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN, JOB_ID_PATTERN),
        views.ExperimentJobDetailView.as_view()),
    re_path(r'^{}/{}/experiments/{}/jobs/{}/statuses/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN, JOB_ID_PATTERN),
        views.ExperimentJobStatusListView.as_view()),
    re_path(r'^{}/{}/experiments/{}/jobs/{}/logs/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN, JOB_ID_PATTERN),
        views.ExperimentJobLogsView.as_view()),
    re_path(r'^{}/{}/experiments/{}/jobs/{}/statuses/{}/?$'.format(
        OWNER_NAME_PATTERN,
        PROJECT_NAME_PATTERN,
        EXPERIMENT_ID_PATTERN,
        JOB_ID_PATTERN,
        UUID_PATTERN),
        views.ExperimentJobStatusDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(experiments_urlpatterns + jobs_urlpatterns)
