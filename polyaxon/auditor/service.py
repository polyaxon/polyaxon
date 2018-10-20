from django.core.exceptions import ObjectDoesNotExist

from auditor.manager import default_manager
from event_manager.event_service import EventService


class AuditorService(EventService):
    """An service that just passes the event to author services."""
    __all__ = EventService.__all__ + ('log', 'notify', 'track')

    event_manager = default_manager

    def __init__(self):
        self.notifier = None
        self.tracker = None
        self.activitylogs = None

    def get_event(self, event_type, instance, **kwargs):
        return {
            'event_type': event_type,
            'instance': instance,
            'kwargs': kwargs
        }

    def record_event(self, event):
        """
        Record the event async.

        N.B. it's intentional that we pass an orm object/instance
        to be sure that we can log later on.
        """
        from polyaxon.celery_api import celery_app
        from polyaxon.settings import EventsCeleryTasks

        celery_app.send_task(EventsCeleryTasks.EVENTS_TRACK,
                             kwargs={'event': event},
                             serializer='pickle')
        celery_app.send_task(EventsCeleryTasks.EVENTS_LOG,
                             kwargs={'event': event},
                             serializer='pickle')
        celery_app.send_task(EventsCeleryTasks.EVENTS_NOTIFY,
                             kwargs={'event': event},
                             serializer='pickle')

    def notify(self, event, refresh_instance=False):
        if refresh_instance and event['instance']:
            try:
                event['instance'].refresh_from_db()
            except ObjectDoesNotExist:
                return
        self.notifier.record(event_type=event['event_type'],
                             instance=event['instance'],
                             **event['kwargs'])

    def track(self, event):
        self.tracker.record(event_type=event['event_type'],
                            instance=event['instance'],
                            **event['kwargs'])

    def log(self, event):
        self.activitylogs.record(event_type=event['event_type'],
                                 instance=event['instance'],
                                 **event['kwargs'])

    def setup(self):
        super().setup()
        # Load default event types
        import auditor.events  # noqa

        import notifier
        import activitylogs
        import tracker

        self.notifier = notifier
        self.tracker = tracker
        self.activitylogs = activitylogs
