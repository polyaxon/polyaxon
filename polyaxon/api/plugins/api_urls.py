from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.plugins import views
from constants.urls import (
    EXPERIMENT_ID_PATTERN,
    GROUP_ID_PATTERN,
    OWNER_NAME_PATTERN,
    PROJECT_NAME_PATTERN
)

projects_urlpatterns = [
    re_path(r'^{}/{}/tensorboard/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.TensorboardDetailView.as_view()),
    re_path(r'^{}/{}/experiments/{}/tensorboard/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.TensorboardDetailView.as_view()),
    re_path(r'^{}/{}/groups/{}/tensorboard/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN),
        views.TensorboardDetailView.as_view()),
    re_path(r'^{}/{}/tensorboard/archive/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
        views.TensorboardArchiveView.as_view()),
    re_path(r'^{}/{}/experiments/{}/tensorboard/archive/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.TensorboardArchiveView.as_view()),
    re_path(r'^{}/{}/groups/{}/tensorboard/archive/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN),
        views.TensorboardArchiveView.as_view()),
    re_path(r'^{}/{}/tensorboard/restore/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
        views.TensorboardRestoreView.as_view()),
    re_path(r'^{}/{}/experiments/{}/tensorboard/restore/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.TensorboardRestoreView.as_view()),
    re_path(r'^{}/{}/groups/{}/tensorboard/restore/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN),
        views.TensorboardRestoreView.as_view()),
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
    re_path(r'^{}/{}/tensorboard/statuses/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.TensorboardStatusListView.as_view()),
    re_path(r'^{}/{}/experiments/{}/tensorboard/statuses/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, EXPERIMENT_ID_PATTERN),
        views.TensorboardStatusListView.as_view()),
    re_path(r'^{}/{}/groups/{}/tensorboard/statuses/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN),
        views.TensorboardStatusListView.as_view()),
    re_path(r'^{}/{}/notebook/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.NotebookDetailView.as_view()),
    re_path(r'^{}/{}/notebook/archive/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
        views.NotebookArchiveView.as_view()),
    re_path(r'^{}/{}/notebook/restore/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
        views.NotebookRestoreView.as_view()),
    re_path(r'^{}/{}/notebook/start/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.StartNotebookView.as_view()),
    re_path(r'^{}/{}/notebook/stop/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.StopNotebookView.as_view()),
    re_path(r'^{}/{}/notebook/statuses/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.NotebookStatusListView.as_view()),
    re_path(r'^{}/{}/notebook/imporsonatetoken/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.NotebookImpersonateTokenView.as_view()),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(projects_urlpatterns)
