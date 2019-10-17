# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_sdk import V1Run

from polyaxon.managers.run import RunManager


class TestRunManager(TestCase):
    def test_default_props(self):
        assert RunManager.IS_GLOBAL is False
        assert RunManager.IS_POLYAXON_DIR is True
        assert RunManager.CONFIG_FILE_NAME == ".polyaxonrun"
        assert RunManager.CONFIG == V1Run
