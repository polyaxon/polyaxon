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

import ujson

from marshmallow import ValidationError

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import V1BucketConnection, V1K8sResourceSchema
from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_AGENT_ARTIFACTS_STORE,
    POLYAXON_KEYS_AGENT_CONNECTIONS,
    POLYAXON_KEYS_AGENT_NOTIFICATION_CONNECTIONS,
    POLYAXON_KEYS_K8S_NAMESPACE,
)
from polyaxon.schemas.cli.agent_config import AgentConfig
from tests.utils import BaseTestCase


@pytest.mark.schemas_mark
class TestAgentConfig(BaseTestCase):
    def test_agent_config(self):
        config_dict = {POLYAXON_KEYS_AGENT_ARTIFACTS_STORE: 12}
        with self.assertRaises(ValidationError):
            AgentConfig.from_dict(config_dict)

        config_dict = {POLYAXON_KEYS_AGENT_ARTIFACTS_STORE: "some"}
        with self.assertRaises(ValidationError):
            AgentConfig.from_dict(config_dict)

        config_dict = {
            POLYAXON_KEYS_K8S_NAMESPACE: "foo",
            POLYAXON_KEYS_AGENT_ARTIFACTS_STORE: {
                "name": "some",
                "kind": V1ConnectionKind.GCS,
                "schema": V1BucketConnection(bucket="gs://test").to_dict(),
            },
            POLYAXON_KEYS_AGENT_CONNECTIONS: [],
            POLYAXON_KEYS_AGENT_NOTIFICATION_CONNECTIONS: [],
        }
        config = AgentConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            POLYAXON_KEYS_K8S_NAMESPACE: "foo",
            POLYAXON_KEYS_AGENT_ARTIFACTS_STORE: "some",
            POLYAXON_KEYS_AGENT_NOTIFICATION_CONNECTIONS: [],
            POLYAXON_KEYS_AGENT_CONNECTIONS: [
                {
                    "name": "some",
                    "kind": V1ConnectionKind.GCS,
                    "schema": V1BucketConnection(bucket="gs://test").to_dict(),
                    "secretResource": "some",
                }
            ],
        }
        with self.assertRaises(ValidationError):
            AgentConfig.from_dict(config_dict)

        config_dict = {
            POLYAXON_KEYS_K8S_NAMESPACE: "foo",
            POLYAXON_KEYS_AGENT_ARTIFACTS_STORE: {
                "name": "test",
                "kind": V1ConnectionKind.GCS,
                "schema": V1BucketConnection(bucket="gs://test").to_dict(),
                "secret": V1K8sResourceSchema(name="some").to_dict(),
            },
            POLYAXON_KEYS_AGENT_NOTIFICATION_CONNECTIONS: [
                {
                    "name": "slack",
                    "kind": V1ConnectionKind.SLACK,
                    "secret": V1K8sResourceSchema(name="some").to_dict(),
                }
            ],
            POLYAXON_KEYS_AGENT_CONNECTIONS: [
                {
                    "name": "some",
                    "kind": V1ConnectionKind.GCS,
                    "schema": V1BucketConnection(bucket="gs://test").to_dict(),
                    "secret": V1K8sResourceSchema(name="some").to_dict(),
                }
            ],
        }
        config = AgentConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_agent_config_from_str_envs(self):
        config_dict = {
            POLYAXON_KEYS_K8S_NAMESPACE: "foo",
            POLYAXON_KEYS_AGENT_ARTIFACTS_STORE: ujson.dumps(
                {
                    "name": "test1",
                    "kind": V1ConnectionKind.GCS,
                    "schema": V1BucketConnection(bucket="gs://test").to_dict(),
                    "secret": V1K8sResourceSchema(name="some").to_dict(),
                }
            ),
            POLYAXON_KEYS_AGENT_NOTIFICATION_CONNECTIONS: ujson.dumps(
                [
                    {
                        "name": "slack",
                        "kind": V1ConnectionKind.SLACK,
                        "secret": V1K8sResourceSchema(name="some").to_dict(),
                    }
                ],
            ),
            POLYAXON_KEYS_AGENT_CONNECTIONS: ujson.dumps(
                [
                    {
                        "name": "test2",
                        "kind": V1ConnectionKind.GCS,
                        "schema": V1BucketConnection(bucket="gs://test").to_dict(),
                        "secret": V1K8sResourceSchema(name="some").to_dict(),
                    }
                ]
            ),
        }

        config = AgentConfig.from_dict(config_dict)
        assert len(config.secrets) == 1
        assert len(config.to_light_dict()[POLYAXON_KEYS_AGENT_CONNECTIONS]) == 1
