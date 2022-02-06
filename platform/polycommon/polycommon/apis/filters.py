#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend
from rest_framework.filters import OrderingFilter as BaseOrderingFilter

from django.core.exceptions import ImproperlyConfigured
from django.db.models import F
from django.db.models.fields.json import KeyTransform

from polyaxon.exceptions import PQLException
from polyaxon.utils.string_utils import strip_spaces
from polycommon import query


class QueryFilter(BaseFilterBackend):
    # The URL query parameter used for the ordering.
    query_param = "query"
    query_manager = None
    check_alive = False

    def get_check_alive(self, view):
        return getattr(view, "check_alive", self.check_alive)

    def get_query_param(self, view):
        return getattr(view, "query_param", self.query_param)

    def get_query_manager(self, view):
        query_manager = getattr(view, "query_manager", self.query_manager)
        if not query_manager:
            raise ImproperlyConfigured(
                "QueryFilter requires a query_manager to be set on the view."
            )
        return query_manager

    def process_alive(self, query_spec: str) -> str:
        if not query_spec:
            query_spec = "live_state:1"
        elif "live_state" not in query_spec:
            query_spec += ",live_state:1"

        return query_spec

    def filter_queryset(self, request, queryset, view):
        query_param = self.get_query_param(view=view)
        query_manager = self.get_query_manager(view=view)
        query_spec = request.query_params.get(query_param)
        check_alive = self.get_check_alive(view=view)
        if check_alive:
            query_spec = self.process_alive(query_spec=query_spec)

        if query_spec and query_manager:
            try:
                queryset = query.filter_queryset(
                    manager=query_manager, query_spec=query_spec, queryset=queryset
                )
            except PQLException as e:
                if getattr(view, "exception_class", False):
                    raise e
                else:
                    raise ValidationError(e)

        return queryset


class OrderingFilter(BaseOrderingFilter):
    ordering_param = "sort"
    ordering_proxy_fields = {}

    def remove_invalid_fields(self, queryset, fields, view, request):
        result_fields = []
        annotation = {}
        proxy_fields = getattr(view, "ordering_proxy_fields", {}) or {}
        valid_fields = [
            item[0]
            for item in self.get_valid_fields(queryset, view, {"request": request})
        ]

        for field in fields:
            negation = "-" if field[0] == "-" else ""
            field = field.lstrip("-")
            if field in valid_fields:
                if negation:
                    result_fields.append(F(field).desc(nulls_last=True))
                else:
                    result_fields.append(field)
                continue

            field, suffix = query.parse_field(field)
            if field in proxy_fields:
                _proxy = proxy_fields[field]
                if _proxy.get("annotate"):
                    if negation:
                        result_fields.append(F(suffix).desc(nulls_last=True))
                    else:
                        result_fields.append(suffix)
                    annotation[suffix] = KeyTransform(suffix, _proxy["field"])
                else:
                    if negation:
                        result_fields.append(F(_proxy["field"]).desc(nulls_last=True))
                    else:
                        result_fields.append(_proxy["field"])

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
            fields = strip_spaces(value=params, sep=",", join=False)
            ordering, annotations = self.remove_invalid_fields(
                queryset, fields, view, request
            )
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
