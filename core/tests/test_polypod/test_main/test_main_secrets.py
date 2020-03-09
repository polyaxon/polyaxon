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

import pytest

from tests.utils import BaseTestCase

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import (
    V1BucketConnection,
    V1ClaimConnection,
    V1HostPathConnection,
    V1K8sResourceSchema,
)
from polyaxon.polypod.main.k8s_resources import get_requested_secrets
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType


@pytest.mark.polypod_mark
class TestMainSecrets(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Secrets
        self.resource1 = V1K8sResourceType(
            name="non_mount_test1",
            schema=V1K8sResourceSchema(
                name="non_mount_test1", items=["item1", "item2"]
            ),
            is_requested=False,
        )
        self.resource2 = V1K8sResourceType(
            name="non_mount_test2",
            schema=V1K8sResourceSchema(name="non_mount_test2"),
            is_requested=False,
        )
        self.resource3 = V1K8sResourceType(
            name="non_mount_test3",
            schema=V1K8sResourceSchema(
                name="non_mount_test3", items=["item1", "item2"]
            ),
            is_requested=True,
        )
        self.resource4 = V1K8sResourceType(
            name="non_mount_test4",
            schema=V1K8sResourceSchema(name="non_mount_test4"),
            is_requested=True,
        )
        self.resource5 = V1K8sResourceType(
            name="non_mount_test1",
            schema=V1K8sResourceSchema(name="non_mount_test1"),
            is_requested=True,
        )

        # Connections
        self.s3_store = V1ConnectionType(
            name="test_s3",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3//:foo"),
            secret=self.resource1.schema,
        )
        self.gcs_store = V1ConnectionType(
            name="test_gcs",
            kind=V1ConnectionKind.GCS,
            schema=V1BucketConnection(bucket="gcs//:foo"),
            secret=self.resource2.schema,
        )
        self.az_store = V1ConnectionType(
            name="test_az",
            kind=V1ConnectionKind.WASB,
            schema=V1BucketConnection(bucket="wasb://x@y.blob.core.windows.net"),
            secret=self.resource3.schema,
        )
        self.claim_store = V1ConnectionType(
            name="test_claim",
            kind=V1ConnectionKind.VOLUME_CLAIM,
            schema=V1ClaimConnection(mount_path="/tmp", volume_claim="test"),
        )
        self.host_path_store = V1ConnectionType(
            name="test_path",
            kind=V1ConnectionKind.HOST_PATH,
            schema=V1HostPathConnection(
                mount_path="/tmp", host_path="/tmp", read_only=True
            ),
        )

    def test_get_requested_secrets_non_values(self):
        assert get_requested_secrets(secrets=None, connections=None) == []
        assert get_requested_secrets(secrets=[], connections=[]) == []
        assert (
            get_requested_secrets(
                secrets=[self.resource1, self.resource2], connections=[]
            )
            == []
        )
        assert (
            get_requested_secrets(
                secrets=[], connections=[self.host_path_store, self.claim_store]
            )
            == []
        )

    def test_get_requested_secrets_and_secrets(self):
        expected = get_requested_secrets(secrets=[], connections=[self.s3_store])
        assert [e.schema for e in expected] == [self.resource1.schema]

        expected = get_requested_secrets(
            secrets=[self.resource2], connections=[self.s3_store]
        )
        assert [e.schema for e in expected] == [self.resource1.schema]

        expected = get_requested_secrets(
            secrets=[self.resource2], connections=[self.s3_store, self.gcs_store]
        )
        assert [e.schema for e in expected] == [
            self.resource1.schema,
            self.resource2.schema,
        ]

        expected = get_requested_secrets(
            secrets=[self.resource1, self.resource2],
            connections=[self.s3_store, self.gcs_store, self.az_store],
        )
        assert [e.schema for e in expected] == [
            self.resource1.schema,
            self.resource2.schema,
            self.resource3.schema,
        ]

    def test_get_requested_secrets(self):
        expected = get_requested_secrets(
            secrets=[self.resource1], connections=[self.s3_store]
        )
        assert [e.schema for e in expected] == [self.resource1.schema]
        expected = get_requested_secrets(
            secrets=[self.resource1, self.resource3], connections=[self.s3_store]
        )
        assert [e.schema for e in expected] == [
            self.resource3.schema,
            self.resource1.schema,
        ]
        expected = get_requested_secrets(
            secrets=[self.resource2, self.resource3, self.resource4],
            connections=[self.gcs_store],
        )
        assert [e.schema for e in expected] == [
            self.resource3.schema,
            self.resource4.schema,
            self.resource2.schema,
        ]
        expected = get_requested_secrets(
            secrets=[self.resource1, self.resource2], connections=[self.gcs_store]
        )
        assert [e.schema for e in expected] == [self.resource2.schema]
        expected = get_requested_secrets(
            secrets=[self.resource1, self.resource2],
            connections=[self.s3_store, self.gcs_store],
        )
        assert [e.schema for e in expected] == [
            self.resource1.schema,
            self.resource2.schema,
        ]
        expected = get_requested_secrets(
            secrets=[self.resource1, self.resource2],
            connections=[
                self.s3_store,
                self.gcs_store,
                self.host_path_store,
                self.claim_store,
            ],
        )
        assert [e.schema for e in expected] == [
            self.resource1.schema,
            self.resource2.schema,
        ]

        new_az_store = V1ConnectionType(
            name="test_az",
            kind=V1ConnectionKind.WASB,
            schema=V1BucketConnection(bucket="Conwasb://x@y.blob.core.windows.net"),
            secret=self.resource1,
        )
        expected = get_requested_secrets(
            secrets=[self.resource1, self.resource2],
            connections=[
                self.s3_store,
                self.gcs_store,
                new_az_store,
                self.host_path_store,
                self.claim_store,
            ],
        )
        assert [e.schema for e in expected] == [
            self.resource1.schema,
            self.resource2.schema,
        ]

        # Using a requested secret with same id
        expected = get_requested_secrets(
            secrets=[self.resource5, self.resource2],
            connections=[
                self.s3_store,
                self.gcs_store,
                new_az_store,
                self.host_path_store,
                self.claim_store,
            ],
        )
        assert [e.schema for e in expected] == [
            self.resource5.schema,
            self.resource2.schema,
        ]
