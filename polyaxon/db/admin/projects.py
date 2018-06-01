from django.contrib import admin

from db.admin.utils import DiffModelAdmin
from db.models.projects import Project


class ProjectAdmin(DiffModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
