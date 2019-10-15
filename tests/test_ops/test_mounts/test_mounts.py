# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from tests.utils import assert_equal_dict

from schemas.ops.mounts import MountsConfig


@pytest.mark.mounts_mark
class TestMountsConfigs(TestCase):
    def test_context_config(self):
        config_dict = {}
        config = MountsConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add secrets
        config_dict["secrets"] = [{"name": "secret1"}, {"name": "secret2"}]
        config = MountsConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add config_maps
        config_dict["config_maps"] = [{"name": "config_map1"}, {"name": "config_map2"}]
        config = MountsConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add artifact_refs
        config_dict["artifacts"] = [
            {"name": "data2"},
            {"name": "data3", "paths": ["/subpath1", "subpath2"]},
            {"name": "artifact2", "paths": ["/subpath1", "subpath2"]},
        ]
        config = MountsConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())
