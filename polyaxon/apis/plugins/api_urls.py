from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from apis.plugins import views
from constants.urls import NAME_PATTERN, USERNAME_PATTERN

projects_urlpatterns = [
    re_path(r'^{}/{}/tensorboard/start/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.StartTensorboardView.as_view()),
    re_path(r'^{}/{}/tensorboard/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.StopTensorboardView.as_view()),
    re_path(r'^{}/{}/notebook/start/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.StartNotebookView.as_view()),
    re_path(r'^{}/{}/notebook/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.StopNotebookView.as_view()),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(projects_urlpatterns)
