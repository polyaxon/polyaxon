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

import pytest

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import (
    V1BucketConnection,
    V1ClaimConnection,
    V1HostPathConnection,
)
from polyaxon.polyflow import V1Init
from polyaxon.polypod.common.annotations import get_connection_annotations
from polyaxon.schemas.types import V1ConnectionType
from polyaxon.utils.test_utils import BaseTestCase


@pytest.mark.polypod_mark
class TestAnnotations(BaseTestCase):
    def test_get_annotations_from_connection(self):
        # No connections
        assert (
            get_connection_annotations(
                artifacts_store=None,
                init_connections=None,
                connections=None,
                connection_by_names=None,
            )
            == {}
        )
        assert (
            get_connection_annotations(
                artifacts_store=None,
                init_connections=[],
                connections=[],
                connection_by_names={},
            )
            == {}
        )

        # Store
        store = V1ConnectionType(
            name="test",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3//:foo"),
        )
        assert (
            get_connection_annotations(
                artifacts_store=store,
                init_connections=None,
                connections=None,
                connection_by_names={store.name: store},
            )
            == {}
        )

        store.annotations = {"foo": "bar"}
        assert (
            get_connection_annotations(
                artifacts_store=store,
                init_connections=None,
                connections=None,
                connection_by_names={store.name: store},
            )
            == store.annotations
        )

        # Add connections
        init_conn = V1ConnectionType(
            name="init",
            kind=V1ConnectionKind.SLACK,
            annotations={"init1_key1": "val1", "init1_key2": "val2"},
        )
        init = V1Init(connection="init")
        conn1 = V1ConnectionType(
            name="conn1",
            kind=V1ConnectionKind.VOLUME_CLAIM,
            schema=V1ClaimConnection(
                mount_path="/tmp", volume_claim="test", read_only=True
            ),
            annotations={"conn1_key1": "val1", "conn1_key2": "val2"},
        )
        conn2 = V1ConnectionType(
            name="conn2",
            kind=V1ConnectionKind.HOST_PATH,
            schema=V1HostPathConnection(
                mount_path="/tmp", host_path="/tmp", read_only=True
            ),
            annotations={"conn2_key1": "val1", "conn2_key2": "val2"},
        )
        assert get_connection_annotations(
            artifacts_store=store,
            init_connections=[init],
            connections=[conn1.name, conn2.name],
            connection_by_names={
                store.name: store,
                init_conn.name: init_conn,
                conn1.name: conn1,
                conn2.name: conn2,
            },
        ) == dict(
            **store.annotations,
            **init_conn.annotations,
            **conn1.annotations,
            **conn2.annotations
        )
