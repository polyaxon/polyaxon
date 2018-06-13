from django.contrib import admin

from db.admin.abstract_job import JobStatusAdmin
from db.admin.utils import DiffModelAdmin
from db.models.jobs import Job, JobStatus


class JobAdmin(DiffModelAdmin):
    pass


admin.site.register(Job, JobAdmin)
admin.site.register(JobStatus, JobStatusAdmin)
