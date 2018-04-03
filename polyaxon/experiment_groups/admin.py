from django.contrib import admin

from experiment_groups.models import ExperimentGroup


class ExperimentGroupAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(ExperimentGroup, ExperimentGroupAdmin)
