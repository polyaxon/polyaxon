from administration.register.abstract_job import JobStatusAdmin
from administration.register.utils import DiffModelAdmin, JobLightAdmin
from db.models.jobs import Job, JobStatus


def register_light(admin_register):
    admin_register(Job, JobLightAdmin)


class JobAdmin(DiffModelAdmin):
    pass


def register(admin_register):
    admin_register(Job, JobAdmin)
    admin_register(JobStatus, JobStatusAdmin)
