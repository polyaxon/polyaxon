from event_manager.event_colors import EventColor
from event_manager.event_context import get_event_context, get_readable_event
from libs.date_utils import to_timestamp
from libs.http import add_notification_referrer_param


def get_field(title, value, short=True):
    return {
        'title': title,
        'value': value,
        'short': short,
    }


def serialize_event_to_context(event):
    event_context = get_event_context(event)
    logo_url = ''  # TODO: add logo url
    fields = []  # Use build_field
    url = add_notification_referrer_param(event_context.object_context.url,
                                          provider='slack',
                                          is_absolute=False)

    payload = {
        'fallback': event_context.subject_action,
        'title': event_context.subject_action,
        'title_link': url,
        'text': get_readable_event(event_context),
        'fields': fields,
        'mrkdwn_in': ['text'],
        'footer_icon': logo_url,
        'footer': 'Polyaxon',
        'color': EventColor.get_for_event(event_content_object=event.instance,
                                          event_type=event.event_type),
        'ts': to_timestamp(event.datetime)
    }

    return payload
