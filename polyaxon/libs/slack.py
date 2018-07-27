from __future__ import absolute_import

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from event_manager import event_context
from event_manager.event_colors import EventColor
from libs.date_utils import to_timestamp


def add_notification_referrer_param(url, provider):
    parsed_url = urlparse(url)
    query = parse_qs(parsed_url.query)
    query['referrer'] = provider
    url_list = list(parsed_url)
    url_list[4] = urlencode(query, doseq=True)
    return urlunparse(url_list)


def build_attachment_title(event):
    return '{} {}'.format(event.get_event_subject(), event.get_event_action())


def build_attachment_text(event):
    return


def get_footer():
    return {
        'footer': 'Polyaxon',
        'footer_icon': '',  # TODO: add png image
    }


def build_field(title, value, short=True):
    return {
        'title': title,
        'value': value,
        'short': short,
    }


def build_attachment(event):
    logo_url = ''  # TODO: add logo url

    text = build_attachment_text(event) or ''

    fields = []  # Use build_field

    event_object_context = event_context.get_event_object_context(
        event_content_object=event.instance,
        event_type=event.event_type
    )

    ts = event.created_at

    if event:
        event_ts = event.datetime
        ts = max(ts, event_ts)

    payload = {
        'fallback': u'[{}] {}',
        'title': build_attachment_title(event),
        'title_link': add_notification_referrer_param(event_object_context.url, 'slack'),
        'text': text,
        'fields': fields,
        'mrkdwn_in': ['text'],
        'footer_icon': logo_url,
        'footer': get_footer(),
        'color': EventColor.get_for_event(event_content_object=event.instance,
                                          event_type=event.event_type),
    }

    if ts:
        payload['ts'] = to_timestamp(ts)
