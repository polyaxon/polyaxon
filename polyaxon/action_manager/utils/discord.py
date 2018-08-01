from event_manager.event_context import get_event_context, get_readable_event


def serialize_event_to_context(event):
    event_context = get_event_context(event)
    logo_url = ''

    payload = {
        'content': get_readable_event(event_context),
        'avatar_url': logo_url
    }

    return payload
