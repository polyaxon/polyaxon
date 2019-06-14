import logging

from api.data_stores.serializers import DataStoreSerializer, DataStoreNameSerializer
from api.utils.views.catalog import CatalogDetailViewV1, CatalogListViewV1, CatalogNameListView
from db.models.data_stores import DataStore

_logger = logging.getLogger("polyaxon.views.k8s_config_maps")


class DataStoreListViewV1(CatalogListViewV1):
    """
    get:
        List entries of k8s config maps catalog.
    post:
        Create an entry in k8s config maps catalog.
    """
    queryset = DataStore.objects.all()
    serializer_class = DataStoreSerializer


class DataStoreDetailViewV1(CatalogDetailViewV1):
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


class DataStoreNameListView(CatalogNameListView):
    """
    get:
        List entry names of k8s config maps catalog.
    """
    queryset = DataStore.objects.all()
    serializer_class = DataStoreNameSerializer
