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

from marshmallow.exceptions import ValidationError

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import (
    V1BucketConnection,
    V1ClaimConnection,
    V1GitConnection,
    V1HostConnection,
    V1HostPathConnection,
    validate_connection,
)
from tests.utils import BaseTestCase


class TestV1BucketConnection(BaseTestCase):
    def test_claim_connect_config(self):
        config_dict = {}
        with self.assertRaises(ValidationError):
            V1BucketConnection.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.VOLUME_CLAIM, config_dict)

        config_dict = {"bucket": "sdf"}
        config = V1BucketConnection.from_dict(config_dict)
        assert config.to_dict() == config_dict

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.VOLUME_CLAIM, config_dict)

        validate_connection(V1ConnectionKind.S3, config_dict)
        validate_connection(V1ConnectionKind.GCP, config_dict)
        validate_connection(V1ConnectionKind.WASB, config_dict)


class TestV1ClaimConnection(BaseTestCase):
    def test_claim_connect_config(self):
        config_dict = {}
        with self.assertRaises(ValidationError):
            V1ClaimConnection.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.VOLUME_CLAIM, config_dict)

        config_dict = {"volumeClaim": "foo"}
        with self.assertRaises(ValidationError):
            V1ClaimConnection.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.VOLUME_CLAIM, config_dict)

        config_dict = {"volumeClaim": "foo", "mountPath": "foo", "readOnly": True}
        config = V1ClaimConnection.from_dict(config_dict)
        assert config.to_dict() == config_dict

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.S3, config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.WASB, config_dict)

        validate_connection(V1ConnectionKind.VOLUME_CLAIM, config_dict)


class TestV1HostPathConnection(BaseTestCase):
    def test_host_path_connect_config(self):
        config_dict = {}
        with self.assertRaises(ValidationError):
            V1HostPathConnection.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.HOST_PATH, config_dict)

        config_dict = {"host_path": "foo"}
        with self.assertRaises(ValidationError):
            V1HostPathConnection.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.HOST_PATH, config_dict)

        config_dict = {"hostPath": "foo", "mountPath": "foo", "readOnly": True}
        config = V1HostPathConnection.from_dict(config_dict)
        assert config.to_dict() == config_dict

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.S3, config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.WASB, config_dict)

        validate_connection(V1ConnectionKind.HOST_PATH, config_dict)


class TestV1HostConnection(BaseTestCase):
    def test_host_connect_config(self):
        config_dict = {}
        with self.assertRaises(ValidationError):
            V1HostConnection.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.REGISTRY, config_dict)

        config_dict = {"url": "foo", "insecure": True}
        config = V1HostConnection.from_dict(config_dict)
        assert config.to_dict() == config_dict

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.GIT, config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.S3, config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.WASB, config_dict)

        validate_connection(V1ConnectionKind.REGISTRY, config_dict)


class TestV1GitConnection(BaseTestCase):
    def test_git_connect_config(self):
        config_dict = {}
        V1GitConnection.from_dict(config_dict)
        validate_connection(V1ConnectionKind.GIT, config_dict)

        config_dict = {"url": "foo"}
        config = V1GitConnection.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"url": "foo", "revision": "foo"}
        config = V1GitConnection.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {
            "url": "foo",
            "revision": "foo",
            "flags": ["flag1", "--flag2", "k=v"],
        }
        config = V1GitConnection.from_dict(config_dict)
        assert config.to_dict() == config_dict

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.REGISTRY, config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.S3, config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(V1ConnectionKind.WASB, config_dict)

        validate_connection(V1ConnectionKind.GIT, config_dict)
