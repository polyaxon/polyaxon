#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

from polyaxon.constants.globals import DEFAULT
from polyaxon.env_vars.getters import get_entity_info
from polyaxon.env_vars.getters.user import get_local_owner
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.managers.project import ProjectConfigManager
from polyaxon.utils.cache import get_local_project
from polyaxon.utils.formatting import Printer


def get_project_error_message(owner, project):
    if not owner or not project:
        return (
            "Please provide a valid project. "
            "Context: <owner: {}> - <project: {}>".format(
                owner or "Missing", project or "Missing"
            )
        )


def get_project_or_local(project=None, is_cli: bool = False):
    from polyaxon import settings

    if not project and not ProjectConfigManager.is_initialized():
        error_message = "Please provide a valid project or initialize a project in the current path."
        if is_cli:
            Printer.print_error(error_message)
            sys.exit(1)
        else:
            raise PolyaxonClientException(error_message)

    if project:
        try:
            owner, project_name = get_entity_info(project)
        except Exception as e:
            if is_cli:
                Printer.print_error("Please provide a valid project name.\n%s" % e)
                sys.exit(1)
            else:
                raise e
    else:
        project = get_local_project(is_cli=is_cli)

        owner, project_name = project.owner, project.name

    if not owner:
        owner = get_local_owner(is_cli=is_cli)

    if not owner and (not settings.CLI_CONFIG or settings.CLI_CONFIG.is_ce):
        owner = DEFAULT

    if not all([owner, project_name]):
        error_message = get_project_error_message(owner, project_name)
        if is_cli:
            Printer.print_error(error_message)
            sys.exit(1)
        else:
            raise PolyaxonClientException(error_message)
    return owner, project_name
