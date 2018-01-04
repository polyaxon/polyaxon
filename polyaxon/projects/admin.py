# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib import admin

from projects.models import Project, ExperimentGroup


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


class ExperimentGroupAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Project, ProjectAdmin)
admin.site.register(ExperimentGroup, ExperimentGroupAdmin)
