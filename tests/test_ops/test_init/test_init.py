# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from polyaxon_schemas.ops.init import InitConfig
from tests.utils import assert_equal_dict


@pytest.mark.init_mark
class TestInitConfigs(TestCase):
    def test_init_config(self):
        config_dict = {}
        config = InitConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add artifact_refs
        config_dict["artifacts"] = [
            {"name": "data2"},
            {"name": "data3", "paths": ["/subpath1", "subpath2"]},
            {"name": "artifact2", "paths": ["/subpath1", "subpath2"]},
        ]
        config = InitConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add repos
        config_dict["repos"] = [
            {"name": "repo1"},
            {"name": "repo1", "commit": "commit-hash"},
            {"name": "repo2", "branch": "dev"},
        ]
        config = InitConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add build context
        config_dict = {
            "build": {
                "image": "tensorflow:1.3.0",
                "build_steps": ["pip install tensor2tensor"],
                "env_vars": [["LC_ALL", "en_US.UTF-8"]],
            }
        }
        config = InitConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())
