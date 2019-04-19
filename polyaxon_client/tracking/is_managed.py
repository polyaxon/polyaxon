from polyaxon_client import settings
from polyaxon_client.exceptions import PolyaxonClientException


def ensure_is_managed():
    if not settings.IS_MANAGED and not settings.IN_CLUSTER:
        raise PolyaxonClientException('This experiment/job is not managed by Polyaxon.')
