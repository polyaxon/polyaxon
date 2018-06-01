import logging

from db.models.projects import Project

_logger = logging.getLogger('polyaxon.db')


def get_valid_project(project_id=None, project_uuid=None):
    if not any([project_id, project_uuid]) or all([project_id, project_uuid]):
        raise ValueError('`get_valid_project` function expects an project id or uuid.')

    try:
        if project_uuid:
            project = Project.objects.get(uuid=project_uuid)
        else:
            project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        _logger.info('Project id `%s` does not exist', project_id)
        return None

    return project
