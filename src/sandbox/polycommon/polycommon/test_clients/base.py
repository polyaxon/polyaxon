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

import datetime
import json
import uuid

from collections.abc import Mapping
from urllib.parse import urlparse

from django.test import Client
from django.test.client import FakePayload

CONTENT_TYPE_APPLICATION_JSON = "application/json"


class BaseClient(Client):
    """Base client class."""

    def do_request(
        self,
        method,
        path,
        data=None,
        content_type=CONTENT_TYPE_APPLICATION_JSON,
        **extra
    ):
        if data is None:
            data = {}

        def validate_data(dvalues):
            if not isinstance(dvalues, Mapping):
                return
            for key, value in dvalues.items():
                # Fix UUIDs for convenience
                if isinstance(value, uuid.UUID):
                    dvalues[key] = value.hex

                # Fix datetimes
                if isinstance(value, datetime.datetime):
                    dvalues[key] = value.strftime("%Y-%m-%d %H:%M")

        if isinstance(data, list):
            for d in data:
                validate_data(d)
        else:
            validate_data(data)

        if content_type == CONTENT_TYPE_APPLICATION_JSON:
            data = json.dumps(data)

        request = self.encode_data(method, path, data, content_type, **extra)
        return self.request(**request)

    def put(self, path, data=None, content_type=CONTENT_TYPE_APPLICATION_JSON, **extra):
        """Construct a PUT request."""
        return self.do_request("PUT", path, data, content_type, **extra)

    def patch(
        self, path, data=None, content_type=CONTENT_TYPE_APPLICATION_JSON, **extra
    ):
        """Construct a PATCH request."""
        return self.do_request("PATCH", path, data, content_type, **extra)

    def post(
        self, path, data=None, content_type=CONTENT_TYPE_APPLICATION_JSON, **extra
    ):
        """Construct a PATCH request."""
        return self.do_request("POST", path, data, content_type, **extra)

    def delete(
        self, path, data=None, content_type=CONTENT_TYPE_APPLICATION_JSON, **extra
    ):
        """Construct a DELETE request."""
        return self.do_request("DELETE", path, data, content_type, **extra)

    def encode_data(self, http_method, path, data, content_type, **extra):
        patch_data = self._encode_data(data, content_type)

        parsed = urlparse(path)
        request = {
            "CONTENT_LENGTH": len(patch_data),
            "CONTENT_TYPE": content_type,
            "PATH_INFO": self._get_path(parsed),
            "QUERY_STRING": parsed[4],
            "REQUEST_METHOD": http_method,
            "wsgi.input": FakePayload(patch_data),
        }
        request.update(extra)

        return request
