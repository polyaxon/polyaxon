from events.event_colors import EventColor
from events.event_context import get_event_context, get_readable_event
from libs.http import add_notification_referrer_param


def serialize_event_to_context(event):
    event_context = get_event_context(event)
    url = add_notification_referrer_param(event_context.object_context.url,
                                          provider='polyaxon',
                                          is_absolute=False)

    payload = {
        'pretext': event_context.subject_action,
        'title': event_context.subject_action,
        'text': get_readable_event(event_context),
        'color': EventColor.get_for_event(event_content_object=event.instance,
                                          event_type=event.event_type),
        'fields': [],
        'author_name': 'Polyaxon',
        'author_link': url,
        'author_icon': None,
    }

    return payload
