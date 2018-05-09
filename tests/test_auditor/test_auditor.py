from __future__ import absolute_import

from unittest.mock import patch

import auditor
import tracker

from clusters.models import Cluster
from event_manager.events.cluster import CLUSTER_CREATED
from tests.utils import BaseTest
from tracker.publisher import TrackerService


class AuditorTest(BaseTest):
    def setUp(self):
        self.cluster = Cluster.load()
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()

    def test_record_calls_other_services(self):
        with patch.object(TrackerService, 'record_event') as mock_record:
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

        assert mock_record.call_count == 1
