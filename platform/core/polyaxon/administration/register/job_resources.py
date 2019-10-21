from db.models.job_resources import JobResources


def register(admin_register):
    admin_register(JobResources)
