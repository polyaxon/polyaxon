from administration.register.abstract_job import JobStatusAdmin
from administration.register.utils import DiffModelAdmin, JobLightAdmin
from db.models.tensorboards import TensorboardJob, TensorboardJobStatus


def register_light(admin_register):
    admin_register(TensorboardJob, JobLightAdmin)


class TensorboardJobAdmin(DiffModelAdmin):
    pass


class TensorboardJobStatusAdmin(JobStatusAdmin):
    pass


def register(admin_register):
    admin_register(TensorboardJob, TensorboardJobAdmin)
    admin_register(TensorboardJobStatus, TensorboardJobStatusAdmin)
