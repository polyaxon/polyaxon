from administration.register.utils import DiffModelAdmin
from db.models.projects import Project


class ProjectAdmin(DiffModelAdmin):
    pass


def register(admin_register):
    admin_register(Project, ProjectAdmin)
