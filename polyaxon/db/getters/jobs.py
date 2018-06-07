import logging

from db.models.jobs import Job

_logger = logging.getLogger('polyaxon.db')


def get_valid_job(job_id=None, job_uuid=None):
    if not any([job_id, job_uuid]) or all([job_id, job_uuid]):
        raise ValueError('`get_valid_job` function expects an job id or uuid.')

    try:
        if job_uuid:
            job = Job.objects.get(uuid=job_uuid)
        else:
            job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        _logger.info('Job `%s` does not exist', job_id or job_uuid)
        return None

    return job


def is_job_still_running(job_id=None, job_uuid=None):
    job = get_valid_job(job_id=job_id, job_uuid=job_uuid)

    if not job or not job.is_running:
        return False

    return True
