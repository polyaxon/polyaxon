from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, re_path
from django.views.generic import RedirectView

from polyaxon.views import (
    Handler50xView,
    Handler403View,
    Handler404View,
    HealthView,
    IndexView,
    ReactIndexView
)
from users.views import LogoutView

API_V1 = 'api/v1'

api_patterns = [
    re_path(r'', include(
        ('commands.urls', 'commands'), namespace='commands')),
    re_path(r'', include(
        ('versions.urls', 'versions'), namespace='versions')),
    re_path(r'', include(
        ('users.api_urls', 'users'), namespace='users')),
]

if settings.DEPLOY_RUNNER:
    api_patterns += [
        re_path(r'', include(
            ('runner.nodes.urls', 'nodes'), namespace='nodes')),
        # always include project related urls last because of the used patterns
        re_path(r'', include(
            ('runner.urls.experiments', 'experiments'), namespace='experiments')),
        re_path(r'', include(
            ('runner.urls.experiment_groups', 'experiment_groups'), namespace='experiment_groups')),
        re_path(r'', include(
            ('plugins.api_urls', 'plugins'), namespace='plugins')),
    ]

api_patterns += [
    # always include project related urls last because of the used patterns
    re_path(r'', include(
        ('experiments.urls', 'experiments'), namespace='runner_experiments')),
    re_path(r'', include(
        ('experiment_groups.urls', 'experiment_groups'), namespace='runner_experiment_groups')),
    re_path(r'', include(
        ('repos.urls', 'repos'), namespace='repos')),
    re_path(r'', include(
        ('projects.urls', 'projects'), namespace='projects')),
]

urlpatterns = [
    re_path(r'', include(
        ('plugins.urls', 'plugins'), namespace='plugins')),
    re_path(r'^users/', include(
        ('users.urls', 'users'), namespace='users')),
    re_path(r'^oauth/', include(
        ('sso.urls', 'sso'), namespace='sso')),
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

handler400 = Handler50xView.as_view()
handler403 = Handler403View.as_view()
handler404 = Handler404View.as_view()
handler500 = Handler50xView.as_view()

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
