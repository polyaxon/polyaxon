import analytics

from tracker.service import TrackerService


class PublishTrackerService(TrackerService):
    def __init__(self, key=''):
        self.analytics = analytics
        self.analytics.write_key = key

    def record_event(self, event):
        if not event.ref_id:
            return

        if event.event_type == 'cluster.created':
            self.analytics.identify(
                event.ref_id,
                event.serialize(dumps=False),
            )
        self.analytics.track(
            event.ref_id,
            event.event_type,
            event.serialize(dumps=False, include_actor_name=False),
        )

    def setup(self):
        super().setup()
