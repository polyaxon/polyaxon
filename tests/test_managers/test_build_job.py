# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_cli.managers.build_job import BuildJobManager
from polyaxon_cli.schemas import BuildJobConfig


class TestBuildJobManager(TestCase):
    def test_default_props(self):
        assert BuildJobManager.IS_GLOBAL is False
        assert BuildJobManager.IS_POLYAXON_DIR is True
        assert BuildJobManager.CONFIG_FILE_NAME == '.polyaxonbuild'
        assert BuildJobManager.CONFIG == BuildJobConfig
