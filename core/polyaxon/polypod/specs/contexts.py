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

from collections import namedtuple

from polyaxon import settings
from polyaxon.polyflow import V1Plugins


class PluginsContextsSpec(
    namedtuple(
        "PluginsContextsSpec",
        "auth "
        "docker "
        "shm "
        "collect_logs "
        "collect_artifacts "
        "collect_resources "
        "auto_resume "
        "sync_statuses",
    )
):
    @classmethod
    def from_config(
        cls, config: V1Plugins, default_auth: bool = False
    ) -> "PluginsContextsSpec":
        auth = default_auth
        docker = False
        shm = True
        collect_logs = True
        collect_artifacts = True
        collect_resources = True
        auto_resume = True
        sync_statuses = True
        if config:
            if config.collect_logs is not None:
                collect_logs = config.collect_logs
            if config.collect_artifacts is not None:
                collect_artifacts = config.collect_artifacts
            if config.collect_resources is not None:
                collect_resources = config.collect_resources
            if config.auto_resume is not None:
                auto_resume = config.auto_resume
            if config.sync_statuses is not None:
                sync_statuses = config.sync_statuses
            if config.auth is not None:
                auth = config.auth
            if config.docker is not None:
                docker = config.docker
            if config.shm is not None:
                shm = config.shm
        if settings.CLIENT_CONFIG.no_api:
            auth = False
            collect_logs = False
            collect_artifacts = False
            auto_resume = False

        return cls(
            auth=auth,
            docker=docker,
            shm=shm,
            collect_logs=collect_logs,
            collect_artifacts=collect_artifacts,
            collect_resources=collect_resources,
            auto_resume=auto_resume,
            sync_statuses=sync_statuses,
        )
