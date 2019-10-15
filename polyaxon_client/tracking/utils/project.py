# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.exceptions import PolyaxonClientException


def get_project_info(project, owner=None):
    if not project:
        raise PolyaxonClientException("You need to provide a project to do tracking.")
    parts = project.replace(".", "/").split("/")
    if len(parts) == 2:
        owner, project_name = parts
    else:
        project_name = project

    return owner, project_name
