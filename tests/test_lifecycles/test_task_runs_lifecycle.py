import pytest

from lifecycles.task_runs import TaskRunLifeCycle
from tests.base.case import BaseTest


@pytest.mark.lifecycles_mark
class TestTaskRunsStatuesTransition(BaseTest):
    NUM_STATUSES = 10

    def test_choices(self):
        assert len(TaskRunLifeCycle.CHOICES) == self.NUM_STATUSES

    def test_values(self):
        assert len(TaskRunLifeCycle.VALUES) == self.NUM_STATUSES

    def test_transition(self):
        assert len(TaskRunLifeCycle.TRANSITION_MATRIX) == self.NUM_STATUSES

    def test_operation_statuses_transition(self):  # pylint:disable=too-many-branches
        # Cannot transition to `CREATED`
        for status in TaskRunLifeCycle.VALUES:
            assert TaskRunLifeCycle.can_transition(
                status_from=status, status_to=TaskRunLifeCycle.CREATED) is False

        # {CREATED, RETRYING} -> SCHEDULED
        for status in TaskRunLifeCycle.VALUES:
            can_transition = TaskRunLifeCycle.can_transition(
                status_from=status, status_to=TaskRunLifeCycle.SCHEDULED)
            if status in {TaskRunLifeCycle.CREATED,
                          TaskRunLifeCycle.RETRYING,
                          TaskRunLifeCycle.WARNING}:
                assert can_transition is True
            else:
                assert can_transition is False

        # SCHEDULED -> RUNNING
        for status in TaskRunLifeCycle.VALUES:
            can_transition = TaskRunLifeCycle.can_transition(
                status_from=status, status_to=TaskRunLifeCycle.RUNNING)
            if status in {TaskRunLifeCycle.SCHEDULED, TaskRunLifeCycle.WARNING}:
                assert can_transition is True
            else:
                assert can_transition is False

        # RUNNING -> SUCCEEDED
        for status in TaskRunLifeCycle.VALUES:
            can_transition = TaskRunLifeCycle.can_transition(
                status_from=status, status_to=TaskRunLifeCycle.SUCCEEDED)
            if status in {TaskRunLifeCycle.RUNNING, TaskRunLifeCycle.WARNING}:
                assert can_transition is True
            else:
                assert can_transition is False

        # {SCHEDULED, RUNNING} -> FAILED
        for status in TaskRunLifeCycle.VALUES:
            can_transition = TaskRunLifeCycle.can_transition(
                status_from=status, status_to=TaskRunLifeCycle.FAILED)
            if status in {TaskRunLifeCycle.SCHEDULED,
                          TaskRunLifeCycle.RUNNING,
                          TaskRunLifeCycle.WARNING}:
                assert can_transition is True
            else:
                assert can_transition is False

        # ALL_VALUES -> UPSTREAM_FAILED
        for status in TaskRunLifeCycle.VALUES:
            can_transition = TaskRunLifeCycle.can_transition(
                status_from=status, status_to=TaskRunLifeCycle.UPSTREAM_FAILED)
            if status == TaskRunLifeCycle.UPSTREAM_FAILED:
                assert can_transition is False
            else:
                assert can_transition is True

        # {CREATED, SCHEDULED, RUNNING} -> STOPPED
        for status in TaskRunLifeCycle.VALUES:
            can_transition = TaskRunLifeCycle.can_transition(
                status_from=status, status_to=TaskRunLifeCycle.STOPPED)
            if status in {TaskRunLifeCycle.CREATED,
                          TaskRunLifeCycle.SCHEDULED,
                          TaskRunLifeCycle.RUNNING,
                          TaskRunLifeCycle.WARNING}:
                assert can_transition is True
            else:
                assert can_transition is False

        # {CREATED, SCHEDULED, STOPPED} -> SKIPPED
        for status in TaskRunLifeCycle.VALUES:
            can_transition = TaskRunLifeCycle.can_transition(
                status_from=status, status_to=TaskRunLifeCycle.SKIPPED)
            if status in {TaskRunLifeCycle.CREATED,
                          TaskRunLifeCycle.SCHEDULED,
                          TaskRunLifeCycle.STOPPED,
                          TaskRunLifeCycle.WARNING}:
                assert can_transition is True
            else:
                assert can_transition is False

        # {SCHEDULED, RUNNING, FAILED, STOPPED, SKIPPED, RETRYING} -> RETRYING
        for status in TaskRunLifeCycle.VALUES:
            can_transition = TaskRunLifeCycle.can_transition(
                status_from=status, status_to=TaskRunLifeCycle.RETRYING)
            if status in {TaskRunLifeCycle.SCHEDULED,
                          TaskRunLifeCycle.RUNNING,
                          TaskRunLifeCycle.FAILED,
                          TaskRunLifeCycle.STOPPED,
                          TaskRunLifeCycle.SKIPPED,
                          TaskRunLifeCycle.WARNING,
                          TaskRunLifeCycle.RETRYING}:
                assert can_transition is True
            else:
                assert can_transition is False
