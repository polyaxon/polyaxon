import pytest

from lifecycles.jobs import JobLifeCycle
from tests.base.case import BaseTest


@pytest.mark.lifecycles_mark
class TestJobsStatusesTransition(BaseTest):
    NUM_STATUSES = 13

    def test_choices(self):
        assert len(JobLifeCycle.CHOICES) == self.NUM_STATUSES

    def test_values(self):
        assert len(JobLifeCycle.VALUES) == self.NUM_STATUSES

    def test_transition(self):
        assert len(JobLifeCycle.TRANSITION_MATRIX) == self.NUM_STATUSES

    def test_job_statuses_transition(self):
        # pylint:disable=too-many-branches
        # pylint:disable=too-many-statements
        # Cannot transition to `CREATED`
        for status in JobLifeCycle.VALUES:
            assert JobLifeCycle.can_transition(
                status_from=status, status_to=JobLifeCycle.CREATED) is False

        # -> BUILDING
        for status in JobLifeCycle.VALUES:
            can_transition = JobLifeCycle.can_transition(
                status_from=status, status_to=JobLifeCycle.BUILDING)
            if status in {JobLifeCycle.CREATED,
                          JobLifeCycle.RESUMING,
                          JobLifeCycle.UNSCHEDULABLE,
                          JobLifeCycle.WARNING,
                          JobLifeCycle.UNKNOWN, }:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> SCHEDULED
        for status in JobLifeCycle.VALUES:
            can_transition = JobLifeCycle.can_transition(
                status_from=status, status_to=JobLifeCycle.SCHEDULED)
            if status in {JobLifeCycle.CREATED,
                          JobLifeCycle.RESUMING,
                          JobLifeCycle.BUILDING,
                          JobLifeCycle.WARNING,
                          JobLifeCycle.UNSCHEDULABLE,
                          JobLifeCycle.UNKNOWN, }:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> RUNNING
        for status in JobLifeCycle.VALUES:
            can_transition = JobLifeCycle.can_transition(
                status_from=status, status_to=JobLifeCycle.RUNNING)
            if status in {JobLifeCycle.CREATED,
                          JobLifeCycle.SCHEDULED,
                          JobLifeCycle.RESUMING,
                          JobLifeCycle.BUILDING,
                          JobLifeCycle.UNSCHEDULABLE,
                          JobLifeCycle.UNKNOWN,
                          JobLifeCycle.WARNING, }:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> SKIPPED
        for status in JobLifeCycle.VALUES:
            can_transition = JobLifeCycle.can_transition(
                status_from=status, status_to=JobLifeCycle.SKIPPED)
            if status not in JobLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> SUCCEEDED
        for status in JobLifeCycle.VALUES:
            can_transition = JobLifeCycle.can_transition(
                status_from=status, status_to=JobLifeCycle.SUCCEEDED)
            if status not in JobLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> FAILED
        for status in JobLifeCycle.VALUES:
            can_transition = JobLifeCycle.can_transition(
                status_from=status, status_to=JobLifeCycle.FAILED)
            if status not in JobLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> UPSTREAM_FAILED
        for status in JobLifeCycle.VALUES:
            can_transition = JobLifeCycle.can_transition(
                status_from=status, status_to=JobLifeCycle.UPSTREAM_FAILED)
            if status not in JobLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> STOPPED
        for status in JobLifeCycle.VALUES:
            can_transition = JobLifeCycle.can_transition(
                status_from=status, status_to=JobLifeCycle.STOPPED)
            if status not in JobLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> WARNING
        for status in JobLifeCycle.VALUES:
            can_transition = JobLifeCycle.can_transition(
                status_from=status, status_to=JobLifeCycle.WARNING)
            cond = status in (JobLifeCycle.VALUES -
                              JobLifeCycle.DONE_STATUS -
                              {JobLifeCycle.WARNING, })
            if cond:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> UNKNOWN
        for status in JobLifeCycle.VALUES:
            can_transition = JobLifeCycle.can_transition(
                status_from=status, status_to=JobLifeCycle.UNKNOWN)
            if status not in {JobLifeCycle.UNKNOWN, }:
                assert can_transition is True
            else:
                assert can_transition is False
