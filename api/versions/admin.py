# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib import admin

from versions.models import CliVersion, LibVersion, PlatformVersion, ChartVersion

admin.site.register(CliVersion)
admin.site.register(LibVersion)
admin.site.register(PlatformVersion)
admin.site.register(ChartVersion)
