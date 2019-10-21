import logging

from db.models.notebooks import NotebookJob

_logger = logging.getLogger('polyaxon.db')


def get_valid_notebook(notebook_job_id: int = None,
                       notebook_job_uuid: str = None,
                       include_deleted: bool = False):
    exists_cond = (not any([notebook_job_id, notebook_job_uuid])
                   or all([notebook_job_id, notebook_job_uuid]))
    if exists_cond:
        raise ValueError('`get_valid_notebook` function expects a notebook id or uuid.')

    try:
        qs = NotebookJob.all if include_deleted else NotebookJob.objects
        if notebook_job_uuid:
            notebook_job = qs.get(uuid=notebook_job_uuid)
        else:
            notebook_job = qs.get(id=notebook_job_id)
    except NotebookJob.DoesNotExist:
        _logger.info('Notebook `%s` does not exist', notebook_job_id or notebook_job_uuid)
        return None

    return notebook_job
