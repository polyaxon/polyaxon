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

from functools import wraps

from django.utils.text import compress_string

try:
    import config
except ImportError:
    config = None


class GzipDecorator:
    """Gzip the response and set the respective header.
    """

    def __call__(self, func):
        @wraps(func)
        def inner(self, request, *args, **kwargs):
            response = func(self, request, *args, **kwargs)

            if (
                config
                and config.is_debug_mode
                and config.is_monolith_service
                and not config.is_testing_env
            ):
                return response

            # Before we can access response.content, the response needs to be rendered.
            response = self.finalize_response(request, response, *args, **kwargs)
            response.render()  # should be rendered, before picklining while storing to cache

            compressed_content = compress_string(response.content)

            # Ensure that the compressed content is actually smaller than the original.
            if len(compressed_content) >= len(response.content):
                return response

            # Replace content with gzipped variant, update respective headers.
            response.content = compressed_content
            response["Content-Length"] = str(len(response.content))
            response["Content-Encoding"] = "gzip"

            return response

        return inner


gzip = GzipDecorator
