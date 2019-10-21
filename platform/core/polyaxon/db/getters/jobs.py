import logging

from db.models.jobs import Job

_logger = logging.getLogger('polyaxon.db')


def get_valid_job(job_id: int = None,
                  job_uuid: str = None,
                  include_deleted: bool = False):
    if not any([job_id, job_uuid]) or all([job_id, job_uuid]):
        raise ValueError('`get_valid_job` function expects an job id or uuid.')

    try:
        qs = Job.all if include_deleted else Job.objects
        if job_uuid:
            job = qs.get(uuid=job_uuid)
        else:
            job = qs.get(id=job_id)
    except Job.DoesNotExist:
        _logger.info('Job `%s` does not exist', job_id or job_uuid)
        return None

    return job


def is_job_still_running(job_id: int = None,
                         job_uuid: str = None):
    job = get_valid_job(job_id=job_id, job_uuid=job_uuid)

    if not job or not job.is_running:
        return False

    return True
