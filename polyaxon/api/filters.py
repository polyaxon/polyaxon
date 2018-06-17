from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend
from rest_framework.filters import OrderingFilter as BaseOrderingFilter

from django.core.exceptions import ImproperlyConfigured

import query

from query.exceptions import QueryError


class QueryFilter(BaseFilterBackend):
    # The URL query parameter used for the ordering.
    query_param = 'query'
    query_manager = None

    def get_query_param(self, view):
        return getattr(view, 'query_param', self.query_param)

    def get_query_manager(self, view):
        query_manager = getattr(view, 'query_manager', self.query_manager)
        if not query_manager:
            raise ImproperlyConfigured('QueryFilter requires a query_manger to be set on the view.')
        return query_manager

    def filter_queryset(self, request, queryset, view):
        query_param = self.get_query_param(view=view)
        query_manager = self.get_query_manager(view=view)
        query_spec = request.query_params.get(query_param)
        if query_spec:
            try:
                queryset = query.filter_queryset(manager=query_manager,
                                                 query_spec=query_spec,
                                                 queryset=queryset)
            except QueryError as e:
                raise ValidationError(e)

        return queryset


class OrderingFilter(BaseOrderingFilter):
    ordering_param = 'sort'
