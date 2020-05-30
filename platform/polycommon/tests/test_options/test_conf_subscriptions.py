#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

from polycommon import conf
from polycommon.options.registry import (
    containers,
    core,
    installation,
    k8s,
    scheduler,
    stats,
)


class TestConfSubscriptions(TestCase):
    def setUp(self):
        super().setUp()
        conf.validate_and_setup()
        # load subscriptions
        import polycommon.options.conf_subscriptions  # noqa

    def _assert_options_subscriptions(self, options):
        for option in options:
            assert conf.option_manager.knows(option)

    def test_core_subscriptions(self):
        self._assert_options_subscriptions(core.OPTIONS)

    def test_installation_subscriptions(self):
        self._assert_options_subscriptions(installation.OPTIONS)

    def test_k8s_subscriptions(self):
        self._assert_options_subscriptions(k8s.OPTIONS)

    def test_scheduler_subscriptions(self):
        self._assert_options_subscriptions(scheduler.OPTIONS)

    def test_containers_subscriptions(self):
        self._assert_options_subscriptions(containers.OPTIONS)

    def test_stats_subscriptions(self):
        self._assert_options_subscriptions(stats.OPTIONS)
