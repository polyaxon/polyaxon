# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib import admin

from experiments.models import Experiment, ExperimentStatus, ExperimentJob, ExperimentJobStatus


class ExperimentAdmin(admin.ModelAdmin):
    readonly_fields = (
        'sequence', 'unique_name', 'last_status', 'last_status', 'created_at', 'updated_at')


class ExperimentStatusAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


class ExperimentMetricAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


class ExperimentJobAdmin(admin.ModelAdmin):
    readonly_fields = ('sequence', 'unique_name', 'last_status', 'created_at', 'updated_at')


class ExperimentJobStatusAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(ExperimentStatus, ExperimentStatusAdmin)
admin.site.register(ExperimentStatus, ExperimentMetricAdmin)
admin.site.register(ExperimentJob, ExperimentJobAdmin)
admin.site.register(ExperimentJobStatus, ExperimentJobStatusAdmin)
