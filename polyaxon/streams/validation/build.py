from django.core.exceptions import ValidationError

from db.models.build_jobs import BuildJob
from streams.validation.project import validate_project


def validate_build(request, username, project_name, build_id):
    project, message = validate_project(request=request,
                                        username=username,
                                        project_name=project_name)
    if project is None:
        return None, message
    try:
        job = BuildJob.objects.get(project=project, id=build_id)
    except (BuildJob.DoesNotExist, ValidationError):
        return None, 'Build was not found'
    if job.is_done:
        return None, 'Job is not running, current status: {}'.format(
            job.last_status
        )
    return job, None


def get_build_job(build_id):
    try:
        job = BuildJob.objects.get(id=build_id)
    except (BuildJob.DoesNotExist, ValidationError):
        return None, 'Build was not found'
    if job.is_done:
        return None, 'Job is not running, current status: {}'.format(
            job.last_status
        )
    return job, None
