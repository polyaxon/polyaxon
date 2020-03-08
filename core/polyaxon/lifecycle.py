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
import polyaxon_sdk

from polyaxon.utils.tz_utils import now

V1Statuses = polyaxon_sdk.V1Statuses


class StatusColor:
    GREEN = "#1aaa55"
    RED = "#aa310f"
    BLUE = "#2e77aa"
    YELLOW = "#aa9e4a"
    GREY = "#485563"

    @classmethod
    def get_color(cls, status: str) -> str:
        if status in [
            V1Statuses.FAILED,
            V1Statuses.STOPPED,
            V1Statuses.UPSTREAM_FAILED,
        ]:
            return cls.RED
        if status == V1Statuses.SUCCEEDED:
            return cls.GREEN

        if status == V1Statuses.SKIPPED:
            return cls.GREY

        if LifeCycle.is_done(status):
            return cls.GREY

        return cls.YELLOW


class LifeCycle:
    CHOICES = (
        (V1Statuses.CREATED, V1Statuses.CREATED),
        (V1Statuses.RESUMING, V1Statuses.RESUMING),
        (V1Statuses.WARNING, V1Statuses.WARNING),
        (V1Statuses.UNSCHEDULABLE, V1Statuses.UNSCHEDULABLE),
        (V1Statuses.QUEUED, V1Statuses.QUEUED),
        (V1Statuses.SCHEDULED, V1Statuses.SCHEDULED),
        (V1Statuses.STARTING, V1Statuses.STARTING),
        (V1Statuses.RUNNING, V1Statuses.RUNNING),
        (V1Statuses.SUCCEEDED, V1Statuses.SUCCEEDED),
        (V1Statuses.FAILED, V1Statuses.FAILED),
        (V1Statuses.UPSTREAM_FAILED, V1Statuses.UPSTREAM_FAILED),
        (V1Statuses.STOPPING, V1Statuses.STOPPING),
        (V1Statuses.STOPPED, V1Statuses.STOPPED),
        (V1Statuses.SKIPPED, V1Statuses.SKIPPED),
        (V1Statuses.RETRYING, V1Statuses.RETRYING),
        (V1Statuses.UNKNOWN, V1Statuses.UNKNOWN),
    )
    VALUES = {
        V1Statuses.CREATED,
        V1Statuses.RESUMING,
        V1Statuses.WARNING,
        V1Statuses.UNSCHEDULABLE,
        V1Statuses.QUEUED,
        V1Statuses.SCHEDULED,
        V1Statuses.STARTING,
        V1Statuses.RUNNING,
        V1Statuses.SUCCEEDED,
        V1Statuses.FAILED,
        V1Statuses.UPSTREAM_FAILED,
        V1Statuses.STOPPING,
        V1Statuses.STOPPED,
        V1Statuses.SKIPPED,
        V1Statuses.RETRYING,
        V1Statuses.UNKNOWN,
    }
    WARNING_VALUES = {V1Statuses.UNSCHEDULABLE, V1Statuses.WARNING}
    PENDING_VALUES = {
        V1Statuses.CREATED,
        V1Statuses.RESUMING,
        V1Statuses.SCHEDULED,
    }
    SCHEDULABLE_VALUES = {
        V1Statuses.CREATED,
        V1Statuses.RESUMING,
        V1Statuses.RETRYING,
    }
    RUNNING_VALUES = {V1Statuses.STARTING, V1Statuses.RUNNING}
    DONE_VALUES = {
        V1Statuses.FAILED,
        V1Statuses.UPSTREAM_FAILED,
        V1Statuses.STOPPED,
        V1Statuses.SKIPPED,
        V1Statuses.SUCCEEDED,
    }

    @classmethod
    def can_check_heartbeat(cls, status: str) -> bool:
        return status in LifeCycle.RUNNING_VALUES

    @classmethod
    def is_unschedulable(cls, status: str) -> bool:
        return status == V1Statuses.UNSCHEDULABLE

    @classmethod
    def is_warning(cls, status: str) -> bool:
        return status in cls.WARNING_VALUES

    @classmethod
    def is_pending(cls, status: str) -> bool:
        return status in cls.PENDING_VALUES

    @classmethod
    def is_queued(cls, status: str) -> bool:
        return status == V1Statuses.QUEUED

    @classmethod
    def is_starting(cls, status: str) -> bool:
        return status == V1Statuses.STARTING

    @classmethod
    def is_running(cls, status: str) -> bool:
        return status in LifeCycle.RUNNING_VALUES

    @classmethod
    def is_unknown(cls, status: str) -> bool:
        return status == V1Statuses.UNKNOWN

    @classmethod
    def is_k8s_stoppable(cls, status: str) -> bool:
        return (
            cls.is_running(status=status)
            or cls.is_unschedulable(status=status)
            or cls.is_warning(status=status)
            or cls.is_unknown(status=status)
        )

    @classmethod
    def is_stoppable(cls, status: str) -> bool:
        return not cls.is_done(status)

    @classmethod
    def is_stopping(cls, status: str) -> bool:
        return status == V1Statuses.STOPPING

    @classmethod
    def is_done(cls, status: str) -> bool:
        return status in cls.DONE_VALUES

    @classmethod
    def failed(cls, status: str) -> bool:
        return status == V1Statuses.FAILED or status == V1Statuses.UPSTREAM_FAILED

    @classmethod
    def succeeded(cls, status: str) -> bool:
        return status == V1Statuses.SUCCEEDED

    @classmethod
    def stopped(cls, status: str) -> bool:
        return status == V1Statuses.STOPPED

    @classmethod
    def skipped(cls, status: str) -> bool:
        return status == V1Statuses.SKIPPED


class V1StatusCondition(polyaxon_sdk.V1StatusCondition):
    @classmethod
    def get_condition(
        cls,
        type=None,  # noqa
        status=None,
        last_update_time=None,
        last_transition_time=None,
        reason=None,
        message=None,
    ) -> "V1StatusCondition":
        current_time = now()
        last_update_time = last_update_time or current_time
        last_transition_time = last_transition_time or current_time
        return cls(
            type=type.lower() if type else type,
            status=status,
            last_update_time=last_update_time,
            last_transition_time=last_transition_time,
            reason=reason,
            message=message,
        )

    def __eq__(self, other: "V1StatusCondition"):
        return (
            self.type == other.type
            and self.status == other.status
            and self.reason == self.reason
            and self.message == self.message
        )
