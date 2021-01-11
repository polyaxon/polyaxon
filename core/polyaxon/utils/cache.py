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

from polyaxon.managers.project import ProjectConfigManager
from polyaxon.utils.formatting import Printer

CACHE_ERROR = (
    "Found an invalid project config or project config cache, "
    "if you are using Polyaxon CLI please run: "
    "`polyaxon config purge --cache-only`"
)


def get_local_project():
    try:
        return ProjectConfigManager.get_config()
    except:
        Printer.print_error(CACHE_ERROR, sys_exit=True)


def _is_same_project(owner=None, project=None):
    local_project = get_local_project()
    if project and project == local_project.name:
        return not all([owner, local_project.owner]) or owner == local_project.owner


def _cache_project(config, owner=None, project=None):
    if (
        ProjectConfigManager.is_initialized()
        and ProjectConfigManager.is_locally_initialized()
    ):
        if _is_same_project(owner, project):
            ProjectConfigManager.set_config(config)
            return

    ProjectConfigManager.set_config(
        config, visibility=ProjectConfigManager.VISIBILITY_GLOBAL
    )


def cache(config_manager, config, owner=None, project=None):
    if config_manager == ProjectConfigManager:
        _cache_project(config=config, project=project, owner=owner)

    # Set caching only if we have an initialized project
    if not ProjectConfigManager.is_initialized():
        return

    if not _is_same_project(owner, project):
        return

    visibility = (
        ProjectConfigManager.VISIBILITY_LOCAL
        if ProjectConfigManager.is_locally_initialized()
        else ProjectConfigManager.VISIBILITY_GLOBAL
    )
    config_manager.set_config(config, visibility=visibility)
