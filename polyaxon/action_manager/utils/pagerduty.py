from event_manager.event_context import get_event_context, get_readable_event
from libs.http import add_notification_referrer_param


def serialize_event_to_context(event):
    event_context = get_event_context(event)
    contexts = []  # Use build_field
    url = add_notification_referrer_param(event_context.object_context.url,
                                          provider='pagerduty',
                                          is_absolute=False)

    payload = {
        'event_type': event_context.subject_action,
        'description': get_readable_event(event_context),
        'details': event.data,
        'incident_key': 'trigger',
        'client': 'polyaxon',
        'client_url': url,
        'contexts': contexts,
    }

    return payload
