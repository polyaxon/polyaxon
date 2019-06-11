import logging

from api.data_stores.serializers import DataStoreSerializer
from api.endpoint.admin import AdminOrReadOnlyEndpoint, AdminOrReadOnlyListEndpoint
from api.endpoint.base import (
    CreateEndpoint,
    DestroyEndpoint,
    ListEndpoint,
    RetrieveEndpoint,
    UpdateEndpoint
)
from db.models.data_stores import DataStore

_logger = logging.getLogger("polyaxon.views.k8s_config_maps")


class DataStoreListViewV1(AdminOrReadOnlyListEndpoint, ListEndpoint, CreateEndpoint):
    """
    get:
        List entries of k8s config maps catalog.
    post:
        Create an entry in k8s config maps catalog.
    """
    queryset = DataStore.objects.all()
    serializer_class = DataStoreSerializer


class DataStoreDetailViewV1(AdminOrReadOnlyEndpoint,
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
    queryset = DataStore.objects.all()
    serializer_class = DataStoreSerializer
