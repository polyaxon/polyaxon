from administration.register.abstract_job import JobStatusAdmin
from administration.register.utils import DiffModelAdmin
from db.models.tensorboards import TensorboardJob, TensorboardJobStatus


class TensorboardJobAdmin(DiffModelAdmin):
    pass


class TensorboardJobStatusAdmin(JobStatusAdmin):
    pass


def register(admin_register):
    admin_register(TensorboardJob, TensorboardJobAdmin)
    admin_register(TensorboardJobStatus, TensorboardJobStatusAdmin)
