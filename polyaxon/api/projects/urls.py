from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.bookmarks import views as bookmark_views
from api.build_jobs import views as builds_views
from api.experiment_groups import views as groups_views
from api.experiments import views as experiments_views
from api.jobs import views as jobs_views
from api.plugins import views as tensorboards_views
from api.projects import views
from constants.urls import OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN

projects_urlpatterns = [
    re_path(r'^projects/?$',
            views.ProjectCreateView.as_view()),
    re_path(r'^{}/?$'.format(OWNER_NAME_PATTERN),
            views.ProjectListView.as_view()),
    re_path(r'^{}/{}/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.ProjectDetailView.as_view()),
    re_path(r'^{}/{}/archive/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.ProjectArchiveView.as_view()),
    re_path(r'^{}/{}/restore/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.ProjectRestoreView.as_view()),
    re_path(r'^{}/{}/groups/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            groups_views.ExperimentGroupListView.as_view()),
    re_path(r'^{}/{}/experiments/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            experiments_views.ProjectExperimentListView.as_view()),
    re_path(r'^{}/{}/jobs/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            jobs_views.ProjectJobListView.as_view()),
    re_path(r'^{}/{}/builds/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            builds_views.ProjectBuildListView.as_view()),
    re_path(r'^{}/{}/tensorboards/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            tensorboards_views.ProjectTensorboardListView.as_view()),
    re_path(r'^{}/{}/bookmark/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            bookmark_views.ProjectBookmarkCreateView.as_view()),
    re_path(r'^{}/{}/unbookmark/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            bookmark_views.ProjectBookmarkDeleteView.as_view()),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(projects_urlpatterns)
