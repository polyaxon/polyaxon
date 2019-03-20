from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.plugins import views
from constants.urls import (
    EXPERIMENT_ID_PATTERN,
    GROUP_ID_PATTERN,
    JOB_ID_PATTERN,
    OWNER_NAME_PATTERN,
    PROJECT_NAME_PATTERN
)

projects_urlpatterns = [
    re_path(r'^{}/{}/tensorboard/start/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.StartTensorboardView.as_view()),
    re_path(r'^{}/{}/experiments/{}/tensorboard/start/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.StartTensorboardView.as_view()),
    re_path(r'^{}/{}/groups/{}/tensorboard/start/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN),
        views.StartTensorboardView.as_view()),
    re_path(r'^{}/{}/tensorboard/stop/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.StopTensorboardView.as_view()),
    re_path(r'^{}/{}/experiments/{}/tensorboard/stop/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.StopTensorboardView.as_view()),
    re_path(r'^{}/{}/groups/{}/tensorboard/stop/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN),
        views.StopTensorboardView.as_view()),
    re_path(r'^{}/{}/tensorboards/{}/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.TensorboardDetailView.as_view()),
    re_path(r'^{}/{}/tensorboards/{}/archive/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.TensorboardArchiveView.as_view()),
    re_path(r'^{}/{}/tensorboards/{}/restore/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.TensorboardRestoreView.as_view()),
    re_path(r'^{}/{}/tensorboards/{}/stop/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.StopTensorboardJobView.as_view()),
    re_path(r'^{}/{}/tensorboards/{}/statuses/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.TensorboardStatusListView.as_view()),
    re_path(r'^{}/{}/notebook/start/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.StartNotebookView.as_view()),
    re_path(r'^{}/{}/notebook/stop/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.StopNotebookView.as_view()),
    re_path(r'^{}/{}/notebook/imporsonatetoken/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.NotebookImpersonateTokenView.as_view()),
    re_path(r'^{}/{}/notebooks/{}/archive/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.NotebookArchiveView.as_view()),
    re_path(r'^{}/{}/notebooks/{}/restore/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.NotebookRestoreView.as_view()),
    re_path(r'^{}/{}/notebooks/{}/stop/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.StopNotebookView.as_view()),
    re_path(r'^{}/{}/notebooks/{}/statuses/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.NotebookStatusListView.as_view()),
    re_path(r'^{}/{}/notebooks/{}/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, JOB_ID_PATTERN),
        views.NotebookDetailView.as_view()),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(projects_urlpatterns)
