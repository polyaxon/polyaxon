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
from rest_framework.generics import GenericAPIView

from django.http import HttpRequest, HttpResponse

from polycommon import auditor
from polycommon.apis.gzip import gzip
from polycommon.apis.regex import OWNER_NAME_KEY, PROJECT_NAME_KEY, UUID_KEY
from polycommon.endpoints import mixins
from polycommon.endpoints.exceptions import EndpointError


class BaseEndpoint(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericAPIView,
):
    serializer_class_mapping = None

    AUDITOR_EVENT_TYPES = None
    AUDIT_OWNER = False
    AUDIT_PROJECT = False
    AUDIT_PROJECT_RESOURCES = False
    AUDIT_INSTANCE = False
    AUDIT_EXTRA_KEYS = ()

    PROJECT_NAME_KEY = PROJECT_NAME_KEY
    PROJECT_OWNER_NAME_KEY = OWNER_NAME_KEY
    PROJECT_RESOURCE_KEY = None

    CONTEXT_KEYS = ()
    QUERY_CONTEXT_KEYS = ()
    CONTEXT_OBJECTS = ()

    # This is a memoization for get_object, to avoid accidentally calling twice.
    _object = None
    _instance_id = None
    _instance_uuid = None
    _owner_id = None

    def set_owner(self):
        pass

    def get_object(self):
        """We memoize the access to this function in case a second call is made."""
        if self._object:
            return self._object
        self._object = super().get_object()
        return self._object

    def filter_queryset(self, queryset):
        queryset = self.enrich_queryset(queryset=queryset)
        return super().filter_queryset(queryset=queryset)

    def enrich_queryset(self, queryset):
        return queryset

    def check_request(self, request: HttpRequest):
        pass

    def initialize_context(self, request: HttpRequest, *args, **kwargs) -> None:
        """
        Initializes the endpoint with the context keys based on the passed
        and/or based on the query parameters (request.GET).
        """
        self.check_request(request)

        for key in self.CONTEXT_KEYS:
            if key not in kwargs:
                raise EndpointError(
                    f"Endpoint `{self.__class__.__name__}` requires a context key {key}, "
                    f"but it was not found."
                )
            setattr(self, key, kwargs.get(key))
        for key in self.QUERY_CONTEXT_KEYS:
            setattr(self, key, request.query_params.get(key))

        if self.AUDIT_OWNER:
            assert OWNER_NAME_KEY in kwargs
        if self.AUDIT_PROJECT:
            assert PROJECT_NAME_KEY in kwargs
        if self.AUDIT_PROJECT_RESOURCES:
            assert self.PROJECT_RESOURCE_KEY is not None
            assert self.PROJECT_RESOURCE_KEY in kwargs

    def initialize_object_context(self, request: HttpRequest, *args, **kwargs) -> None:
        pass

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.initialize_context(request, *args, **kwargs)
        self.initialize_object_context(request, *args, **kwargs)

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        request.access = None
        return request

    def get_audit_params(self, **kwargs):
        params = {}
        if self.AUDIT_OWNER:
            params[self.PROJECT_OWNER_NAME_KEY] = kwargs.get(OWNER_NAME_KEY)
        if self.AUDIT_PROJECT:
            params[self.PROJECT_NAME_KEY] = kwargs.get(PROJECT_NAME_KEY)
        if self.AUDIT_PROJECT_RESOURCES:
            params[UUID_KEY] = kwargs.get(self.PROJECT_RESOURCE_KEY)
        if self.AUDIT_INSTANCE:
            params["instance"] = self._object
        for extra_key in self.AUDIT_EXTRA_KEYS:
            params[extra_key] = kwargs.get(extra_key)
        return params

    def audit(self, request, *args, **kwargs):
        if not self.AUDITOR_EVENT_TYPES:
            return
        event_type = self.AUDITOR_EVENT_TYPES.get(request.method)
        if event_type:
            self.set_owner()
            params = self.get_audit_params(**kwargs)
            auditor.record(
                event_type=event_type,
                actor_id=1,
                actor_name="polyaxon",
                owner_id=self._owner_id,
                **params,
            )

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        assert (
            self.serializer_class is not None
            or self.serializer_class_mapping is not None
        ), (
            "'%s' should either include a `serializer_class` attribute or "
            "a `serializer_class_mapping` attribute, "
            "or override the `get_serializer_class()` method." % self.__class__.__name__
        )

        if self.serializer_class_mapping:
            return self.serializer_class_mapping[self.request.method]
        return self.serializer_class


class CreateEndpoint:
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.create(request, *args, **kwargs)


class PostEndpoint:
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.create(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        pass


class ListEndpoint:
    @gzip()
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.list(request, *args, **kwargs)


class RetrieveEndpoint:
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.retrieve(request, *args, **kwargs)


class DestroyEndpoint:
    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.destroy(request, *args, **kwargs)


class UpdateEndpoint:
    def put(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.update(request, *args, **kwargs)

    def patch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.partial_update(request, *args, **kwargs)
