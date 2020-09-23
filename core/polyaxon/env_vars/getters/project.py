#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

import sys

from polyaxon.constants import DEFAULT
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.managers.project import ProjectConfigManager
from polyaxon.utils.formatting import Printer


def get_project_full_name(owner: str = None, project: str = None) -> str:
    if owner and project:
        return "{}/{}".format(owner, project)
    return project


def get_project_info(project):
    from polyaxon import settings

    parts = project.replace(".", "/").split("/")
    if len(parts) == 2:
        owner, project_name = parts
    else:
        owner = settings.AUTH_CONFIG.username
        project_name = project

    return owner, project_name


def get_project_or_local(project=None, is_cli: bool = False):
    from polyaxon import settings

    if not project and not ProjectConfigManager.is_initialized():
        if is_cli:
            Printer.print_error("Please provide a valid project.")
            sys.exit(1)
        else:
            raise PolyaxonClientException("Please provide a valid project.")

    if project:
        owner, project_name = get_project_info(project)
    else:
        project = ProjectConfigManager.get_config()
        owner, project_name = project.owner, project.name

    if not owner and (not settings.CLI_CONFIG or settings.CLI_CONFIG.is_ce):
        owner = DEFAULT

    if not all([owner, project_name]):
        if is_cli:
            Printer.print_error("Please provide a valid project.")
            sys.exit(1)
        else:
            raise PolyaxonClientException("Please provide a valid project.")
    return owner, project_name
