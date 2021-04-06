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

from mock import MagicMock

from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common.containers import sanitize_container_env
from tests.utils import BaseTestCase


@pytest.mark.polypod_mark
class TestSanitizeContainerEnv(BaseTestCase):
    def test_sanitize_container_env_value(self):
        value = MagicMock(env=[{"foo": "bar"}])
        assert sanitize_container_env(value).env[0] == {"foo": "bar"}

        value = MagicMock(env=[{"foo": 1}])
        assert sanitize_container_env(value).env[0] == {"foo": "1"}

        value = MagicMock(
            env=[
                {
                    "name": "secret-name",
                    "value": True,
                },
            ]
        )
        assert sanitize_container_env(value).env[0] == {
            "name": "secret-name",
            "value": "true",
        }

        value = MagicMock(
            env=[
                {
                    "name": "secret-name",
                    "value": 1,
                },
            ]
        )
        assert sanitize_container_env(value).env[0] == {
            "name": "secret-name",
            "value": "1",
        }

        value = MagicMock(
            env=[
                {
                    "name": "secret-name",
                    "value": "test",
                },
            ]
        )
        assert sanitize_container_env(value).env[0] == {
            "name": "secret-name",
            "value": "test",
        }

        value = MagicMock(
            env=[
                {
                    "name": "secret-name",
                    "value": {"foo": "bar"},
                },
            ]
        )
        assert sanitize_container_env(value).env[0] == {
            "name": "secret-name",
            "value": '{"foo": "bar"}',
        }

        value = MagicMock(env=[{"foo": {"key": "value"}}])
        assert sanitize_container_env(value).env[0] == {"foo": {"key": "value"}}

    def test_sanitize_container_env_value_obj(self):
        value = MagicMock(
            env=[
                k8s_schemas.V1EnvVar(
                    name="secret-name",
                    value=True,
                ),
            ]
        )
        assert sanitize_container_env(value).env[0] == k8s_schemas.V1EnvVar(
            name="secret-name",
            value="true",
        )

        value = MagicMock(
            env=[
                k8s_schemas.V1EnvVar(
                    name="secret-name",
                    value=1,
                ),
            ]
        )
        assert sanitize_container_env(value).env[0] == k8s_schemas.V1EnvVar(
            name="secret-name",
            value="1",
        )

        value = MagicMock(
            env=[
                k8s_schemas.V1EnvVar(
                    name="secret-name",
                    value="test",
                ),
            ]
        )
        assert sanitize_container_env(value).env[0] == k8s_schemas.V1EnvVar(
            name="secret-name",
            value="test",
        )

        value = MagicMock(
            env=[
                k8s_schemas.V1EnvVar(
                    name="secret-name",
                    value={"foo": "bar"},
                ),
            ]
        )
        assert sanitize_container_env(value).env[0] == k8s_schemas.V1EnvVar(
            name="secret-name",
            value='{"foo": "bar"}',
        )

    def test_sanitize_container_env_value_from(self):
        value = MagicMock(
            env=[
                {
                    "name": "secret-name",
                    "valueFrom": {
                        "secretKeyRef": {
                            "name": "my-secret",
                            "key": "my-key",
                        }
                    },
                },
            ]
        )
        assert sanitize_container_env(value).env[0] == {
            "name": "secret-name",
            "valueFrom": {
                "secretKeyRef": {
                    "name": "my-secret",
                    "key": "my-key",
                }
            },
        }

        value = MagicMock(
            env=[
                {
                    "name": "secret-name",
                    "valueFrom": {
                        "configKeyRef": {
                            "name": "my-secret",
                            "key": "my-key",
                        }
                    },
                },
            ]
        )
        assert sanitize_container_env(value).env[0] == {
            "name": "secret-name",
            "valueFrom": {
                "configKeyRef": {
                    "name": "my-secret",
                    "key": "my-key",
                }
            },
        }

    def test_sanitize_container_env_value_from_obj(self):
        value = MagicMock(
            env=[
                k8s_schemas.V1EnvVar(
                    name="secret-name",
                    value_from=k8s_schemas.V1EnvVarSource(
                        config_map_key_ref=k8s_schemas.V1ConfigMapKeySelector(
                            key="my-key",
                            name="my-secret",
                        )
                    ),
                ),
            ]
        )
        assert sanitize_container_env(value).env[0] == k8s_schemas.V1EnvVar(
            name="secret-name",
            value_from=k8s_schemas.V1EnvVarSource(
                config_map_key_ref=k8s_schemas.V1ConfigMapKeySelector(
                    key="my-key",
                    name="my-secret",
                )
            ),
        )

        value = MagicMock(
            env=[
                k8s_schemas.V1EnvVar(
                    name="secret-name",
                    value_from=k8s_schemas.V1EnvVarSource(
                        config_map_key_ref=k8s_schemas.V1SecretKeySelector(
                            key="my-key",
                            name="my-secret",
                        )
                    ),
                ),
            ]
        )
        assert sanitize_container_env(value).env[0] == k8s_schemas.V1EnvVar(
            name="secret-name",
            value_from=k8s_schemas.V1EnvVarSource(
                config_map_key_ref=k8s_schemas.V1SecretKeySelector(
                    key="my-key",
                    name="my-secret",
                )
            ),
        )
