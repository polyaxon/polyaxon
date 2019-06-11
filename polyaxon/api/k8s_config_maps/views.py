import logging

from api.endpoint.admin import AdminOrReadOnlyEndpoint, AdminOrReadOnlyListEndpoint
from api.endpoint.base import (
    CreateEndpoint,
    DestroyEndpoint,
    ListEndpoint,
    RetrieveEndpoint,
    UpdateEndpoint
)
from api.k8s_config_maps.serializers import K8SConfigMapSerializer
from db.models.config_maps import K8SConfigMap

_logger = logging.getLogger("polyaxon.views.k8s_config_maps")


class ClusterK8SConfigMapListViewV1(AdminOrReadOnlyListEndpoint, ListEndpoint, CreateEndpoint):
    """
    get:
        List entries of k8s config maps catalog.
    post:
        Create an entry in k8s config maps catalog.
    """
    queryset = K8SConfigMap.objects.all()
    serializer_class = K8SConfigMapSerializer


class ClusterK8SConfigMapDetailViewV1(AdminOrReadOnlyEndpoint,
                                      RetrieveEndpoint,
                                      UpdateEndpoint,
                                      DestroyEndpoint):
    """
    get:
        Get an entry in k8s config maps catalog.
    patch:
        Update an entry in k8s config maps catalog.
    delete:
        Delete an entry in k8s config maps catalog.
    """
    queryset = K8SConfigMap.objects.all()
    serializer_class = K8SConfigMapSerializer
