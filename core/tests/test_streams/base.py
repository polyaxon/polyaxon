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


import tempfile

from starlette.testclient import TestClient

from polyaxon import settings
from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import V1HostPathConnection
from polyaxon.schemas.cli.agent_config import AgentConfig
from polyaxon.schemas.types import V1ConnectionType
from polyaxon.streams.app.main import app


def set_store():
    store_root = tempfile.mkdtemp()
    settings.AGENT_CONFIG = AgentConfig(
        artifacts_store=V1ConnectionType(
            name="test",
            kind=V1ConnectionKind.HOST_PATH,
            schema=V1HostPathConnection(host_path=store_root, mount_path=store_root),
            secret=None,
        ),
        connections=[],
    )
    settings.CLIENT_CONFIG.archive_root = tempfile.mkdtemp()
    return store_root


def create_tmp_files(path):
    for i in range(4):
        open("{}/{}".format(path, i), "+w")


def get_streams_client():
    return TestClient(app)
