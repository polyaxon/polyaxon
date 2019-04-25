import pytest

from lifecycles.pipelines import PipelineLifeCycle
from tests.base.case import BaseTest


@pytest.mark.lifecycles_mark
class TestPipelinesStatusesTransition(BaseTest):
    NUM_STATUSES = 12

    def test_choices(self):
        assert len(PipelineLifeCycle.CHOICES) == self.NUM_STATUSES

    def test_values(self):
        assert len(PipelineLifeCycle.VALUES) == self.NUM_STATUSES

    def test_transition(self):
        assert len(PipelineLifeCycle.TRANSITION_MATRIX) == self.NUM_STATUSES

    def test_pipeline_statuses_transition(self):  # pylint:disable=too-many-branches
        # Cannot transition to `CREATED`
        for status in PipelineLifeCycle.VALUES:
            assert PipelineLifeCycle.can_transition(
                status_from=status, status_to=PipelineLifeCycle.CREATED) is False

        # -> SCHEDULED
        for status in PipelineLifeCycle.VALUES:
            can_transition = PipelineLifeCycle.can_transition(
                status_from=status, status_to=PipelineLifeCycle.SCHEDULED)
            if status in {PipelineLifeCycle.CREATED, PipelineLifeCycle.WARNING}:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> RUNNING
        for status in PipelineLifeCycle.VALUES:
            can_transition = PipelineLifeCycle.can_transition(
                status_from=status, status_to=PipelineLifeCycle.RUNNING)
            if status in {PipelineLifeCycle.CREATED,
                          PipelineLifeCycle.SCHEDULED,
                          PipelineLifeCycle.WARNING}:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> DONE
        for status in PipelineLifeCycle.VALUES:
            can_transition = PipelineLifeCycle.can_transition(
                status_from=status, status_to=PipelineLifeCycle.DONE)
            if status not in PipelineLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> STOPPED
        for status in PipelineLifeCycle.VALUES:
            can_transition = PipelineLifeCycle.can_transition(
                status_from=status, status_to=PipelineLifeCycle.STOPPED)
            if status not in PipelineLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> SUCCEEDED
        for status in PipelineLifeCycle.VALUES:
            can_transition = PipelineLifeCycle.can_transition(
                status_from=status, status_to=PipelineLifeCycle.SUCCEEDED)
            if status not in PipelineLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False

        # -> SKIPPED
        for status in PipelineLifeCycle.VALUES:
            can_transition = PipelineLifeCycle.can_transition(
                status_from=status, status_to=PipelineLifeCycle.SKIPPED)
            if status not in PipelineLifeCycle.DONE_STATUS:
                assert can_transition is True
            else:
                assert can_transition is False
