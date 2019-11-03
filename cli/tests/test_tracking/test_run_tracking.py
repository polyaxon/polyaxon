#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8
from __future__ import absolute_import, division, print_function

import uuid

from tests.utils import TestEnvVarsCase

from polyaxon import settings
from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_ARTIFACTS_PATHS,
    POLYAXON_KEYS_LOG_LEVEL,
    POLYAXON_KEYS_OUTPUTS_PATH,
    POLYAXON_KEYS_RUN_INSTANCE,
)
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.tracking import paths
from polyaxon.tracking.run import Run


class TestExperimentTracking(TestEnvVarsCase):
    def setUp(self):
        super(TestExperimentTracking, self).setUp()
        settings.CLIENT_CONFIG.is_managed = True

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

    def test_run_info_checks_is_managed(self):
        settings.CLIENT_CONFIG.is_managed = False
        with self.assertRaises(PolyaxonClientException):
            Run.get_run_info()

    def test_empty_run_info(self):
        self.check_raise_for_invalid_value(
            POLYAXON_KEYS_RUN_INSTANCE, Run.get_run_info, None, PolyaxonClientException
        )

    def test_non_valid_run_info(self):
        self.check_raise_for_invalid_value(
            POLYAXON_KEYS_RUN_INSTANCE,
            Run.get_run_info,
            "something random",
            PolyaxonClientException,
        )

        self.check_raise_for_invalid_value(
            POLYAXON_KEYS_RUN_INSTANCE,
            Run.get_run_info,
            "foo.bar",
            PolyaxonClientException,
        )

    def test_dict_run_info(self):
        uid = uuid.uuid4().hex
        run_info = "user.project_bar.runs.{}".format(uid)
        self.check_valid_value(
            POLYAXON_KEYS_RUN_INSTANCE,
            Run.get_run_info,
            run_info,
            ("user", "project_bar", uid),
        )
