import logging

from api.registry_access.serializers import RegistryAccessNameSerializer, RegistryAccessSerializer
from api.utils.views.catalog import CatalogDetailViewV1, CatalogListViewV1, CatalogNameListView
from api.utils.views.is_default_mixin import IsDefaultListMixinView
from db.models.registry_access import RegistryAccess
from options.registry.access import ACCESS_REGISTRY

_logger = logging.getLogger("polyaxon.views.k8s_config_maps")


class RegistryAccessListViewV1(IsDefaultListMixinView, CatalogListViewV1):
    """
    get:
        List entries of k8s config maps catalog.
    post:
        Create an entry in k8s config maps catalog.
    """
    default_option = ACCESS_REGISTRY
    queryset = RegistryAccess.objects.all()
    serializer_class = RegistryAccessSerializer


class RegistryAccessDetailViewV1(CatalogDetailViewV1):
    """
    get:
        Get an entry in k8s config maps catalog.
    patch:
        Update an entry in k8s config maps catalog.
    delete:
        Delete an entry in k8s config maps catalog.
    """
    queryset = RegistryAccess.objects.all()
    serializer_class = RegistryAccessSerializer


class RegistryAccessNameListView(CatalogNameListView):
    """
    get:
        List entry names of k8s config maps catalog.
    """
    queryset = RegistryAccess.objects.all()
    serializer_class = RegistryAccessNameSerializer
