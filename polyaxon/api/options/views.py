import logging

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

import conf

from api.endpoint.admin import AdminListEndpoint
from api.endpoint.base import CreateEndpoint, ListEndpoint
from api.endpoint.owner import OwnerResourceEndpoint
from api.options.serializers import ConfigOptionSerializer
from conf.exceptions import ConfException  # pylint:disable=ungrouped-imports
from db.models.config_options import ConfigOption

_logger = logging.getLogger("polyaxon.views.jobs")


class ClusterConfigOptionsViewV1(AdminListEndpoint, ListEndpoint, CreateEndpoint):
    """
    get:
        List options for cluster
    post:
        Create options for cluster
    """
    queryset = ConfigOption.objects
    serializer_class = ConfigOptionSerializer

    def list(self, request, *args, **kwargs):
        keys = self.request.query_params.getlist('keys', None)
        if not keys:
            raise ValidationError('No keys passed.')
        try:
            results = [conf.get(key, to_dict=True) for key in keys]
        except ConfException as e:
            raise ValidationError(e)
        return Response(results, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if not self.request.data:
            raise ValidationError('Received no config options.')
        for key in self.request.data:
            value = self.request.data.get(key)
            try:
                if value is not None:
                    conf.set(key, value)
                else:
                    conf.delete(key)
            except ConfException as e:
                raise ValidationError(e)
        return Response(data={}, status=status.HTTP_200_OK)


class OwnerConfigOptionsViewV1(OwnerResourceEndpoint, ListEndpoint, CreateEndpoint):
    """
    get:
        List options for cluster
    post:
        Create options for cluster
    """
    queryset = ConfigOption.objects
    serializer_class = ConfigOptionSerializer

    def filter_queryset(self, queryset):
        keys = self.request.query_params.getlist('keys', None)
        if not keys:
            raise ValidationError('No keys passed.')
        queryset = queryset.filter(key__in=keys)
        return super().filter_queryset(queryset=queryset)

    def create(self, request, *args, **kwargs):
        if not self.request.data:
            raise ValidationError('Received no config options.')
        for key in self.request.data:
            value = self.request.data.get(key)
            try:
                if value:
                    conf.set(key, value)
                else:
                    conf.delete(key)
            except ConfException as e:
                raise ValidationError(e)
        return Response(data={}, status=status.HTTP_200_OK)
