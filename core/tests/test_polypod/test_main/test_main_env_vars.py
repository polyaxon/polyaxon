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
    V1K8sResourceSchema,
)
from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_COLLECT_ARTIFACTS,
    POLYAXON_KEYS_COLLECT_RESOURCES,
    POLYAXON_KEYS_LOG_LEVEL,
)
from polyaxon.exceptions import PolypodException
from polyaxon.polyflow import V1Plugins
from polyaxon.polypod.common.env_vars import (
    get_connection_env_var,
    get_env_var,
    get_env_vars_from_k8s_resources,
    get_items_from_config_map,
    get_items_from_secret,
    get_kv_env_vars,
)
from polyaxon.polypod.main.env_vars import get_env_vars
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType


@pytest.mark.polypod_mark
class TestMainEnvVars(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Secrets
        self.resource1 = V1K8sResourceType(
            name="non_mount_test1",
            schema=V1K8sResourceSchema(name="ref", items=["item1", "item2"]),
            is_requested=False,
        )
        self.resource2 = V1K8sResourceType(
            name="non_mount_test2",
            schema=V1K8sResourceSchema(name="ref"),
            is_requested=False,
        )

        self.resource3 = V1K8sResourceType(
            name="non_mount_test1",
            schema=V1K8sResourceSchema(name="ref", items=["item1", "item2"]),
            is_requested=True,
        )
        self.resource4 = V1K8sResourceType(
            name="non_mount_test2",
            schema=V1K8sResourceSchema(name="ref"),
            is_requested=True,
        )

        self.resource5 = V1K8sResourceType(
            name="non_mount_test2",
            schema=V1K8sResourceSchema(name="ref"),
            is_requested=True,
        )

        self.resource6 = V1K8sResourceType(
            name="mount_test",
            schema=V1K8sResourceSchema(name="ref", mount_path="/test"),
            is_requested=True,
        )
        # Connections
        self.bucket_store = V1ConnectionType(
            name="test_s3",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3//:foo"),
            secret=self.resource3.schema,
        )
        self.mount_store = V1ConnectionType(
            name="test_claim",
            kind=V1ConnectionKind.VOLUME_CLAIM,
            schema=V1ClaimConnection(
                mount_path="/tmp", volume_claim="test", read_only=True
            ),
        )

    def test_get_env_vars(self):
        assert (
            get_env_vars(
                contexts=None,
                log_level=None,
                kv_env_vars=None,
                connections=None,
                secrets=None,
                config_maps=None,
            )
            == []
        )

    def test_get_env_vars_with_kv_env_vars(self):
        # Check wrong kv env vars
        with self.assertRaises(PolypodException):
            get_env_vars(
                contexts=None,
                log_level=None,
                kv_env_vars=["x", "y", "z"],
                connections=None,
                secrets=None,
                config_maps=None,
            )
        with self.assertRaises(PolypodException):
            get_env_vars(
                contexts=None,
                log_level=None,
                kv_env_vars={"x": "y"},
                connections=None,
                secrets=None,
                config_maps=None,
            )

        # Valid kv env vars
        assert get_env_vars(
            contexts=None,
            log_level=None,
            kv_env_vars=[["key1", "val1"], ["key2", "val2"]],
            connections=None,
            secrets=None,
            config_maps=None,
        ) == get_kv_env_vars([["key1", "val1"], ["key2", "val2"]])

    def test_get_env_vars_with_artifacts_store(self):
        assert (
            get_env_vars(
                contexts=None,
                log_level=None,
                kv_env_vars=None,
                connections=None,
                secrets=None,
                config_maps=None,
            )
            == []
        )

        assert get_env_vars(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    collect_logs=False, collect_artifacts=True, collect_resources=True
                )
            ),
            log_level=None,
            kv_env_vars=None,
            connections=None,
            secrets=None,
            config_maps=None,
        ) == [
            get_env_var(name=POLYAXON_KEYS_COLLECT_ARTIFACTS, value=True),
            get_env_var(name=POLYAXON_KEYS_COLLECT_RESOURCES, value=True),
        ]

        assert (
            get_env_vars(
                contexts=PluginsContextsSpec.from_config(
                    V1Plugins(
                        collect_logs=False,
                        collect_artifacts=False,
                        collect_resources=False,
                    )
                ),
                log_level=None,
                kv_env_vars=None,
                connections=None,
                secrets=None,
                config_maps=None,
            )
            == []
        )

        assert (
            get_env_vars(
                contexts=None,
                log_level=None,
                kv_env_vars=None,
                connections=None,
                secrets=None,
                config_maps=None,
            )
            == []
        )

        assert get_env_vars(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    collect_logs=False, collect_artifacts=True, collect_resources=False
                )
            ),
            log_level=None,
            kv_env_vars=None,
            connections=None,
            secrets=None,
            config_maps=None,
        ) == [get_env_var(name=POLYAXON_KEYS_COLLECT_ARTIFACTS, value=True)]

    def test_get_env_vars_with_secrets(self):
        assert get_env_vars(
            contexts=None,
            log_level=None,
            kv_env_vars=None,
            connections=None,
            secrets=[self.resource1, self.resource2],
            config_maps=None,
        ) == get_items_from_secret(secret=self.resource1) + get_items_from_secret(
            secret=self.resource2
        )

        assert get_env_vars(
            contexts=None,
            log_level=None,
            kv_env_vars=None,
            connections=None,
            secrets=[self.resource1, self.resource2, self.resource3, self.resource4],
            config_maps=None,
        ) == get_items_from_secret(secret=self.resource1) + get_items_from_secret(
            secret=self.resource2
        ) + get_items_from_secret(
            secret=self.resource3
        ) + get_items_from_secret(
            secret=self.resource4
        )

    def test_get_env_vars_with_config_maps(self):
        assert get_env_vars(
            contexts=None,
            log_level=None,
            kv_env_vars=None,
            connections=None,
            secrets=None,
            config_maps=[self.resource1, self.resource2],
        ) == get_items_from_config_map(
            config_map=self.resource1
        ) + get_items_from_config_map(
            config_map=self.resource2
        )

        assert get_env_vars(
            contexts=None,
            log_level=None,
            kv_env_vars=None,
            connections=None,
            secrets=None,
            config_maps=[
                self.resource1,
                self.resource2,
                self.resource3,
                self.resource4,
            ],
        ) == get_items_from_config_map(
            config_map=self.resource1
        ) + get_items_from_config_map(
            config_map=self.resource2
        ) + get_items_from_config_map(
            config_map=self.resource3
        ) + get_items_from_config_map(
            config_map=self.resource4
        )

    def test_get_env_vars_with_all(self):
        connection = V1ConnectionType(
            name="test_s3",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3//:foo"),
            secret=self.resource6.schema,
        )

        env_vars = get_env_vars(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    collect_logs=False, collect_artifacts=True, collect_resources=True
                )
            ),
            log_level="info",
            kv_env_vars=[["key1", "val1"], ["key2", "val2"]],
            connections=[connection],
            secrets=[
                self.resource1,
                self.resource2,
                self.resource3,
                self.resource4,
                self.resource6,
            ],
            config_maps=[
                self.resource1,
                self.resource2,
                self.resource3,
                self.resource4,
            ],
        )
        expected = [
            get_env_var(name=POLYAXON_KEYS_LOG_LEVEL, value="info"),
            get_env_var(name=POLYAXON_KEYS_COLLECT_ARTIFACTS, value=True),
            get_env_var(name=POLYAXON_KEYS_COLLECT_RESOURCES, value=True),
        ]
        expected += get_connection_env_var(connection=connection, secret=self.resource6)
        expected += get_kv_env_vars([["key1", "val1"], ["key2", "val2"]])
        expected += get_env_vars_from_k8s_resources(
            secrets=[
                self.resource1,
                self.resource2,
                self.resource3,
                self.resource4,
                self.resource6,
            ],
            config_maps=[
                self.resource1,
                self.resource2,
                self.resource3,
                self.resource4,
            ],
        )

        assert env_vars == expected
