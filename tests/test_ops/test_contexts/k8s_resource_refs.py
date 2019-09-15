# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from marshmallow import ValidationError
from tests.utils import assert_equal_dict

from polyaxon_schemas.ops.contexts.artifact_refs import ArtifactRefConfig


@pytest.mark.contexts_mark
class TestK8SResourceConfigs(TestCase):
    def test_k8s_resource_config(self):
        config_dict = {"name": "foo"}
        config = ArtifactRefConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"name": "foo", "managed": 213}
        with self.assertRaises(ValidationError):
            ArtifactRefConfig.from_dict(config_dict)

        config_dict = {"name": "foo", "paths": 213}
        with self.assertRaises(ValidationError):
            ArtifactRefConfig.from_dict(config_dict)

        config_dict = {"name": "foo", "managed": True, "paths": ["item1", "item2"]}
        config = ArtifactRefConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"name": "foo", "paths": ["item1", "item2"]}
        config = ArtifactRefConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
