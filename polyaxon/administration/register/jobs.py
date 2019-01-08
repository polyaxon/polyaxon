from administration.register.abstract_job import JobStatusAdmin
from administration.register.utils import DiffModelAdmin
from db.models.jobs import Job, JobStatus


class JobAdmin(DiffModelAdmin):
    pass


def register(admin_register):
    admin_register(Job, JobAdmin)
    admin_register(JobStatus, JobStatusAdmin)
