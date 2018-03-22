from django.contrib import admin

from jobs.admin import JobStatusAdmin
from plugins.models import TensorboardJob, NotebookJob, TensorboardJobStatus, NotebookJobStatus


class TensorboardJobAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


class NotebookJobAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


class TensorboardJobStatusAdmin(JobStatusAdmin):
    pass


class NotebookJobStatusAdmin(JobStatusAdmin):
    pass


admin.site.register(TensorboardJob, TensorboardJobAdmin)
admin.site.register(NotebookJob, NotebookJobAdmin)
admin.site.register(TensorboardJobStatus, TensorboardJobStatusAdmin)
admin.site.register(NotebookJobStatus, NotebookJobStatusAdmin)
