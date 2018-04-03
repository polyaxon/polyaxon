from django.contrib import admin

from projects.models import Project


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Project, ProjectAdmin)
