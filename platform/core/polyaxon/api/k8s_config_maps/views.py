import logging

from api.k8s_config_maps.serializers import K8SConfigMapNameSerializer, K8SConfigMapSerializer
from api.utils.views.catalog import CatalogDetailViewV1, CatalogListViewV1, CatalogNameListView
from db.models.config_maps import K8SConfigMap

_logger = logging.getLogger("polyaxon.views.k8s_config_maps")


class ClusterK8SConfigMapListViewV1(CatalogListViewV1):
    """
    get:
        List entries of k8s config maps catalog.
    post:
        Create an entry in k8s config maps catalog.
    """
    queryset = K8SConfigMap.objects.all()
    serializer_class = K8SConfigMapSerializer


class ClusterK8SConfigMapDetailViewV1(CatalogDetailViewV1):
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


class ClusterK8SConfigMapNameListView(CatalogNameListView):
    """
    get:
        List entry names of k8s config maps catalog.
    """
    queryset = K8SConfigMap.objects.all()
    serializer_class = K8SConfigMapNameSerializer
