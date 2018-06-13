from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, re_path
from django.views.generic import RedirectView

from api.index.views import (  # noqa
    Handler50xView,
    Handler403View,
    Handler404View,
    HealthView,
    IndexView,
    ReactIndexView
)
from api.users.views import LogoutView
from constants.urls import API_V1

api_patterns = [
    re_path(r'', include(
        ('api.clusters.urls', 'clusters'), namespace='clusters')),
    re_path(r'', include(
        ('api.versions.urls', 'versions'), namespace='versions')),
    re_path(r'', include(
        ('api.users.api_urls', 'users'), namespace='users')),
]

api_patterns += [
    re_path(r'', include(
        ('api.nodes.urls', 'nodes'), namespace='nodes')),
    # always include project related urls last because of the used patterns
    re_path(r'', include(
        ('api.jobs.urls', 'jobs'), namespace='jobs')),
    re_path(r'', include(
        ('api.builds.urls', 'builds'), namespace='builds')),
    re_path(r'', include(
        ('api.experiments.urls', 'experiments'), namespace='experiments')),
    re_path(r'', include(
        ('api.experiment_groups.urls', 'experiment_groups'), namespace='experiment_groups')),
    re_path(r'', include(
        ('api.plugins.api_urls', 'plugins'), namespace='plugins')),
    re_path(r'', include(
        ('api.repos.urls', 'repos'), namespace='repos')),
    re_path(r'', include(
        ('api.projects.urls', 'projects'), namespace='projects')),
]

urlpatterns = [
    re_path(r'', include(
        ('api.plugins.urls', 'plugins'), namespace='plugins')),
    re_path(r'^users/', include(
        ('api.users.urls', 'users'), namespace='users')),
    re_path(r'^oauth/', include(
        ('api.oauth.urls', 'oauth'), namespace='oauth')),
    re_path(r'^_admin/logout/$', LogoutView.as_view(), name='logout'),
    re_path(r'^_admin/login/$',
            RedirectView.as_view(url=settings.LOGIN_URL, permanent=True, query_string=True),
            name='login'),

    re_path(r'^_admin/', admin.site.urls),
    re_path(r'^_health/?$', HealthView.as_view(), name='health_check'),
    re_path(r'^{}/'.format(API_V1), include((api_patterns, 'v1'), namespace='v1')),
    re_path(r'^$', IndexView.as_view(), name='index'),
    re_path(r'^^50x.html$', Handler50xView.as_view(), name='50x'),
    re_path(r'^app.*/?', login_required(ReactIndexView.as_view()), name='react-index'),
]
