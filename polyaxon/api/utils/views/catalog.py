from api.endpoint.admin import AdminOrReadOnlyEndpoint, AdminOrReadOnlyListEndpoint
from api.endpoint.base import (
    CreateEndpoint,
    DestroyEndpoint,
    ListEndpoint,
    RetrieveEndpoint,
    UpdateEndpoint
)
from db.models.clusters import Cluster
from db.models.owner import Owner


class CatalogListViewV1(AdminOrReadOnlyListEndpoint, ListEndpoint, CreateEndpoint):
    queryset = None
    serializer_class = None

    def get_owner(self):
        return Owner.objects.get(name=Cluster.load().uuid)

    def perform_create(self, serializer):
        serializer.save(owner=self.get_owner())


class CatalogDetailViewV1(AdminOrReadOnlyEndpoint,
                          RetrieveEndpoint,
                          UpdateEndpoint,
                          DestroyEndpoint):
    queryset = None
    serializer_class = None
