from event_manager.event import Attribute, Event


class ActionExecutedEvent(Event):
    attributes = (
        Attribute('automatic'),
        Attribute('user.id', is_required=False),
    )
