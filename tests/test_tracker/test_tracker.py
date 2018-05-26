import pytest
from django.conf import settings
from django.test import override_settings

import tracker

from tests.utils import BaseTest


@pytest.mark.auditor
class TrackerTest(BaseTest):
    def test_default_backend_tracker(self):
        backend = tracker.get_tracker_backend()
        assert backend == 'tracker.service.TrackerService'

    @override_settings(TRACKER_BACKEND=settings.TRACKER_BACKEND_PUBLISHER)
    def test_publisher_backend_tracker(self):
        backend = tracker.get_tracker_backend()
        assert backend == 'tracker.publish_tracker.PublishTrackerService'
