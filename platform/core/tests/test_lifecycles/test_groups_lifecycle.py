import pytest

from lifecycles.experiment_groups import ExperimentGroupLifeCycle
from tests.base.case import BaseTest


@pytest.mark.lifecycles_mark
class TestGroupsStatusesTransition(BaseTest):
    NUM_STATUSES = 11

    def test_choices(self):
        assert len(ExperimentGroupLifeCycle.CHOICES) == self.NUM_STATUSES

    def test_values(self):
        assert len(ExperimentGroupLifeCycle.VALUES) == self.NUM_STATUSES

    def test_transition(self):
        assert len(ExperimentGroupLifeCycle.TRANSITION_MATRIX) == self.NUM_STATUSES

    def test_group_statuses_transition(self):  # pylint:disable=too-many-branches
        # Cannot transition to `CREATED`
        for status in ExperimentGroupLifeCycle.VALUES:
            assert ExperimentGroupLifeCycle.can_transition(
                status_from=status, status_to=ExperimentGroupLifeCycle.CREATED) is False

        # -> RESUMING
        for status in ExperimentGroupLifeCycle.VALUES:
            can_transition = ExperimentGroupLifeCycle.can_transition(
                status_from=status, status_to=ExperimentGroupLifeCycle.RESUMING)
            if status in {ExperimentGroupLifeCycle.CREATED,
                          ExperimentGroupLifeCycle.WARNING,
                          ExperimentGroupLifeCycle.SKIPPED,
                          ExperimentGroupLifeCycle.STOPPED}:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> RUNNING
        for status in ExperimentGroupLifeCycle.VALUES:
            can_transition = ExperimentGroupLifeCycle.can_transition(
                status_from=status, status_to=ExperimentGroupLifeCycle.RUNNING)
            if status in {ExperimentGroupLifeCycle.CREATED,
                          ExperimentGroupLifeCycle.WARNING,
                          ExperimentGroupLifeCycle.RESUMING}:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> DONE
        for status in ExperimentGroupLifeCycle.VALUES:
            can_transition = ExperimentGroupLifeCycle.can_transition(
                status_from=status, status_to=ExperimentGroupLifeCycle.DONE)
            if status not in ExperimentGroupLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> SKIPPED
        for status in ExperimentGroupLifeCycle.VALUES:
            can_transition = ExperimentGroupLifeCycle.can_transition(
                status_from=status, status_to=ExperimentGroupLifeCycle.SKIPPED)
            if status not in ExperimentGroupLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> FAILED
        for status in ExperimentGroupLifeCycle.VALUES:
            can_transition = ExperimentGroupLifeCycle.can_transition(
                status_from=status, status_to=ExperimentGroupLifeCycle.FAILED)
            if status not in ExperimentGroupLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> UPSTREAM_FAILED
        for status in ExperimentGroupLifeCycle.VALUES:
            can_transition = ExperimentGroupLifeCycle.can_transition(
                status_from=status, status_to=ExperimentGroupLifeCycle.UPSTREAM_FAILED)
            if status not in ExperimentGroupLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> STOPPING
        for status in ExperimentGroupLifeCycle.VALUES:
            can_transition = ExperimentGroupLifeCycle.can_transition(
                status_from=status, status_to=ExperimentGroupLifeCycle.STOPPING)
            cond = (status not in (ExperimentGroupLifeCycle.DONE_STATUS |
                                   {ExperimentGroupLifeCycle.STOPPING, }))
            if cond:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> STOPPED
        for status in ExperimentGroupLifeCycle.VALUES:
            can_transition = ExperimentGroupLifeCycle.can_transition(
                status_from=status, status_to=ExperimentGroupLifeCycle.STOPPED)
            if status not in ExperimentGroupLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> WARNING
        for status in ExperimentGroupLifeCycle.VALUES:
            can_transition = ExperimentGroupLifeCycle.can_transition(
                status_from=status, status_to=ExperimentGroupLifeCycle.WARNING)
            cond = status in (ExperimentGroupLifeCycle.VALUES -
                              ExperimentGroupLifeCycle.DONE_STATUS -
                              {ExperimentGroupLifeCycle.WARNING, })
            if cond:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> UNKNOWN
        for status in ExperimentGroupLifeCycle.VALUES:
            can_transition = ExperimentGroupLifeCycle.can_transition(
                status_from=status, status_to=ExperimentGroupLifeCycle.UNKNOWN)
            if status not in {ExperimentGroupLifeCycle.UNKNOWN, }:
                assert can_transition is True
            else:
                assert can_transition is False
