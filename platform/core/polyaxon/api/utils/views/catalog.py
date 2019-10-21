from api.endpoint.admin import AdminOrReadOnlyEndpoint, AdminOrReadOnlyListEndpoint
from api.endpoint.base import (
    CreateEndpoint,
    DestroyEndpoint,
    ListEndpoint,
    RetrieveEndpoint,
    UpdateEndpoint
)
from api.paginator import LargeLimitOffsetPagination
from db.models.clusters import Cluster


class CatalogListViewV1(AdminOrReadOnlyListEndpoint, ListEndpoint, CreateEndpoint):
    queryset = None
    serializer_class = None

    def get_owner(self):
        cluster = Cluster.load()
        return cluster.get_or_create_owner(cluster)

    def perform_create(self, serializer):
        serializer.save(owner=self.get_owner())


class CatalogDetailViewV1(AdminOrReadOnlyEndpoint,
                          RetrieveEndpoint,
                          UpdateEndpoint,
                          DestroyEndpoint):
    queryset = None
    serializer_class = None


class CatalogNameListView(AdminOrReadOnlyListEndpoint, ListEndpoint):
    """List projects' names for a user."""
    queryset = None
    serializer_class = None
    pagination_class = LargeLimitOffsetPagination
