from django.contrib import admin

from repos.models import ExternalRepo, Repo


class RepoAdmin(admin.ModelAdmin):
    readonly_fields = ('project', 'path', 'git', 'last_commit',)


class ExternalRepoAdmin(admin.ModelAdmin):
    readonly_fields = ('project', 'name', 'git_url', 'path', 'git', 'last_commit',)


admin.site.register(Repo, RepoAdmin)
admin.site.register(ExternalRepo, ExternalRepoAdmin)
