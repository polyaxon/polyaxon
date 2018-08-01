from event_manager.event_colors import EventColor
from event_manager.event_context import get_event_context, get_readable_event


def serialize_event_to_context(event):
    event_context = get_event_context(event)

    payload = {
        'message': get_readable_event(event_context),
        'message_format': 'text',
        'color': EventColor.get_for_event(event_content_object=event.instance,
                                          event_type=event.event_type),
        'from': 'Polyaxon',
    }

    return payload
