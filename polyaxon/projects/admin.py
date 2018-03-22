from django.contrib import admin

from projects.models import Project, ExperimentGroup


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


class ExperimentGroupAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Project, ProjectAdmin)
admin.site.register(ExperimentGroup, ExperimentGroupAdmin)
