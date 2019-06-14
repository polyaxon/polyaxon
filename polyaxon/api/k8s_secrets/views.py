import logging

from api.k8s_secrets.serializers import K8SSecretSerializer
from api.utils.views.catalog import CatalogListViewV1, CatalogDetailViewV1
from db.models.secrets import K8SSecret

_logger = logging.getLogger("polyaxon.views.k8s_secrets")


class ClusterK8SSecretListViewV1(CatalogListViewV1):
    """
    get:
        List entries of k8s secrets catalog.
    post:
        Create an entry in k8s secrets catalog.
    """
    queryset = K8SSecret.objects.all()
    serializer_class = K8SSecretSerializer


class ClusterK8SSecretDetailViewV1(CatalogDetailViewV1):
    """
    get:
        Get an entry in k8s secrets catalog.
    patch:
        Update an entry in k8s secrets catalog.
    delete:
        Delete an entry in k8s secrets catalog.
    """
    queryset = K8SSecret.objects.all()
    serializer_class = K8SSecretSerializer
