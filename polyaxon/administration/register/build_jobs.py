from administration.register.abstract_job import JobStatusAdmin
from administration.register.utils import DiffModelAdmin
from db.models.build_jobs import BuildJob, BuildJobStatus


class BuildJobAdmin(DiffModelAdmin):
    pass


class BuildJobStatusAdmin(JobStatusAdmin):
    pass


def register(admin_register):
    admin_register(BuildJob, BuildJobAdmin)
    admin_register(BuildJobStatus, BuildJobStatusAdmin)
