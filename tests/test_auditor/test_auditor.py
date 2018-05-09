# pylint:disable=ungrouped-imports

from unittest.mock import patch

import activitylogs
import auditor
import tracker
from activitylogs import ActivityLogService

from clusters.models import Cluster
from event_manager.events.cluster import CLUSTER_CREATED
from event_manager.events.user import USER_ACTIVATED
from factories.factory_users import UserFactory
from tests.utils import BaseTest
from tracker.publisher import TrackerService


class AuditorTest(BaseTest):
    def setUp(self):
        self.cluster = Cluster.load()
        self.admin = UserFactory(is_staff=True, is_superuser=True)
        self.user = UserFactory()
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()
        activitylogs.validate()
        activitylogs.setup()

    def test_record_calls_only_subscribed_services(self):
        with patch.object(TrackerService, 'record_event') as mock_tracker_record:
            with patch.object(ActivityLogService, 'record_event') as mock_activitylog_record:
                auditor.record(event_type=USER_ACTIVATED,
                               instance=self.user,
                               actor_id=self.admin.id)

        assert mock_tracker_record.call_count == 1
        assert mock_activitylog_record.call_count == 1

        with patch.object(TrackerService, 'record_event') as mock_tracker_record:
            with patch.object(ActivityLogService, 'record_event') as mock_activitylog_record:
                auditor.record(event_type=CLUSTER_CREATED,
                               instance=self.cluster,
                               namespace='test',
                               environment='test',
                               is_upgrade='test',
                               use_provisioner=False,
                               use_data_claim=False,
                               use_outputs_claim=False,
                               use_logs_claim=False,
                               use_repos_claim=False,
                               use_upload_claim=False,
                               cli_version='',
                               cli_min_version='',
                               cli_latest_version='',
                               platform_min_version='',
                               platform_latest_version='',
                               chart_version='',
                               cpu=0,
                               memory=0,
                               gpu=0)

        assert mock_tracker_record.call_count == 1
        assert mock_activitylog_record.call_count == 0
