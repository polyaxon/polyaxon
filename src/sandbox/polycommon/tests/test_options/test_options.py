#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

from unittest import TestCase

from polycommon.options.registry import core, scheduler


class TestOptions(TestCase):
    def test_options_core(self):
        assert core.Logging.default is None
        assert core.Logging.is_global() is True
        assert core.Logging.is_optional is False
        assert core.Logging.get_key_subject() == "LOGGING"
        assert core.Logging.get_namespace() is None
        assert core.UiAdminEnabled.default is True
        assert core.UiAdminEnabled.is_global() is True
        assert core.UiAdminEnabled.is_optional is True
        assert core.UiAdminEnabled.get_key_subject() == "UI_ADMIN_ENABLED"
        assert core.UiBaseUrl.get_key_subject() == "UI_BASE_URL"
        assert core.UiAssetsVersion.get_key_subject() == "UI_ASSETS_VERSION"
        assert core.UiAdminEnabled.get_namespace() is None

    def test_options_scheduler(self):
        assert scheduler.SchedulerCountdown.get_namespace() is None
        assert (
            scheduler.SchedulerCountdown.get_key_subject()
            == "SCHEDULER_GLOBAL_COUNTDOWN"
        )
