import tracker

from tracker import AnalyticService


class PublisherAnalyticsService(AnalyticService):
    def __init__(self):
        self.cluster_id = None
        self.publisher = None

    def get_cluster_id(self):
        if self.cluster_id:
            return self.cluster_id

        from clusters.models import Cluster
        cluster_uuid = Cluster.load().uuid.hex
        self.cluster_id = cluster_uuid
        return self.cluster_id

    def record_event(self, event):
        self.publisher.publish(
            self.cluster_id,  # Add to data
            data=event.serialize(dumps=True),
        )
