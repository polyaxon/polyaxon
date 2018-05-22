from django.contrib import admin

from admin.jobs import JobStatusAdmin
from libs.admin import DiffModelAdmin
from models.plugins import NotebookJob, NotebookJobStatus, TensorboardJob, TensorboardJobStatus


class TensorboardJobAdmin(DiffModelAdmin):
    pass


class NotebookJobAdmin(DiffModelAdmin):
    pass


class TensorboardJobStatusAdmin(JobStatusAdmin):
    pass


class NotebookJobStatusAdmin(JobStatusAdmin):
    pass


admin.site.register(TensorboardJob, TensorboardJobAdmin)
admin.site.register(NotebookJob, NotebookJobAdmin)
admin.site.register(TensorboardJobStatus, TensorboardJobStatusAdmin)
admin.site.register(NotebookJobStatus, NotebookJobStatusAdmin)
