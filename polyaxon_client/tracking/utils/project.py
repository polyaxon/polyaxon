# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


def get_project_info(current_user, project):
    parts = project.replace('.', '/').split('/')
    if len(parts) == 2:
        user, project_name = parts
    else:
        user = current_user
        project_name = project

    return user, project_name
