from django.contrib import admin

from libs.admin import DiffModelAdmin
from projects.models import Project


class ProjectAdmin(DiffModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
