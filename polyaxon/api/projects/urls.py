from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.experiment_groups import views as groups_views
from api.experiments import views as experiments_views
from api.jobs import views as jobs_views
from api.projects import views
from constants.urls import NAME_PATTERN, USERNAME_PATTERN

projects_urlpatterns = [
    re_path(r'^projects/?$',
            views.ProjectCreateView.as_view()),
    re_path(r'^{}/?$'.format(USERNAME_PATTERN),
            views.ProjectListView.as_view()),
    re_path(r'^{}/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.ProjectDetailView.as_view()),
    re_path(r'^{}/{}/groups/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            groups_views.ExperimentGroupListView.as_view()),
    re_path(r'^{}/{}/experiments/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            experiments_views.ProjectExperimentListView.as_view()),
    re_path(r'^{}/{}/jobs/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            jobs_views.ProjectJobListView.as_view()),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(projects_urlpatterns)
