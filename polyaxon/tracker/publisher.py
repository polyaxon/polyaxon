import analytics

from tracker import AnalyticService


class PublisherAnalyticsService(AnalyticService):
    def __init__(self):
        self.cluster_id = None
        self.publisher = analytics
        # Set key
        analytics.write_key = ''

    def get_cluster_id(self):
        if self.cluster_id:
            return self.cluster_id

        from clusters.models import Cluster
        cluster_uuid = Cluster.load().uuid.hex
        self.cluster_id = cluster_uuid
        return self.cluster_id

    def record_event(self, event):
        self.publisher.track(
            self.cluster_id,  # Add to data
            data=event.serialize(dumps=True),
        )
