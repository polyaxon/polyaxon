# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

urlpatterns = [
    url(r'^admin', include(admin.site.urls)),
    url(r'^v1/api/', include('core.urls', namespace='v1')),
    url(r'^.*$', IndexView.as_view(), name='index'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
