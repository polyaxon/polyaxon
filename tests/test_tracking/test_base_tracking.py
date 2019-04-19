# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from tests.utils import TestEnvVarsCase

from polyaxon_client import settings
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.tracking import paths


class TestTracker(TestEnvVarsCase):
    def test_empty_base_outputs_path(self):
        self.check_empty_value('POLYAXON_BASE_OUTPUTS_PATH', paths.get_base_outputs_path)

    def test_valid_base_outputs_path(self):
        self.check_valid_value('POLYAXON_BASE_OUTPUTS_PATH', paths.get_base_outputs_path, 'path')

    def test_get_outputs_raises_out_cluster(self):
        settings.IS_MANAGED = False
        with self.assertRaises(PolyaxonClientException):
            paths.get_outputs_path()

    def test_empty_outputs_path(self):
        settings.IS_MANAGED = True
        self.check_empty_value('POLYAXON_RUN_OUTPUTS_PATH', paths.get_outputs_path)

    def test_valid_outputs_path(self):
        settings.IS_MANAGED = True
        self.check_valid_value('POLYAXON_RUN_OUTPUTS_PATH', paths.get_outputs_path, 'path')

    def test_get_data_paths_raises_out_cluster(self):
        settings.IS_MANAGED = False
        with self.assertRaises(PolyaxonClientException):
            paths.get_data_paths()

    def test_empty_data_path(self):
        settings.IS_MANAGED = True
        self.check_empty_value('POLYAXON_RUN_DATA_PATHS', paths.get_data_paths)

    def test_valid_data_path(self):
        settings.IS_MANAGED = True
        self.check_valid_dict_value('POLYAXON_RUN_DATA_PATHS', paths.get_data_paths,
                                    {'data': 'path'})

    def test_get_outputs_refs_paths_raises_out_cluster(self):
        settings.IS_MANAGED = False
        with self.assertRaises(PolyaxonClientException):
            paths.get_outputs_refs_paths()

    def test_empty_outputs_refs_paths(self):
        settings.IS_MANAGED = True
        self.check_empty_value('POLYAXON_REFS_OUTPUTS_PATHS', paths.get_outputs_refs_paths)

    def test_valid_outputs_refs_paths(self):
        settings.IS_MANAGED = True
        self.check_valid_dict_value('POLYAXON_REFS_OUTPUTS_PATHS',
                                    paths.get_outputs_refs_paths,
                                    {
                                        'jobs': ['path1', 'path12'],
                                        'experiments': ['path1', 'path12']
                                    })

    def test_get_log_level_raises_out_cluster(self):
        settings.IS_MANAGED = False
        with self.assertRaises(PolyaxonClientException):
            paths.get_log_level()

    def test_empty_log_level(self):
        settings.IS_MANAGED = True
        self.check_empty_value('POLYAXON_LOG_LEVEL', paths.get_log_level)

    def test_valid_log_level(self):
        settings.IS_MANAGED = True
        self.check_valid_value('POLYAXON_LOG_LEVEL', paths.get_log_level, 'info')
