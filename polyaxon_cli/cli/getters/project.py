# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon_cli.managers.auth import AuthConfigManager
from polyaxon_cli.managers.project import ProjectManager
from polyaxon_cli.utils import constants
from polyaxon_cli.utils.formatting import Printer


def get_project_info(project):
    parts = project.replace('.', '/').split('/')
    if len(parts) == 2:
        user, project_name = parts
    else:
        user = AuthConfigManager.get_value('username')
        project_name = project

    return user, project_name


def get_project_or_local(project=None):
    if not project and not ProjectManager.is_initialized():
        Printer.print_error('Please provide a valid project, or init a new project. '
                            ' {}'.format(constants.INIT_COMMAND))
        sys.exit(1)

    if project:
        user, project_name = get_project_info(project)
    else:
        project = ProjectManager.get_config()
        user, project_name = project.user, project.name

    if not all([user, project_name]):
        Printer.print_error('Please provide a valid project, or init a new project.'
                            ' {}'.format(constants.INIT_COMMAND))
        sys.exit(1)
    return user, project_name
