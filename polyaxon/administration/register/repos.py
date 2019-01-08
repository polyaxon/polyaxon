from django.contrib import admin

from db.models.repos import CodeReference, Repo


class RepoAdmin(admin.ModelAdmin):
    readonly_fields = ('project', 'path',)


def register(admin_register):
    admin_register(Repo, RepoAdmin)
    admin_register(CodeReference)
