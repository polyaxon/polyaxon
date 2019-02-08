from typing import Any, Optional
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse

import conf


def absolute_uri(url: str) -> Optional[str]:
    if not url:
        return None

    api_host = conf.get('API_HOST')
    if not api_host:
        return url

    url = urljoin(api_host.rstrip('/') + '/', url.lstrip('/'))
    return '{}://{}'.format(conf.get('PROTOCOL'), url)


def add_notification_referrer_param(url: str,
                                    provider: str,
                                    is_absolute: bool = True) -> Optional[Any]:
    if not is_absolute:
        url = absolute_uri(url)
    if not url:
        return None
    parsed_url = urlparse(url)
    query = parse_qs(parsed_url.query)
    query['referrer'] = provider
    url_list = list(parsed_url)
    url_list[4] = urlencode(query, doseq=True)
    return urlunparse(url_list)
