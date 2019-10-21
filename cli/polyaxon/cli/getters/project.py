#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon.managers.auth import AuthConfigManager
from polyaxon.managers.project import ProjectManager
from polyaxon.utils import constants
from polyaxon.utils.formatting import Printer


def get_project_info(project):
    parts = project.replace(".", "/").split("/")
    if len(parts) == 2:
        user, project_name = parts
    else:
        user = AuthConfigManager.get_value("username")
        project_name = project

    return user, project_name


def get_project_or_local(project=None):
    if not project and not ProjectManager.is_initialized():
        Printer.print_error(
            "Please provide a valid project, or init a new project. "
            " {}".format(constants.INIT_COMMAND)
        )
        sys.exit(1)

    if project:
        user, project_name = get_project_info(project)
    else:
        project = ProjectManager.get_config()
        user, project_name = project.user, project.name

    if not all([user, project_name]):
        Printer.print_error(
            "Please provide a valid project, or init a new project."
            " {}".format(constants.INIT_COMMAND)
        )
        sys.exit(1)
    return user, project_name
