from administration.register.utils import DiffModelAdmin
from db.models.projects import Project


class ProjectAdmin(DiffModelAdmin):
    readonly_fields = DiffModelAdmin.readonly_fields + ('name',)
    fields = ('name', 'deleted', 'is_public', 'created_at', 'updated_at')

    def get_queryset(self, request):
        qs = self.model.all.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


def register(admin_register):
    admin_register(Project, ProjectAdmin)
