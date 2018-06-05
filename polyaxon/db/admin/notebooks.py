from django.contrib import admin

from db.admin.abstract_job import JobStatusAdmin
from db.admin.utils import DiffModelAdmin
from db.models.notebooks import NotebookJob, NotebookJobStatus


class NotebookJobAdmin(DiffModelAdmin):
    pass


class NotebookJobStatusAdmin(JobStatusAdmin):
    pass


admin.site.register(NotebookJob, NotebookJobAdmin)
admin.site.register(NotebookJobStatus, NotebookJobStatusAdmin)
