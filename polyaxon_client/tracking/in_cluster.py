from polyaxon_client import settings
from polyaxon_client.exceptions import PolyaxonClientException


def ensure_in_custer():
    if not settings.IN_CLUSTER:
        raise PolyaxonClientException('This experiment/job is not running inside a Polyaxon job.')
