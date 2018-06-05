from django.contrib import admin

from db.admin.abstract_job import JobStatusAdmin
from db.admin.utils import DiffModelAdmin
from db.models.build_jobs import BuildJob, BuildJobStatus


class BuildJobAdmin(DiffModelAdmin):
    pass


class BuildJobStatusAdmin(JobStatusAdmin):
    pass


admin.site.register(BuildJob, BuildJobAdmin)
admin.site.register(BuildJobStatus, BuildJobStatusAdmin)
