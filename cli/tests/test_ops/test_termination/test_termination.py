# coding: utf-8
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from tests.utils import assert_equal_dict

from polyaxon.schemas.ops.termination import TerminationConfig


@pytest.mark.termination_mark
class TestTerminationConfigs(TestCase):
    def test_termination_config(self):
        config_dict = {}
        config = TerminationConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add max_retries
        config_dict["max_retries"] = 4
        config = TerminationConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add timeout
        config_dict["timeout"] = 4
        config = TerminationConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add restart_policy
        config_dict["restart_policy"] = "never"
        config = TerminationConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add ttl
        config_dict["ttl"] = 40
        config = TerminationConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())
