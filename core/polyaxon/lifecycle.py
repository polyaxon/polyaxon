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


class V1Statuses(polyaxon_sdk.V1Statuses):
    """Status is the information that represents the current state of a run.

    By examining a run status and/or the history of its statuses,
    you can learn what stage the run is at, and what stages are left.

    The supported statuses by Polyaxon.

    Enum:
        CREATED: "created"
        RESUMING: "resuming"
        WARNING: "warning"
        UNSCHEDULABLE: "unschedulable"
        COMPILED: "compiled"
        QUEUED: "queued"
        SCHEDULED: "scheduled"
        STARTING: "starting"
        RUNNING: "running"
        SUCCEEDED: "succeeded"
        FAILED: "failed"
        UPSTREAM_FAILED: "upstream_failed"
        STOPPING: "stopping"
        STOPPED: "stopped"
        SKIPPED: "skipped"
        RETRYING: "retrying"
        UNKNOWN: "unknown"
    """


class StatusColor:
    """The statuses colors.

    Enum:
        GREEN: #1aaa55
        RED: #aa310f
        BLUE: #2e77aa
        YELLOW: #aa9e4a
        GREY: #485563
    """

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
    """The Run LifeCycle is state machine for status transition."""

    CHOICES = (
        (V1Statuses.CREATED, V1Statuses.CREATED),
        (V1Statuses.RESUMING, V1Statuses.RESUMING),
        (V1Statuses.WARNING, V1Statuses.WARNING),
        (V1Statuses.UNSCHEDULABLE, V1Statuses.UNSCHEDULABLE),
        (V1Statuses.COMPILED, V1Statuses.COMPILED),
        (V1Statuses.QUEUED, V1Statuses.QUEUED),
        (V1Statuses.SCHEDULED, V1Statuses.SCHEDULED),
        (V1Statuses.STARTING, V1Statuses.STARTING),
        (V1Statuses.RUNNING, V1Statuses.RUNNING),
        (V1Statuses.INITIALIZING, V1Statuses.INITIALIZING),
        (V1Statuses.PROCESSING, V1Statuses.PROCESSING),
        (V1Statuses.SUCCEEDED, V1Statuses.SUCCEEDED),
        (V1Statuses.FAILED, V1Statuses.FAILED),
        (V1Statuses.UPSTREAM_FAILED, V1Statuses.UPSTREAM_FAILED),
        (V1Statuses.STOPPING, V1Statuses.STOPPING),
        (V1Statuses.STOPPED, V1Statuses.STOPPED),
        (V1Statuses.SKIPPED, V1Statuses.SKIPPED),
        (V1Statuses.RETRYING, V1Statuses.RETRYING),
        (V1Statuses.UNKNOWN, V1Statuses.UNKNOWN),
    )
    WARNING_VALUES = {V1Statuses.UNSCHEDULABLE, V1Statuses.WARNING}
    PENDING_VALUES = {
        V1Statuses.CREATED,
        V1Statuses.RESUMING,
        V1Statuses.SCHEDULED,
    }
    COMPILABLE_VALUES = {
        V1Statuses.CREATED,
        V1Statuses.RESUMING,
        V1Statuses.RETRYING,
    }
    RUNNING_VALUES = {
        V1Statuses.STARTING,
        V1Statuses.INITIALIZING,
        V1Statuses.PROCESSING,
        V1Statuses.RUNNING,
    }
    ON_K8S_VALUES = RUNNING_VALUES | WARNING_VALUES | {V1Statuses.UNKNOWN}
    DONE_VALUES = {
        V1Statuses.FAILED,
        V1Statuses.UPSTREAM_FAILED,
        V1Statuses.STOPPED,
        V1Statuses.SKIPPED,
        V1Statuses.SUCCEEDED,
    }
    DONE_OR_IN_PROGRESS_VALUES = DONE_VALUES | {
        V1Statuses.STOPPING,
    }

    @classmethod
    def can_check_heartbeat(cls, status: str) -> bool:
        """Checks if a run with this status is in a state that allows to check for a heartbeat."""
        return status in cls.RUNNING_VALUES

    @classmethod
    def is_unschedulable(cls, status: str) -> bool:
        """Checks if a run with this status is unschedulable."""
        return status == V1Statuses.UNSCHEDULABLE

    @classmethod
    def is_processing(cls, status: str) -> bool:
        """Checks if a run with this status is processing."""
        return status == V1Statuses.PROCESSING

    @classmethod
    def is_warning(cls, status: str) -> bool:
        """Checks if a run with this status is in a warning status."""
        return status in cls.WARNING_VALUES

    @classmethod
    def is_pending(cls, status: str) -> bool:
        """Checks if a run with this status is in a pending status."""
        return status in cls.PENDING_VALUES

    @classmethod
    def is_compiled(cls, status: str) -> bool:
        """Checks if a run with this status is compiled."""
        return status == V1Statuses.COMPILED

    @classmethod
    def is_compilable(cls, status: str) -> bool:
        """Checks if a run with this status is compilable."""
        return status in cls.COMPILABLE_VALUES

    @classmethod
    def is_queued(cls, status: str) -> bool:
        """Checks if a run with this status is queued."""
        return status == V1Statuses.QUEUED

    @classmethod
    def is_starting(cls, status: str) -> bool:
        """Checks if a run with this status is starting."""
        return status == V1Statuses.STARTING

    @classmethod
    def is_running(cls, status: str) -> bool:
        """Checks if a run with this status is running."""
        return status in cls.RUNNING_VALUES

    @classmethod
    def is_unknown(cls, status: str) -> bool:
        """Checks if a run with this status is in an unknown state."""
        return status == V1Statuses.UNKNOWN

    @classmethod
    def is_k8s_stoppable(cls, status: str) -> bool:
        """Checks if a run with this status is scheduled on k8s and is stoppable."""
        return status in cls.ON_K8S_VALUES

    @classmethod
    def is_stoppable(cls, status: str) -> bool:
        """Checks if a run with this status is stoppable."""
        return not cls.is_done(status)

    @classmethod
    def is_stopping(cls, status: str) -> bool:
        """Checks if a run with this status is stopping."""
        return status == V1Statuses.STOPPING

    @classmethod
    def is_done(cls, status: str, progressing: bool = False) -> bool:
        """Checks if a run with this status is done."""
        if progressing:
            return status in cls.DONE_OR_IN_PROGRESS_VALUES

        return status in cls.DONE_VALUES

    @classmethod
    def failed(cls, status: str) -> bool:
        """Checks if a run with this status is failed."""
        return status == V1Statuses.FAILED or status == V1Statuses.UPSTREAM_FAILED

    @classmethod
    def succeeded(cls, status: str) -> bool:
        """Checks if a run with this status is succeeded."""
        return status == V1Statuses.SUCCEEDED

    @classmethod
    def stopped(cls, status: str) -> bool:
        """Checks if a run with this status is stopped."""
        return status == V1Statuses.STOPPED

    @classmethod
    def skipped(cls, status: str) -> bool:
        """Checks if a run with this status is skipped."""
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
