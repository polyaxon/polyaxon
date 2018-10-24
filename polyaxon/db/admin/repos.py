from django.contrib import admin

from db.models.repos import CodeReference, Repo


class RepoAdmin(admin.ModelAdmin):
    readonly_fields = ('project', 'path',)


admin.site.register(Repo, RepoAdmin)
admin.site.register(CodeReference)
