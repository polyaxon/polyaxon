# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from polyaxon.views import (
    Handler404View,
    Handler403View,
    HealthView,
    IndexView,
    ReactIndexView,
    Handler50xView)
from users.views import LogoutView, LoginView

API_V1 = 'api/v1'

api_patterns = [
    url(r'', include('clusters.urls', namespace='clusters')),
    url(r'', include('versions.urls', namespace='versions')),
    url(r'', include('users.api_urls', namespace='users')),
    # always include project last because of it's patterns
    url(r'', include('experiments.urls', namespace='experiments')),
    url(r'', include('repos.urls', namespace='repos')),
    url(r'', include('projects.urls', namespace='projects')),
]

urlpatterns = [
    url(r'', include('plugins.urls', namespace='plugins')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^_admin/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^_admin/login/$', LoginView.as_view(template_name='admin/login.html'), name='login'),
    url(r'^_admin/', include(admin.site.urls)),
    url(r'^_health/?$', HealthView.as_view(), name='health_check'),
    url(r'^{}/'.format(API_V1), include(api_patterns, namespace='v1')),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^^50x.html$', Handler50xView.as_view(), name='50x'),
    url(r'^app.*/?', ReactIndexView.as_view(), name='react-index'),
]

handler400 = Handler50xView.as_view()
handler403 = Handler403View.as_view()
handler404 = Handler404View.as_view()
handler500 = Handler50xView.as_view()

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
