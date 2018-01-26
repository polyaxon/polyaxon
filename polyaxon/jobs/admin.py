# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib import admin

from jobs.models import JobResources


class JobStatusAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


admin.site.register(JobResources)
