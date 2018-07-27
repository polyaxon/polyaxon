from __future__ import absolute_import

from django.conf import settings


def get_asset_url(module, path):
    """Return a static asset URL (located within Polyaxon's static files).

    Example:
        ```python
        >>> get_asset_url('polyaxon', 'dist/global.css')
        ... "/_static/74d127b78dc7daf2c51f/polyaxon/dist/global.css"
        ```
    """
    return '{}/{}/{}'.format(
        settings.STATIC_URL.rstrip('/'),
        module,
        path.lstrip('/'),
    )
