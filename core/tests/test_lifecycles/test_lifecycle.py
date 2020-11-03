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
from polyaxon.lifecycle import LifeCycle, V1Statuses
from tests.utils import BaseTestCase


class TestStatusesTransition(BaseTestCase):
    def test_values(self):
        assert len(V1Statuses.allowable_values) == 20

    def test_warning_statuses(self):
        assert LifeCycle.WARNING_VALUES == {
            V1Statuses.WARNING,
            V1Statuses.UNSCHEDULABLE,
        }

    def test_pending_statuses(self):
        assert LifeCycle.PENDING_VALUES == {
            V1Statuses.CREATED,
            V1Statuses.RESUMING,
            V1Statuses.SCHEDULED,
        }

    def test_running_statuses(self):
        assert LifeCycle.RUNNING_VALUES == {
            V1Statuses.INITIALIZING,
            V1Statuses.PROCESSING,
            V1Statuses.STARTING,
            V1Statuses.RUNNING,
        }

    def test_done_statuses(self):
        assert LifeCycle.DONE_VALUES == {
            V1Statuses.FAILED,
            V1Statuses.UPSTREAM_FAILED,
            V1Statuses.SUCCEEDED,
            V1Statuses.STOPPED,
            V1Statuses.SKIPPED,
        }

    def test_can_check_heartbeat(self):
        assert LifeCycle.can_check_heartbeat(None) is False
        for status in V1Statuses.allowable_values:
            if LifeCycle.is_running(status):
                assert LifeCycle.can_check_heartbeat(status) is True
            else:
                assert LifeCycle.can_check_heartbeat(status) is False

    def test_is_unschedulable(self):
        assert LifeCycle.is_unschedulable(None) is False
        for status in V1Statuses.allowable_values:
            if status == V1Statuses.UNSCHEDULABLE:
                assert LifeCycle.is_unschedulable(status) is True
            else:
                assert LifeCycle.is_unschedulable(status) is False

    def test_is_compilable(self):
        assert LifeCycle.is_unschedulable(None) is False
        for status in V1Statuses.allowable_values:
            if status in LifeCycle.COMPILABLE_VALUES:
                assert LifeCycle.is_compilable(status) is True
            else:
                assert LifeCycle.is_compilable(status) is False

    def test_is_warning(self):
        assert LifeCycle.is_warning(None) is False
        for status in V1Statuses.allowable_values:
            if status in LifeCycle.WARNING_VALUES:
                assert LifeCycle.is_warning(status) is True
            else:
                assert LifeCycle.is_warning(status) is False

    def test_is_pending(self):
        assert LifeCycle.is_pending(None) is False
        for status in V1Statuses.allowable_values:
            if status in LifeCycle.PENDING_VALUES:
                assert LifeCycle.is_pending(status) is True
            else:
                assert LifeCycle.is_pending(status) is False

    def test_is_starting(self):
        assert LifeCycle.is_starting(None) is False
        for status in V1Statuses.allowable_values:
            if status == V1Statuses.STARTING:
                assert LifeCycle.is_starting(status) is True
            else:
                assert LifeCycle.is_starting(status) is False

    def test_is_running(self):
        assert LifeCycle.is_running(None) is False
        for status in V1Statuses.allowable_values:
            if status in LifeCycle.RUNNING_VALUES:
                assert LifeCycle.is_running(status) is True
            else:
                assert LifeCycle.is_running(status) is False

    def test_is_unknown(self):
        assert LifeCycle.is_unknown(None) is False
        for status in V1Statuses.allowable_values:
            if status == V1Statuses.UNKNOWN:
                assert LifeCycle.is_unknown(status) is True
            else:
                assert LifeCycle.is_unknown(status) is False

    def test_is_k8s_stoppable(self):
        assert LifeCycle.is_k8s_stoppable(None) is False
        for status in V1Statuses.allowable_values:
            cond = (
                LifeCycle.is_running(status)
                or LifeCycle.is_unschedulable(status)
                or LifeCycle.is_warning(status=status)
                or LifeCycle.is_unknown(status=status)
            )
            if cond:
                assert LifeCycle.is_k8s_stoppable(status) is True
            else:
                assert LifeCycle.is_k8s_stoppable(status) is False

    def is_stopping(self):
        assert LifeCycle.is_stopping(None) is False
        for status in V1Statuses.allowable_values:
            if status == V1Statuses.STOPPING:
                assert LifeCycle.is_stopping(status) is True
            else:
                assert LifeCycle.is_stopping(status) is False

    def test_is_stoppable(self):
        assert LifeCycle.is_stoppable(None) is True
        for status in V1Statuses.allowable_values:
            if not LifeCycle.is_done(status):
                assert LifeCycle.is_stoppable(status) is True
            else:
                assert LifeCycle.is_stoppable(status) is False

    def test_is_done(self):
        assert LifeCycle.is_done(None) is False
        for status in V1Statuses.allowable_values:
            if status in LifeCycle.DONE_VALUES:
                assert LifeCycle.is_done(status) is True
            else:
                assert LifeCycle.is_done(status) is False

    def test_succeeded(self):
        assert LifeCycle.succeeded(None) is False
        for status in V1Statuses.allowable_values:
            if status == V1Statuses.SUCCEEDED:
                assert LifeCycle.succeeded(status) is True
            else:
                assert LifeCycle.succeeded(status) is False

    def test_failed(self):
        assert LifeCycle.failed(None) is False
        for status in V1Statuses.allowable_values:
            if status in {V1Statuses.FAILED, V1Statuses.UPSTREAM_FAILED}:
                assert LifeCycle.failed(status) is True
            else:
                assert LifeCycle.failed(status) is False

    def test_skipped(self):
        assert LifeCycle.skipped(None) is False
        for status in V1Statuses.allowable_values:
            if status == V1Statuses.SKIPPED:
                assert LifeCycle.skipped(status) is True
            else:
                assert LifeCycle.skipped(status) is False
