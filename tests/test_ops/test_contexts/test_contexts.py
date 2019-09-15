# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from tests.utils import assert_equal_dict

from polyaxon_schemas.ops.contexts import ContextsConfig


@pytest.mark.contexts_mark
class TestContextsConfigs(TestCase):
    def test_context_config(self):
        config_dict = {}
        config = ContextsConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add secrets
        config_dict["secrets"] = [{"name": "secret1"}, {"name": "secret2"}]
        config = ContextsConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add config_maps
        config_dict["config_maps"] = [{"name": "config_map1"}, {"name": "config_map2"}]
        config = ContextsConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add artifact_refs
        config_dict["artifacts"] = [
            {"name": "data2", "managed": False},
            {"name": "data3", "paths": ["/subpath1", "subpath2"], "managed": True},
            {"name": "artifact2", "paths": ["/subpath1", "subpath2"], "managed": True},
        ]
        config = ContextsConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add repos
        config_dict["repos"] = [
            {"name": "repo1"},
            {"name": "repo1", "commit": "commit-hash"},
            {"name": "repo2", "branch": "dev"},
        ]
        config = ContextsConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())
