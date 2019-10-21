from administration.register.abstract_job import JobStatusAdmin
from administration.register.utils import DiffModelAdmin, JobLightAdmin
from db.models.notebooks import NotebookJob, NotebookJobStatus


def register_light(admin_register):
    admin_register(NotebookJob, JobLightAdmin)


class NotebookJobAdmin(DiffModelAdmin):
    pass


class NotebookJobStatusAdmin(JobStatusAdmin):
    pass


def register(admin_register):
    admin_register(NotebookJob, NotebookJobAdmin)
    admin_register(NotebookJobStatus, NotebookJobStatusAdmin)
