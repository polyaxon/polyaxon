from django.contrib import admin

from libs.admin import DiffModelAdmin
from db.models.projects import Project


class ProjectAdmin(DiffModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
