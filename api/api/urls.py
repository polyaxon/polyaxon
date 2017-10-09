# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework.authtoken.views import obtain_auth_token


class IndexView(TemplateView):
    template_name = "api/index.html"

urlpatterns = [
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/token/', obtain_auth_token),
    url(r'^v1/api/', include('projects.urls', namespace='projects_v1')),
    url(r'^$', IndexView.as_view(), name='index'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
