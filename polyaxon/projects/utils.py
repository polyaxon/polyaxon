import logging

from models.projects import Project

logger = logging.getLogger('polyaxon.projects.utils')


def get_valid_project(project_id):
    try:
        return Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        logger.info('Project id `%s` does not exist', project_id)
        return None
