from django.core.exceptions import ValidationError

from db.models.experiment_jobs import ExperimentJob
from streams.validation.experiment import get_experiment, validate_experiment


def validate_experiment_job(request, username, project_name, experiment_id, job_id):
    experiment, message = validate_experiment(request=request,
                                              username=username,
                                              project_name=project_name,
                                              experiment_id=experiment_id)
    if experiment is None:
        return None, None, message
    try:
        job = ExperimentJob.objects.get(experiment=experiment, id=job_id)
    except (ExperimentJob.DoesNotExist, ValidationError):
        return None, None, 'Experiment job was not found'
    if job.is_done:
        return None, 'Experiment job is not running, current status: {}'.format(
            job.last_status
        )
    return job, experiment, None


def get_experiment_job(experiment_id, job_id):
    experiment, message = get_experiment(experiment_id=experiment_id)
    if experiment is None:
        return None, None, message
    try:
        job = ExperimentJob.objects.get(id=job_id)
    except (ExperimentJob.DoesNotExist, ValidationError):
        return None, None, 'Experiment job was not found'
    if job.is_done:
        return None, 'Experiment job is not running, current status: {}'.format(
            job.last_status
        )
    return job, experiment, None
