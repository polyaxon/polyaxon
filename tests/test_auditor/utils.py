import pytest

from tests.base.case import BaseTest


@pytest.mark.auditor_mark
class AuditorBaseTest(BaseTest):
    DISABLE_AUDITOR = False
    DISABLE_EXECUTOR = False
    EVENTS = None

    def test_num_events(self):
        assert len(self.EVENTS) == len(self.tested_events)
