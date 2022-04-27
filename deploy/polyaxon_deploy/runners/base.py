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
import os

import uvicorn

from polyaxon.utils.workers_utils import get_core_workers
from polyaxon_deploy.logger import logger


def start_app(
    app,
    app_name,
    host: str = None,
    port: int = None,
    log_level: str = None,
    workers: int = None,
    per_core: bool = False,
    uds: str = None,
):
    host = host or "0.0.0.0"
    port = int(port or 8000)
    log_level = log_level or "warning"
    if per_core:
        workers = get_core_workers(per_core=workers or 2)
    else:
        workers = workers or get_core_workers(per_core=2)

    logger.info(
        "{app_name} is running on http://{host}:{port} in process {pid}".format(
            app_name=app_name, host=host, port=port, pid=os.getpid()
        )
    )
    uvicorn.run(
        app,
        host=host,
        port=port,
        access_log=False,
        log_level=log_level.lower(),
        workers=workers,
        uds=uds,
        timeout_keep_alive=120,
    )
