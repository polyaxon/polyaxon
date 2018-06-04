import logging

from db.models.build_jobs import BuildJob

_logger = logging.getLogger('polyaxon.db')


def get_valid_build_job(build_job_id=None, build_job_uuid=None):
    if not any([build_job_id, build_job_uuid]) or all([build_job_id, build_job_uuid]):
        raise ValueError('`get_valid_build_job` function expects an build_job id or uuid.')

    try:
        if build_job_uuid:
            build_job = BuildJob.objects.get(uuid=build_job_uuid)
        else:
            build_job = BuildJob.objects.get(id=build_job_id)
    except BuildJob.DoesNotExist:
        _logger.info('Experiment id `%s` does not exist', build_job_id)
        return None

    return build_job


def is_build_job_still_running(build_job_id=None, build_job_uuid=None):
    build_job = get_valid_build_job(build_job_id=build_job_id, build_job_uuid=build_job_uuid)

    if not build_job or not build_job.is_running:
        return False

    return True
