# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_sdk import V1Project

from polyaxon.managers.project import ProjectManager


class TestProjectManager(TestCase):
    def test_default_props(self):
        assert ProjectManager.IS_GLOBAL is False
        assert ProjectManager.IS_POLYAXON_DIR is True
        assert ProjectManager.CONFIG_FILE_NAME == ".polyaxonproject"
        assert ProjectManager.CONFIG == V1Project
