from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from experiment_groups import views as groups_views
from experiments import views as experiments_views
from libs.urls import NAME_PATTERN, USERNAME_PATTERN
from projects import views

projects_urlpatterns = [
    re_path(r'^projects/?$',
            views.ProjectCreateView.as_view()),
    re_path(r'^{}/?$'.format(USERNAME_PATTERN),
            views.ProjectListView.as_view()),
    re_path(r'^{}/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.ProjectDetailView.as_view()),
    re_path(r'^{}/{}/groups/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            groups_views.ExperimentGroupListView.as_view()),
    # Get all experiment under a project
    re_path(r'^{}/{}/experiments/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            experiments_views.ProjectExperimentListView.as_view()),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(projects_urlpatterns)
