from django.core.exceptions import ValidationError

from db.models.jobs import Job
from streams.validation.project import validate_project


def validate_job(request, username, project_name, job_id):
    project, message = validate_project(request=request,
                                        username=username,
                                        project_name=project_name)
    if project is None:
        return None, message
    try:
        job = Job.objects.get(project=project, id=job_id)
    except (Job.DoesNotExist, ValidationError):
        return None, 'Job was not found'
    if job.is_done:
        return None, 'Experiment is not running, current status: {}'.format(
            job.last_status
        )
    return job, None
