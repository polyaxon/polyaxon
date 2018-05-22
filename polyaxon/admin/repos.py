from django.contrib import admin

from models.repos import ExternalRepo, Repo


class RepoAdmin(admin.ModelAdmin):
    readonly_fields = ('project', 'path',)


class ExternalRepoAdmin(admin.ModelAdmin):
    readonly_fields = ('project', 'name', 'git_url', 'path',)


admin.site.register(Repo, RepoAdmin)
admin.site.register(ExternalRepo, ExternalRepoAdmin)
