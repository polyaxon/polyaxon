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


class NoPageMixin:
    no_page_query_param = 'no_page'

    def paginate_queryset(self, queryset, request, view=None):
        try:
            no_page = to_bool(
                request.query_params.get(self.no_page_query_param),
                handle_none=True,
            )
            if no_page:
                return None
        except (KeyError, ValueError):
            pass

        return super().paginate_queryset(queryset, request, view)


class LargeLimitOffsetPagination(LimitOffsetPagination, NoPageMixin):
    default_limit = 1000


class PolyaxonPagination(LimitOffsetPagination, NoPageMixin):
    max_limit = 100
    default_limit = 20
