# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_cli.managers.experiment import ExperimentManager
from polyaxon_cli.schemas import ExperimentConfig


class TestExperimentManager(TestCase):
    def test_default_props(self):
        assert ExperimentManager.IS_GLOBAL is False
        assert ExperimentManager.IS_POLYAXON_DIR is True
        assert ExperimentManager.CONFIG_FILE_NAME == '.polyaxonxp'
        assert ExperimentManager.CONFIG == ExperimentConfig
