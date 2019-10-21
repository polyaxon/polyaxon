from django.conf import settings


def get_asset_url(module: str, path: str) -> str:
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
