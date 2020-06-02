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

from django.views.generic import TemplateView


class TemplateStatusView(TemplateView):
    status_code = 200

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=self.status_code)


class Handler404View(TemplateStatusView):
    template_name = "common/404.html"
    status_code = 404


class Handler50xView(TemplateStatusView):
    template_name = "common/50x.html"
    status_code = 500


class Handler403View(TemplateStatusView):
    template_name = "common/403.html"
    status_code = 403
