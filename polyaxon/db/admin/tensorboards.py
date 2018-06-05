from django.contrib import admin

from db.admin.abstract_job import JobStatusAdmin
from db.admin.utils import DiffModelAdmin
from db.models.tensorboards import TensorboardJob, TensorboardJobStatus


class TensorboardJobAdmin(DiffModelAdmin):
    pass


class TensorboardJobStatusAdmin(JobStatusAdmin):
    pass


admin.site.register(TensorboardJob, TensorboardJobAdmin)
admin.site.register(TensorboardJobStatus, TensorboardJobStatusAdmin)
