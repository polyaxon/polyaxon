# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_cli.managers.experiment_job import ExperimentJobManager
from polyaxon_cli.schemas import ExperimentJobConfig


class TestExperimentJobManager(TestCase):
    def test_default_props(self):
        assert ExperimentJobManager.IS_GLOBAL is False
        assert ExperimentJobManager.IS_POLYAXON_DIR is True
        assert ExperimentJobManager.CONFIG_FILE_NAME == '.polyaxonxpjob'
        assert ExperimentJobManager.CONFIG == ExperimentJobConfig
