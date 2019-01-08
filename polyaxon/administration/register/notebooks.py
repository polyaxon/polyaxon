from administration.register.abstract_job import JobStatusAdmin
from administration.register.utils import DiffModelAdmin
from db.models.notebooks import NotebookJob, NotebookJobStatus


class NotebookJobAdmin(DiffModelAdmin):
    pass


class NotebookJobStatusAdmin(JobStatusAdmin):
    pass


def register(admin_register):
    admin_register(NotebookJob, NotebookJobAdmin)
    admin_register(NotebookJobStatus, NotebookJobStatusAdmin)
