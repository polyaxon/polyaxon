# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib import admin

from versions.models import CliVersion

admin.site.register(CliVersion)
