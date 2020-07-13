#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

from django.http import HttpResponse
from django.views.generic import View


class StatusView(View):
    status_code = 200

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=self.status_code)


class Handler404View(StatusView):
    status_code = 404


class Handler50xView(StatusView):
    status_code = 500


class Handler403View(StatusView):
    status_code = 403
