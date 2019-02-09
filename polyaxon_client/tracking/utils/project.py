# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.exceptions import PolyaxonClientException


def get_project_info(current_user, project):
    if not project:
        raise PolyaxonClientException('You need to provide a project to do tracking.')
    parts = project.replace('.', '/').split('/')
    if len(parts) == 2:
        user, project_name = parts
    else:
        user = current_user
        project_name = project

    return user, project_name
