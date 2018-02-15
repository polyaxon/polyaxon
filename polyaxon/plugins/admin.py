# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib import admin

from plugins.models import TensorboardJob, NotebookJob


class TensorboardJobAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


class NotebookJobAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(TensorboardJob, TensorboardJobAdmin)
admin.site.register(NotebookJob, NotebookJobAdmin)
