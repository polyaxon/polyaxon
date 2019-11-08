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

from marshmallow import ValidationError

from polyaxon.deploy.schemas.persistence import (
    PersistenceConfig,
    PersistenceEntityConfig,
)


class TestPersistenceConfig(TestCase):
    def test_persistence_entity_config(self):
        bad_config_dicts = [
            {"existingClaim": 1},
            {"mountPath": False},
            {"hostPath": False},
            {"store": False},
            {"store": "dfo"},
            {"bucket": False},
            {"secret": False},
            {"secretKey": 321},
            {"readOnly": "foo"},
            {"existingClaim": "foo", "hostPath": "bar"},
            {"existingClaim": "foo", "store": "bar"},
            {"hostPath": "foo", "store": "s3"},
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                PersistenceEntityConfig.from_dict(config_dict)

        config_dicts = [
            {"existingClaim": "test"},
            {"mountPath": "test"},
            {"hostPath": "test"},
            {"store": "azure"},
            {"bucket": "test"},
            {"secret": "test"},
            {"secretKey": "test"},
            {"readOnly": False},
        ]

        for config_dict in config_dicts:
            config = PersistenceEntityConfig.from_dict(config_dict)
            assert config.to_light_dict() == config_dict

    def test_persistence_config(self):
        bad_config_dicts = [
            {"logs": {"existingClaim": "foo"}, "data": {"existingClaim": False}},
            {
                "repos": {"hostPath": "foo"},
                "data": {"foo": {"existingClaim": "foo"}, "bar": {"hostPath": False}},
            },
            {
                "repos": {"hostPath": "foo"},
                "data": {
                    "foo": {"existingClaim": "foo", "hostPath": "foo"},
                    "bar": {"hostPath": "foo"},
                },
            },
            {"upload": {"hostPath": "test"}, "data": {"hostPath": "test"}},
            {"logs": {"hostPath": "test"}, "outputs": {"existingClaim": "foo"}},
            {"logs": {"hostPath": 123}, "outputs": {"foo": {"existingClaim": "foo"}}},
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                PersistenceConfig.from_dict(config_dict)

        config_dicts = [
            {},
            {"repos": {"existingClaim": "foo"}, "outputs": {}},
            {"upload": {}, "outputs": {}},
            {"logs": {}},
            {"repos": {}},
            {"upload": {}},
            {
                "logs": {"existingClaim": "foo"},
                "data": {},
                "outputs": {
                    "foo": {"existingClaim": "foo"},
                    "bar": {"hostPath": "foo"},
                },
            },
            {
                "repos": {"existingClaim": "foo"},
                "logs": {"existingClaim": "foo"},
                "data": {
                    "foo": {"existingClaim": "foo"},
                    "bar": {"hostPath": "bar", "readOnly": True},
                    "moo": {"store": "s3"},
                },
                "outputs": {"foo": {"existingClaim": "foo"}},
            },
        ]

        for config_dict in config_dicts:
            config = PersistenceConfig.from_dict(config_dict)
            assert config.to_light_dict() == config_dict
