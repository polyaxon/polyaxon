from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.plugins import views
from constants.urls import EXPERIMENT_ID_PATTERN, GROUP_ID_PATTERN, NAME_PATTERN, USERNAME_PATTERN

projects_urlpatterns = [
    re_path(r'^{}/{}/tensorboard/start/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.StartTensorboardView.as_view()),
    re_path(r'^{}/{}/experiments/{}/tensorboard/start/?$'.format(USERNAME_PATTERN,
                                                                 NAME_PATTERN,
                                                                 EXPERIMENT_ID_PATTERN),
            views.StartTensorboardView.as_view()),
    re_path(r'^{}/{}/groups/{}/tensorboard/start/?$'.format(USERNAME_PATTERN,
                                                            NAME_PATTERN,
                                                            GROUP_ID_PATTERN),
            views.StartTensorboardView.as_view()),
    re_path(r'^{}/{}/tensorboard/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.StopTensorboardView.as_view()),
    re_path(r'^{}/{}/experiments/{}/tensorboard/stop/?$'.format(USERNAME_PATTERN,
                                                                NAME_PATTERN,
                                                                EXPERIMENT_ID_PATTERN),
            views.StopTensorboardView.as_view()),
    re_path(r'^{}/{}/groups/{}/tensorboard/stop/?$'.format(USERNAME_PATTERN,
                                                           NAME_PATTERN,
                                                           GROUP_ID_PATTERN),
            views.StopTensorboardView.as_view()),
    re_path(r'^{}/{}/notebook/start/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.StartNotebookView.as_view()),
    re_path(r'^{}/{}/notebook/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.StopNotebookView.as_view()),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(projects_urlpatterns)
