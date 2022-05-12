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


def start_sandbox(
    host: str, port: int, workers: int, per_core: bool, path: str, uds: str
):
    """Start sandbox service."""
    from polyaxon.env_vars.keys import EV_KEYS_SANDBOX_ROOT, EV_KEYS_SERVICE
    from polyaxon.services.values import PolyaxonServices
    from polyaxon_deploy.runners.sandbox import start

    os.environ[EV_KEYS_SERVICE] = PolyaxonServices.SANDBOX
    if path:
        os.environ[EV_KEYS_SANDBOX_ROOT] = path

    start(host=host, port=port, workers=workers, per_core=per_core, uds=uds)
