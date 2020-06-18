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

from polyaxon.managers.project import ProjectManager


def _is_same_project(owner=None, project=None):
    local_project = ProjectManager.get_config()
    if project and project == local_project.name:
        return not all([owner, local_project.owner]) or owner == local_project.owner


def _cache_project(config, owner=None, project=None):
    if ProjectManager.is_initialized() and ProjectManager.is_locally_initialized():
        if _is_same_project(owner, project):
            ProjectManager.set_config(config)
            return

    ProjectManager.set_config(config, visibility=ProjectManager.VISIBILITY_GLOBAL)


def cache(config_manager, config, owner=None, project=None):
    if config_manager == ProjectManager:
        _cache_project(config=config, project=project, owner=owner)

    # Set caching only if we have an initialized project
    if not ProjectManager.is_initialized():
        return

    if not _is_same_project(owner, project):
        return

    visibility = (
        ProjectManager.VISIBILITY_LOCAL
        if ProjectManager.is_locally_initialized()
        else ProjectManager.VISIBILITY_GLOBAL
    )
    config_manager.set_config(config, visibility=visibility)
