# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from hestia.env_var_keys import (
    POLYAXON_KEYS_ARTIFACTS_PATHS,
    POLYAXON_KEYS_OUTPUTS_PATH,
    POLYAXON_KEYS_LOG_LEVEL)
from tests.utils import TestEnvVarsCase

from polyaxon import settings
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.tracking import paths


class TestTracker(TestEnvVarsCase):
    def test_empty_base_outputs_path(self):
        self.check_empty_value(
            "POLYAXON_BASE_OUTPUTS_PATH", paths.get_base_outputs_path
        )

    def test_valid_base_outputs_path(self):
        self.check_valid_value(
            "POLYAXON_BASE_OUTPUTS_PATH", paths.get_base_outputs_path, "path"
        )

    def test_get_outputs_raises_out_cluster(self):
        settings.CLIENT_CONFIG.is_managed = False
        with self.assertRaises(PolyaxonClientException):
            paths.get_outputs_path()

    def test_empty_outputs_path(self):
        settings.CLIENT_CONFIG.is_managed = True
        self.check_empty_value(POLYAXON_KEYS_OUTPUTS_PATH, paths.get_outputs_path)

    def test_valid_outputs_path(self):
        settings.CLIENT_CONFIG.is_managed = True
        self.check_valid_value(
            POLYAXON_KEYS_OUTPUTS_PATH, paths.get_outputs_path, "path"
        )

    def test_get_artifacts_paths_raises_out_cluster(self):
        settings.CLIENT_CONFIG.is_managed = False
        with self.assertRaises(PolyaxonClientException):
            paths.get_artifacts_paths()

    def test_empty_artifacts_path(self):
        settings.CLIENT_CONFIG.is_managed = True
        self.check_empty_value(POLYAXON_KEYS_ARTIFACTS_PATHS, paths.get_artifacts_paths)

    def test_valid_artifacts_path(self):
        settings.CLIENT_CONFIG.is_managed = True
        self.check_valid_dict_value(
            POLYAXON_KEYS_ARTIFACTS_PATHS, paths.get_artifacts_paths, {"data": "path"}
        )

    def test_get_log_level_raises_out_cluster(self):
        settings.CLIENT_CONFIG.is_managed = False
        with self.assertRaises(PolyaxonClientException):
            paths.get_log_level()

    def test_empty_log_level(self):
        settings.CLIENT_CONFIG.is_managed = True
        self.check_empty_value(POLYAXON_KEYS_LOG_LEVEL, paths.get_log_level)

    def test_valid_log_level(self):
        settings.CLIENT_CONFIG.is_managed = True
        self.check_valid_value(POLYAXON_KEYS_LOG_LEVEL, paths.get_log_level, "info")
