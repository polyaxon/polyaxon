from db.models.jobs import Job

jobs = Job.objects.select_related(
    'user',
    'project',
    'project__user',
    'build_job',
    'build_job__project',
    'build_job__project__user',
    'status')

jobs_details = jobs.select_related('original_job')
