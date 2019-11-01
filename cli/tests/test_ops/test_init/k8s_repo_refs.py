# coding: utf-8
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from marshmallow import ValidationError
from tests.utils import assert_equal_dict

from polyaxon.schemas.ops.mounts.repo_refs import RepoRefConfig


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
