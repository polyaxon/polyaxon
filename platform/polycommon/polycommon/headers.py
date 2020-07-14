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

from django.http import HttpRequest

from polyaxon.services.headers import PolyaxonServiceHeaders

try:
    from rest_framework import HTTP_HEADER_ENCODING
except ImportError:
    raise ImportError("This module depends on django rest.")


POLYAXON_HEADERS_USER_ID = "X_POLYAXON_USER_ID"
POLYAXON_HEADERS_PUBLIC_ONLY = "X_POLYAXON_PUBLIC_ONLY"


def get_header(request: HttpRequest, header_service: str):
    """Return request's 'X_POLYAXON_...:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    service = request.META.get("HTTP_{}".format(header_service), b"")
    if isinstance(service, str):
        # Work around django test client oddness
        service = service.encode(HTTP_HEADER_ENCODING)
    return service


def get_service_header(request: HttpRequest):
    """Return request's 'X_POLYAXON_SERVICE:' header, as a bytestring."""
    return get_header(request=request, header_service=PolyaxonServiceHeaders.SERVICE)


def get_internal_header(request: HttpRequest) -> str:
    """
    Return request's 'X_POLYAXON_INTERNAL:' header, as a bytestring.
    """
    return get_header(request=request, header_service=PolyaxonServiceHeaders.INTERNAL)
