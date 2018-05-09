import analytics

from tracker import TrackerService


class PublisherService(TrackerService):
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
        if event.event_type == 'cluster.created':
            self.publisher.identify(
                self.cluster_id,  # Add to data
                data=event.serialize(dumps=True),
            )
        self.publisher.track(
            self.cluster_id,  # Add to data
            data=event.serialize(dumps=True),
        )

    def setup(self):
        super(self, PublisherService).setup()
        self.cluster_id = self.get_cluster_id()
