from django.contrib import admin

from db.models.repos import CodeReference, ExternalRepo, Repo


class RepoAdmin(admin.ModelAdmin):
    readonly_fields = ('project', 'path',)


class ExternalRepoAdmin(admin.ModelAdmin):
    readonly_fields = ('project', 'name', 'git_url', 'path',)


def register(admin_register):
    admin_register(Repo, RepoAdmin)
    admin.site.register(ExternalRepo, ExternalRepoAdmin)
    admin_register(CodeReference)
