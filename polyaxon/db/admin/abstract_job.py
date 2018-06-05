from django.contrib import admin


class JobStatusAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

