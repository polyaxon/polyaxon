# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from marshmallow import ValidationError
from tests.utils import assert_equal_dict

from schemas.ops.mounts.artifact_refs import ArtifactRefConfig


@pytest.mark.mounts_mark
class TestArtifactConfigs(TestCase):
    def test_artifact_config(self):
        config_dict = {"name": "foo"}
        config = ArtifactRefConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"name": "foo", "mount_path": 213}
        with self.assertRaises(ValidationError):
            ArtifactRefConfig.from_dict(config_dict)

        config_dict = {"name": "foo", "items": 213}
        with self.assertRaises(ValidationError):
            ArtifactRefConfig.from_dict(config_dict)

        config_dict = {
            "name": "foo",
            "mount_path": "/foo/path",
            "items": ["item1", "item2"],
        }
        config = ArtifactRefConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"name": "foo", "items": ["item1", "item2"]}
        config = ArtifactRefConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
