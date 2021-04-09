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

import pytest

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import (
    V1BucketConnection,
    V1ClaimConnection,
    V1HostPathConnection,
)
from polyaxon.connections.schemas.connections import V1CustomConnection
from polyaxon.schemas.types import V1ConnectionType
from tests.utils import BaseTestCase


@pytest.mark.parser_mark
class TestConnectionType(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.s3_store = V1ConnectionType(
            name="test",
            kind=V1ConnectionKind.S3,
            tags=["test", "foo"],
            schema=V1BucketConnection(bucket="s3//:foo"),
        )
        self.gcs_store = V1ConnectionType(
            name="test",
            kind=V1ConnectionKind.GCS,
            tags=["test"],
            schema=V1BucketConnection(bucket="gs//:foo"),
        )
        self.az_store = V1ConnectionType(
            name="test",
            kind=V1ConnectionKind.WASB,
            schema=V1BucketConnection(bucket="Conwasb://x@y.blob.core.windows.net"),
        )
        self.claim_store = V1ConnectionType(
            name="test",
            kind=V1ConnectionKind.VOLUME_CLAIM,
            schema=V1ClaimConnection(
                volume_claim="test", mount_path="/tmp", read_only=True
            ),
        )
        self.host_path_store = V1ConnectionType(
            name="test",
            kind=V1ConnectionKind.HOST_PATH,
            schema=V1HostPathConnection(
                host_path="/tmp", mount_path="/tmp", read_only=True
            ),
        )

        self.custom_connection1 = V1ConnectionType(
            name="db",
            kind=V1ConnectionKind.POSTGRES,
        )

        self.custom_connection2 = V1ConnectionType(
            name="ssh",
            kind=V1ConnectionKind.SSH,
            schema=V1CustomConnection(key1="val1", key2="val2"),
        )

    def test_store_path(self):
        assert self.s3_store.store_path == self.s3_store.schema.bucket
        assert self.s3_store.tags == ["test", "foo"]
        assert self.gcs_store.store_path == self.gcs_store.schema.bucket
        assert self.gcs_store.tags == ["test"]
        assert self.az_store.store_path == self.az_store.schema.bucket
        assert self.az_store.tags is None
        assert self.claim_store.store_path == self.claim_store.schema.mount_path
        assert self.claim_store.tags is None
        assert self.host_path_store.store_path == self.claim_store.schema.mount_path
        assert self.host_path_store.tags is None

    def test_is_bucket(self):
        assert self.s3_store.is_bucket is True
        assert self.s3_store.is_s3 is True
        assert self.s3_store.is_gcs is False

        assert self.gcs_store.is_bucket is True
        assert self.gcs_store.is_gcs is True
        assert self.gcs_store.is_s3 is False

        assert self.az_store.is_bucket is True
        assert self.az_store.is_wasb is True
        assert self.az_store.is_s3 is False
        assert self.az_store.is_gcs is False

        assert self.claim_store.is_bucket is False
        assert self.claim_store.is_s3 is False

        assert self.host_path_store.is_bucket is False
        assert self.host_path_store.is_s3 is False

    @staticmethod
    def assert_from_model(spec: V1ConnectionType):
        result = V1ConnectionType.from_model(model=spec)

        assert result.name == spec.name
        assert result.kind == spec.kind
        if spec.schema is None:
            assert result.schema == spec.schema
        else:
            value_dict = spec.schema.to_dict()
            result_dict = result.schema.to_dict()
            assert value_dict.keys() == result_dict.keys()
            for k in result_dict.keys():
                assert value_dict[k] == result_dict[k]
        assert result.secret == spec.secret

    def test_get_from_model_s(self):
        self.assert_from_model(self.s3_store)
        self.assert_from_model(self.gcs_store)
        self.assert_from_model(self.az_store)
        self.assert_from_model(self.claim_store)
        self.assert_from_model(self.host_path_store)
        assert self.custom_connection1.schema is None
        self.assert_from_model(self.custom_connection1)
        assert self.custom_connection2.schema.key1 == "val1"
        assert self.custom_connection2.schema.key2 == "val2"
        self.assert_from_model(self.custom_connection2)
