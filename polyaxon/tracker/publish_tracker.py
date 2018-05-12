import analytics

from django.db import InterfaceError, OperationalError, ProgrammingError

from tracker.service import TrackerService


class PublishTrackerService(TrackerService):
    def __init__(self, key=''):
        self.cluster_id = None
        self.analytics = analytics
        self.analytics.write_key = key

    def get_cluster_id(self):
        if self.cluster_id:
            return self.cluster_id

        from clusters.models import Cluster
        try:
            cluster_uuid = Cluster.load().uuid.hex
            self.cluster_id = cluster_uuid
        except (Cluster.DoesNotExist, InterfaceError, ProgrammingError, OperationalError):
            pass
        return self.cluster_id

    def record_event(self, event):
        if not self.cluster_id:
            return

        if event.event_type == 'cluster.created':
            self.analytics.identify(
                self.get_cluster_id(),
                data=event.serialize(dumps=False),
            )
        self.analytics.track(
            self.get_cluster_id(),
            event.event_type,
            event.serialize(dumps=False),
        )

    def setup(self):
        super(PublishTrackerService, self).setup()
        self.cluster_id = self.get_cluster_id()
