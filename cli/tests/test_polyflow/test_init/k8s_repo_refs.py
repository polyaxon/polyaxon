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

import pytest

from marshmallow import ValidationError
from tests.utils import assert_equal_dict

from polyaxon.schemas.polyflow.init.repo_refs import RepoRefConfig


@pytest.mark.init_mark
class TestRepoConfigs(TestCase):
    def test_repo_config(self):
        config_dict = {"name": "foo"}
        config = RepoRefConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"name": "foo", "commit": 213}
        with self.assertRaises(ValidationError):
            RepoRefConfig.from_dict(config_dict)

        config_dict = {"name": "foo", "branch": 213}
        with self.assertRaises(ValidationError):
            RepoRefConfig.from_dict(config_dict)

        config_dict = {"name": "foo", "commit": "commit-hash"}
        config = RepoRefConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"name": "foo", "branch": "dev"}
        config = RepoRefConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
