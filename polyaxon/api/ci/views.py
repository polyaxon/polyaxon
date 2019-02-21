import logging

from rest_framework.generics import get_object_or_404

from api.ci.serializers import CISerializer

from api.endpoint.base import (
    DestroyEndpoint,
    RetrieveEndpoint,
    UpdateEndpoint,
    PostEndpoint
)
from api.endpoint.project import ProjectResourceListEndpoint
from db.models.ci import CI

_logger = logging.getLogger('polyaxon.views.ci')


class CIView(ProjectResourceListEndpoint,
             PostEndpoint,
             RetrieveEndpoint,
             UpdateEndpoint,
             DestroyEndpoint):
    """
    post:
        set a ci.
    get:
        Get a ci details.
    patch:
        Update a ci details.
    delete:
        Delete a ci.
    """
    queryset = CI.objects
    serializer_class = CISerializer

    def get_object(self):
        if self._object:
            return self._object
        self._object = get_object_or_404(CI, project=self.project)
        return self._object
