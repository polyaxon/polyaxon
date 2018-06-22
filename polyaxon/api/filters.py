from django.contrib.postgres.fields.jsonb import KeyTransform
from django.db.models.sql.constants import ORDER_PATTERN
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
    ordering_proxy_fields = {}

    def remove_invalid_fields(self, queryset, fields, view, request):
        result_fields = []
        annotation = {}
        proxy_fields = getattr(view, 'ordering_proxy_fields', {})
        valid_fields = [item[0] for item in
                        self.get_valid_fields(queryset, view, {'request': request})]

        for field in fields:
            if not ORDER_PATTERN.match(field):
                continue

            negation = '-' if field[0] == '-' else ''
            field = field.lstrip('-')
            if field in valid_fields:
                result_fields.append('{}{}'.format(negation, field))
                continue

            field, suffix = query.parse_field(field)
            if field in proxy_fields:
                result_fields.append('{}{}'.format(negation, suffix))
                annotation[suffix] = KeyTransform(suffix, proxy_fields[field])

        return result_fields, annotation

    def get_ordering(self, request, queryset, view):
        """
        Ordering is set by a comma delimited ?ordering=... query parameter.

        The `ordering` query parameter can be overridden by setting
        the `ordering_param` value on the OrderingFilter or by
        specifying an `ORDERING_PARAM` value in the API settings.
        """
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(',')]
            ordering, annotations = self.remove_invalid_fields(queryset, fields, view, request)
            if ordering:
                return ordering, annotations

        # No ordering was included, or all the ordering fields were invalid
        return self.get_default_ordering(view), None

    def filter_queryset(self, request, queryset, view):
        ordering, annotations = self.get_ordering(request, queryset, view)

        if ordering:
            if annotations:
                queryset = queryset.annotate(**annotations)
            return queryset.order_by(*ordering)

        return queryset
