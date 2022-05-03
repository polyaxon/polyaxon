#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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
from polyaxon import settings
from polyaxon.services.values import PolyaxonServices
from polyaxon_deploy.runners.base import start_app


def start(
    host: str = None,
    port: int = None,
    log_level: str = None,
    workers: int = None,
    per_core: bool = False,
    uds: str = None,
):
    settings.set_sandbox_config()

    start_app(
        app="polyaxon_deploy.apps.sandbox:app",
        app_name=PolyaxonServices.SANDBOX,
        host=host or settings.SANDBOX_CONFIG.host,
        port=port or settings.SANDBOX_CONFIG.port,
        log_level=log_level or settings.CLIENT_CONFIG.log_level,
        workers=workers or settings.SANDBOX_CONFIG.workers,
        per_core=per_core or settings.SANDBOX_CONFIG.per_core,
        uds=uds,
    )
