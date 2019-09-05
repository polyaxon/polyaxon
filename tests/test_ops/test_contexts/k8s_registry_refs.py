# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from tests.utils import assert_equal_dict

from polyaxon_schemas.ops.contexts.registry_refs import RegistryRefConfig


@pytest.mark.contexts_mark
class TestRegistryConfigs(TestCase):
    def test_registry_config(self):
        config_dict = {"name": "foo"}
        config = RegistryRefConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
