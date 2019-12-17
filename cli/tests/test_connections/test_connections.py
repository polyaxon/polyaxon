#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow.exceptions import ValidationError

from polyaxon.connections.kinds import ConnectionKind
from polyaxon.connections.schemas import (
    BlobConnectionConfig,
    ClaimConnectionConfig,
    HostConnectionConfig,
    HostPathConnectionConfig,
    validate_connection,
)


class TestBlobConnectionConfig(TestCase):
    def test_claim_connect_config(self):
        config_dict = {}
        with self.assertRaises(ValidationError):
            BlobConnectionConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(ConnectionKind.VOLUME_CLAIM, config_dict)

        config_dict = {"blob": "sdf"}
        config = BlobConnectionConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        with self.assertRaises(ValidationError):
            validate_connection(ConnectionKind.VOLUME_CLAIM, config_dict)

        validate_connection(ConnectionKind.S3, config_dict)
        validate_connection(ConnectionKind.GCP, config_dict)
        validate_connection(ConnectionKind.WASB, config_dict)


class TestClaimConnectionConfig(TestCase):
    def test_claim_connect_config(self):
        config_dict = {}
        with self.assertRaises(ValidationError):
            ClaimConnectionConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(ConnectionKind.VOLUME_CLAIM, config_dict)

        config_dict = {"volume_claim": "foo"}
        with self.assertRaises(ValidationError):
            ClaimConnectionConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(ConnectionKind.VOLUME_CLAIM, config_dict)

        config_dict = {"volume_claim": "foo", "mount_path": "foo", "read_only": True}
        config = ClaimConnectionConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        with self.assertRaises(ValidationError):
            validate_connection(ConnectionKind.S3, config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(ConnectionKind.WASB, config_dict)

        validate_connection(ConnectionKind.VOLUME_CLAIM, config_dict)


class TestHostPathConnectionConfig(TestCase):
    def test_host_path_connect_config(self):
        config_dict = {}
        with self.assertRaises(ValidationError):
            HostPathConnectionConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(ConnectionKind.HOST_PATH, config_dict)

        config_dict = {"host_path": "foo"}
        with self.assertRaises(ValidationError):
            HostPathConnectionConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(ConnectionKind.HOST_PATH, config_dict)

        config_dict = {"host_path": "foo", "mount_path": "foo", "read_only": True}
        config = HostPathConnectionConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        with self.assertRaises(ValidationError):
            validate_connection(ConnectionKind.S3, config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(ConnectionKind.WASB, config_dict)

        validate_connection(ConnectionKind.HOST_PATH, config_dict)


class TestHostConnectionConfig(TestCase):
    def test_host_connect_config(self):
        config_dict = {}
        with self.assertRaises(ValidationError):
            HostConnectionConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(ConnectionKind.GIT, config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(ConnectionKind.REGISTRY, config_dict)

        config_dict = {"url": "foo", "insecure": True}
        config = HostConnectionConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        with self.assertRaises(ValidationError):
            validate_connection(ConnectionKind.S3, config_dict)

        with self.assertRaises(ValidationError):
            validate_connection(ConnectionKind.WASB, config_dict)

        validate_connection(ConnectionKind.GIT, config_dict)
        validate_connection(ConnectionKind.REGISTRY, config_dict)
