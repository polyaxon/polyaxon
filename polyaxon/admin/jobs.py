from django.contrib import admin

from models.jobs import JobResources


class JobStatusAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


admin.site.register(JobResources)
