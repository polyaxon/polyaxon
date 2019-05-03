import analytics

from tracker.service import TrackerService


class PublishTrackerService(TrackerService):
    def __init__(self, key=''):
        self.analytics = analytics
        self.analytics.write_key = key


    @staticmethod
    def _record_event(event):
        if not event.ref_id:
            return

        if event.event_type == 'cluster.created':
            self.analytics.identify(
                event.ref_id.hex,
                event.serialize(dumps=False),
            )
        self.analytics.track(
            event.ref_id.hex,
            event.event_type,
            event.serialize(dumps=False, include_actor_name=False),
        )

    def record_event(self, event):
       try:
           self._record_event(event)
       except:
           pass
