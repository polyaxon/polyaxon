import pytest

from lifecycles.experiments import ExperimentLifeCycle
from tests.base.case import BaseTest


@pytest.mark.lifecycles_mark
class TestExperimentsStatusesTransition(BaseTest):
    NUM_STATUSES = 13

    def test_choices(self):
        assert len(ExperimentLifeCycle.CHOICES) == self.NUM_STATUSES

    def test_values(self):
        assert len(ExperimentLifeCycle.VALUES) == self.NUM_STATUSES

    def test_transition(self):
        assert len(ExperimentLifeCycle.TRANSITION_MATRIX) == self.NUM_STATUSES

    def test_experiment_statuses_transition(self):
        # pylint:disable=too-many-branches
        # pylint:disable=too-many-statements
        # Cannot transition to `CREATED`
        for status in ExperimentLifeCycle.VALUES:
            assert ExperimentLifeCycle.can_transition(
                status_from=status, status_to=ExperimentLifeCycle.CREATED) is False

        # -> RESUMING
        for status in ExperimentLifeCycle.VALUES:
            can_transition = ExperimentLifeCycle.can_transition(
                status_from=status, status_to=ExperimentLifeCycle.RESUMING)
            if status in {ExperimentLifeCycle.CREATED,
                          ExperimentLifeCycle.WARNING,
                          ExperimentLifeCycle.SUCCEEDED,
                          ExperimentLifeCycle.SKIPPED,
                          ExperimentLifeCycle.STOPPED, }:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> BUILDING
        for status in ExperimentLifeCycle.VALUES:
            can_transition = ExperimentLifeCycle.can_transition(
                status_from=status, status_to=ExperimentLifeCycle.BUILDING)
            if status in {ExperimentLifeCycle.CREATED,
                          ExperimentLifeCycle.RESUMING,
                          ExperimentLifeCycle.WARNING,
                          ExperimentLifeCycle.UNKNOWN, }:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> SCHEDULED
        for status in ExperimentLifeCycle.VALUES:
            can_transition = ExperimentLifeCycle.can_transition(
                status_from=status, status_to=ExperimentLifeCycle.SCHEDULED)
            if status in {ExperimentLifeCycle.CREATED,
                          ExperimentLifeCycle.RESUMING,
                          ExperimentLifeCycle.BUILDING,
                          ExperimentLifeCycle.WARNING,
                          ExperimentLifeCycle.UNKNOWN, }:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> STARTING
        for status in ExperimentLifeCycle.VALUES:
            can_transition = ExperimentLifeCycle.can_transition(
                status_from=status, status_to=ExperimentLifeCycle.STARTING)
            if status in {ExperimentLifeCycle.CREATED,
                          ExperimentLifeCycle.RESUMING,
                          ExperimentLifeCycle.BUILDING,
                          ExperimentLifeCycle.SCHEDULED,
                          ExperimentLifeCycle.WARNING, }:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> RUNNING
        for status in ExperimentLifeCycle.VALUES:
            can_transition = ExperimentLifeCycle.can_transition(
                status_from=status, status_to=ExperimentLifeCycle.RUNNING)
            if status in {ExperimentLifeCycle.CREATED,
                          ExperimentLifeCycle.RESUMING,
                          ExperimentLifeCycle.BUILDING,
                          ExperimentLifeCycle.SCHEDULED,
                          ExperimentLifeCycle.STARTING,
                          ExperimentLifeCycle.UNKNOWN,
                          ExperimentLifeCycle.WARNING, }:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> SKIPPED
        for status in ExperimentLifeCycle.VALUES:
            can_transition = ExperimentLifeCycle.can_transition(
                status_from=status, status_to=ExperimentLifeCycle.SKIPPED)
            if status not in ExperimentLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> SUCCEEDED
        for status in ExperimentLifeCycle.VALUES:
            can_transition = ExperimentLifeCycle.can_transition(
                status_from=status, status_to=ExperimentLifeCycle.SUCCEEDED)
            if status not in ExperimentLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> FAILED
        for status in ExperimentLifeCycle.VALUES:
            can_transition = ExperimentLifeCycle.can_transition(
                status_from=status, status_to=ExperimentLifeCycle.FAILED)
            if status not in ExperimentLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> UPSTREAM_FAILED
        for status in ExperimentLifeCycle.VALUES:
            can_transition = ExperimentLifeCycle.can_transition(
                status_from=status, status_to=ExperimentLifeCycle.UPSTREAM_FAILED)
            if status not in ExperimentLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> STOPPED
        for status in ExperimentLifeCycle.VALUES:
            can_transition = ExperimentLifeCycle.can_transition(
                status_from=status, status_to=ExperimentLifeCycle.STOPPED)
            if status in ExperimentLifeCycle.VALUES - {ExperimentLifeCycle.STOPPED,
                                                       ExperimentLifeCycle.SKIPPED, }:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> WARNING
        for status in ExperimentLifeCycle.VALUES:
            can_transition = ExperimentLifeCycle.can_transition(
                status_from=status, status_to=ExperimentLifeCycle.WARNING)
            cond = status in (ExperimentLifeCycle.VALUES -
                              ExperimentLifeCycle.DONE_STATUS -
                              {ExperimentLifeCycle.WARNING, })
            if cond:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> UNKNOWN
        for status in ExperimentLifeCycle.VALUES:
            can_transition = ExperimentLifeCycle.can_transition(
                status_from=status, status_to=ExperimentLifeCycle.UNKNOWN)
            cond = status in (ExperimentLifeCycle.VALUES -
                              ExperimentLifeCycle.DONE_STATUS -
                              {ExperimentLifeCycle.UNKNOWN, })
            if cond:
                assert can_transition is True
            else:
                assert can_transition is False
