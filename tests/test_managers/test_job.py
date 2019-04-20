# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_cli.managers.job import JobManager
from polyaxon_cli.schemas import JobConfig


class TestJobManager(TestCase):
    def test_default_props(self):
        assert JobManager.IS_GLOBAL is False
        assert JobManager.IS_POLYAXON_DIR is True
        assert JobManager.CONFIG_FILE_NAME == '.polyaxonjob'
        assert JobManager.CONFIG == JobConfig
