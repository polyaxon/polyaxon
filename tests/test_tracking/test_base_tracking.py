# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from tests.utils import TestEnvVarsCase

from polyaxon_client.tracking.base import BaseTracker


class TestTracker(TestEnvVarsCase):
    def test_empty_outputs_path(self):
        self.check_empty_value('POLYAXON_RUN_OUTPUTS_PATH', BaseTracker.get_outputs_path)

    def test_valid_outputs_path(self):
        self.check_valid_value('POLYAXON_RUN_OUTPUTS_PATH', BaseTracker.get_outputs_path, 'path')

    def test_empty_data_path(self):
        self.check_empty_value('POLYAXON_RUN_DATA_PATHS', BaseTracker.get_data_paths)

    def test_valid_data_path(self):
        self.check_valid_dict_value('POLYAXON_RUN_DATA_PATHS', BaseTracker.get_data_paths,
                                    {'data': 'path'})

    def test_empty_outputs_refs_paths(self):
        self.check_empty_value('POLYAXON_REFS_OUTPUTS_PATHS', BaseTracker.get_outputs_refs_paths)

    def test_valid_outputs_refs_paths(self):
        self.check_valid_dict_value('POLYAXON_REFS_OUTPUTS_PATHS',
                                    BaseTracker.get_outputs_refs_paths,
                                    {
                                        'jobs': ['path1', 'path12'],
                                        'experiments': ['path1', 'path12']
                                    })

    def test_empty_log_level(self):
        self.check_empty_value('POLYAXON_LOG_LEVEL', BaseTracker.get_log_level)

    def test_valid_log_level(self):
        self.check_valid_value('POLYAXON_LOG_LEVEL', BaseTracker.get_log_level, 'info')
