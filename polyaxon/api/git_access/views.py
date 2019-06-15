import logging

from api.git_access.serializers import GitAccessNameSerializer, GitAccessSerializer
from api.utils.views.catalog import CatalogDetailViewV1, CatalogListViewV1, CatalogNameListView
from db.models.git_access import GitAccess

_logger = logging.getLogger("polyaxon.views.k8s_config_maps")


class GitAccessListViewV1(CatalogListViewV1):
    """
    get:
        List entries of k8s config maps catalog.
    post:
        Create an entry in k8s config maps catalog.
    """
    queryset = GitAccess.objects.all()
    serializer_class = GitAccessSerializer


class GitAccessDetailViewV1(CatalogDetailViewV1):
    """
    get:
        Get an entry in k8s config maps catalog.
    patch:
        Update an entry in k8s config maps catalog.
    delete:
        Delete an entry in k8s config maps catalog.
    """
    queryset = GitAccess.objects.all()
    serializer_class = GitAccessSerializer


class GitAccessNameListView(CatalogNameListView):
    """
    get:
        List entry names of k8s config maps catalog.
    """
    queryset = GitAccess.objects.all()
    serializer_class = GitAccessNameSerializer
