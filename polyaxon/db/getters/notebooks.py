import logging

from db.models.notebooks import NotebookJob

_logger = logging.getLogger('polyaxon.db')


def get_valid_notebook(notebook_job_id=None, notebook_job_uuid=None):
    exists_cond = (not any([notebook_job_id, notebook_job_uuid])
                   or all([notebook_job_id, notebook_job_uuid]))
    if exists_cond:
        raise ValueError('`get_valid_project` function expects an project id or uuid.')

    try:
        if notebook_job_uuid:
            notebook_job = NotebookJob.objects.get(uuid=notebook_job_uuid)
        else:
            notebook_job = NotebookJob.objects.get(id=notebook_job_id)
    except NotebookJob.DoesNotExist:
        _logger.info('Notebook `%s` does not exist', notebook_job_id or notebook_job_uuid)
        return None

    return notebook_job
