from polyaxon import settings
from polyaxon.exceptions import PolyaxonClientException


def ensure_is_managed():
    if not settings.CLIENT_CONFIG.is_managed and not settings.CLIENT_CONFIG.in_cluster:
        raise PolyaxonClientException("This experiment/job is not managed by Polyaxon.")
