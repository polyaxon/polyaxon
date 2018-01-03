# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib import admin

from projects.models import Project, ExperimentGroup

admin.site.register(Project)
admin.site.register(ExperimentGroup)
