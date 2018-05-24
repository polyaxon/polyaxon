import logging

from db.models.projects import Project

_logger = logging.getLogger('polyaxon.db')


def get_valid_project(project_id):
    try:
        return Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        _logger.info('Project id `%s` does not exist', project_id)
        return None
