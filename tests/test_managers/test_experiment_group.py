# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon.managers.experiment_group import GroupManager
from polyaxon.schemas import GroupConfig


class TestGroupManager(TestCase):
    def test_default_props(self):
        assert GroupManager.IS_GLOBAL is False
        assert GroupManager.IS_POLYAXON_DIR is True
        assert GroupManager.CONFIG_FILE_NAME == '.polyaxongroup'
        assert GroupManager.CONFIG == GroupConfig
