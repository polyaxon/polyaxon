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

from rest_framework.pagination import LimitOffsetPagination

from polyaxon.utils.bool_utils import to_bool


class PolyaxonBasePagination(LimitOffsetPagination):
    no_page_query_param = "no_page"

    def get_no_page(self, request):
        try:
            return to_bool(
                request.query_params.get(self.no_page_query_param),
                handle_none=True,
            )
        except (KeyError, ValueError):
            return False

    def get_count(self, queryset):
        if self.no_page:
            return None
        return super().get_count(queryset)

    def paginate_queryset(self, queryset, request, view=None):
        self.no_page = self.get_no_page(request)
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.count = self.get_count(queryset)
        self.offset = self.get_offset(request)
        self.request = request

        if self.no_page:
            return queryset[self.offset : self.offset + self.limit]

        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return queryset[self.offset : self.offset + self.limit]

    def get_next_link(self):
        if self.no_page:
            return None
        return super().get_next_link()

    def get_previous_link(self):
        if self.no_page:
            return None
        return super().get_previous_link()


class LargeLimitOffsetPagination(PolyaxonBasePagination):
    max_limit = None
    default_limit = 100


class PolyaxonPagination(PolyaxonBasePagination):
    max_limit = 100
    default_limit = 20
