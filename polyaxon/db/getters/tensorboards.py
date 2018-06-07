import logging

from db.models.tensorboards import TensorboardJob

_logger = logging.getLogger('polyaxon.db')


def get_valid_tensorboard(tensorboard_job_id=None, tensorboard_job_uuid=None):
    exists_cond = (not any([tensorboard_job_id, tensorboard_job_uuid])
                   or all([tensorboard_job_id, tensorboard_job_uuid]))
    if exists_cond:
        raise ValueError('`get_valid_project` function expects an project id or uuid.')

    try:
        if tensorboard_job_uuid:
            tensorboard_job = TensorboardJob.objects.get(uuid=tensorboard_job_uuid)
        else:
            tensorboard_job = TensorboardJob.objects.get(id=tensorboard_job_id)
    except TensorboardJob.DoesNotExist:
        _logger.info('Tensorboard id `%s` does not exist',
                     tensorboard_job_id or tensorboard_job_uuid)
        return None

    return tensorboard_job
