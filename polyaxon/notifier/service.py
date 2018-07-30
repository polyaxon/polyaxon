from event_manager.event_service import EventService
from notifier.managers import default_action_manager, default_event_manager


class NotifierService(EventService):
    event_manager = default_event_manager
    action_manager = default_action_manager

    def record_event(self, event):
        for action in self.action_manager.values:
            action().execute(context=event, config=None, from_user=event.actor)

    def setup(self):
        super().setup()
        # Load default event types and actions
        import notifier.actions  # noqa
        import notifier.events  # noqa
