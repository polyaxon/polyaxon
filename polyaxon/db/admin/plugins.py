from django.contrib import admin

from db.admin.abstract_job import JobStatusAdmin
from db.admin.utils import DiffModelAdmin
from db.models.plugins import NotebookJob, NotebookJobStatus, TensorboardJob, TensorboardJobStatus


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
