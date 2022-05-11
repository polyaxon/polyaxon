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


def start_streams(host: str, port: int, workers: int, per_core: bool, uds: str):
    """Start streams service."""
    from polyaxon.env_vars.keys import EV_KEYS_PROXY_STREAMS_TARGET_PORT
    from polyaxon_deploy.runners.streams import start

    port = port or os.environ.get(EV_KEYS_PROXY_STREAMS_TARGET_PORT)
    start(host=host, port=port, workers=workers, per_core=per_core, uds=uds)
