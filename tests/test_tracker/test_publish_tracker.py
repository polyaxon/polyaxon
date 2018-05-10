from unittest.mock import patch

from clusters.models import Cluster
from event_manager.events.cluster import CLUSTER_CREATED
from event_manager.events.user import USER_ACTIVATED
from factories.factory_users import UserFactory
from tests.utils import BaseTest
from tracker.publish_tracker import PublishTrackerService


class PublishTrackerTest(BaseTest):
    def setUp(self):
        self.cluster = Cluster.load()
        self.admin = UserFactory(is_staff=True, is_superuser=True)
        self.user = UserFactory()
        self.publisher = PublishTrackerService()
        self.publisher.setup()
        super(PublishTrackerTest, self).setUp()

    def test_record_calls_identify_if_cluster_created(self):
        with patch('analytics.identify') as mock_identify:
            with patch('analytics.track') as mock_track:
                self.publisher.record(event_type=USER_ACTIVATED,
                                      instance=self.user,
                                      actor_id=self.admin.id)

        assert mock_identify.call_count == 0
        assert mock_track.call_count == 1

        with patch('analytics.identify') as mock_identify:
            with patch('analytics.track') as mock_track:
                self.publisher.record(event_type=CLUSTER_CREATED,
                                      instance=self.cluster,
                                      namespace='test',
                                      environment='test',
                                      is_upgrade='test',
                                      provisioner_enabled=False,
                                      use_data_claim=False,
                                      use_outputs_claim=False,
                                      use_logs_claim=False,
                                      use_repos_claim=False,
                                      use_upload_claim=False,
                                      cli_min_version='',
                                      cli_latest_version='',
                                      platform_min_version='',
                                      platform_latest_version='',
                                      chart_version='',
                                      cpu=0,
                                      memory=0,
                                      gpu=0)

        assert mock_identify.call_count == 1
        assert mock_track.call_count == 1
