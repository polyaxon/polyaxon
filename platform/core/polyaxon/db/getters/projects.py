import logging

from db.models.projects import Project

_logger = logging.getLogger('polyaxon.db')


def get_valid_project(project_id: int = None,
                      project_uuid: str = None,
                      include_deleted: bool = False):
    if not any([project_id, project_uuid]) or all([project_id, project_uuid]):
        raise ValueError('`get_valid_project` function expects an project id or uuid.')

    try:
        qs = Project.all if include_deleted else Project.objects
        if project_uuid:
            project = qs.get(uuid=project_uuid)
        else:
            project = qs.get(id=project_id)
    except Project.DoesNotExist:
        _logger.info('Project `%s` does not exist', project_id or project_uuid)
        return None

    return project
