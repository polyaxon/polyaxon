from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.serializers import Serializer

from django.http import HttpRequest, HttpResponse

import auditor

from scopes.authentication.utils import is_user


class BaseEndpoint(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   GenericAPIView):
    AUDITOR_EVENT_TYPES = None
    CONTEXT_KEYS = ()
    QUERY_CONTEXT_KEYS = ()
    CONTEXT_OBJECTS = ()
    create_serializer_class = None
    _object = None  # This is a memoization for get_object, to avoid accidentally calling twice.

    def get_serializer_class(self) -> Serializer:
        if self.create_serializer_class and self.request.method == 'POST':
            return self.create_serializer_class
        return self.serializer_class

    def filter_queryset(self, queryset):
        queryset = self.enrich_queryset(queryset=queryset)
        return super().filter_queryset(queryset=queryset)

    def enrich_queryset(self, queryset):
        return queryset

    def get_object(self):
        """We memoize the access to this function in case a second call is made."""
        if self._object:
            return self._object
        self._object = super().get_object()
        if not self.AUDITOR_EVENT_TYPES:
            return self._object
        method = self.request.method
        event_type = self.AUDITOR_EVENT_TYPES.get(method)
        if method == 'GET' and event_type and is_user(self.request.user):
            auditor.record(event_type=event_type,
                           instance=self._object,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username)
        elif method == 'DELETE' and event_type and is_user(self.request.user):
            auditor.record(event_type=event_type,
                           instance=self._object,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username)
        return self._object

    def perform_update(self, serializer: Serializer) -> None:
        instance = serializer.save()
        if not self.AUDITOR_EVENT_TYPES:
            return instance
        event_type = self.AUDITOR_EVENT_TYPES.get('UPDATE')
        if event_type and is_user(self.request.user):
            auditor.record(event_type=event_type,
                           instance=instance,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username)

    def _validate_context(self):
        """
        Validates that the context is correct.
        """
        pass

    def _initialize_context(self):
        """
        Initializes the objects needed for the endpoint and checks object base permissions.
        """
        pass

    def validate_context(self) -> None:
        for key in self.CONTEXT_OBJECTS:
            assert hasattr(self, key)
        self._validate_context()

    def initialize_context(self, request: HttpRequest, *args, **kwargs) -> None:
        """
        Initializes the endpoint with the context keys based on the passed
        and/or based on the query parameters (request.GET).
        """
        for key in self.CONTEXT_KEYS:
            setattr(self, key, kwargs.get(key))
        for key in self.QUERY_CONTEXT_KEYS:
            setattr(self, key, request.query_params.get(key))
        self._initialize_context()
        self.validate_context()

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        `.dispatch()` is pretty much the same as DRF's regular dispatch,
        but with extra logic to initialize a local context.
        Please check parent methods for more info.
        """
        #  pylint:disable=attribute-defined-outside-init
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            if handler != self.http_method_not_allowed:
                # Polyaxon's context initializer
                self.initialize_context(request, *args, **kwargs)

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


class CreateEndpoint(object):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.create(request, *args, **kwargs)


class PostEndpoint(object):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.create(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        pass


class ListEndpoint(object):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.list(request, *args, **kwargs)


class RetrieveEndpoint(object):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.retrieve(request, *args, **kwargs)


class DestroyEndpoint(object):
    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.destroy(request, *args, **kwargs)


class UpdateEndpoint(object):
    def put(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.update(request, *args, **kwargs)

    def patch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.partial_update(request, *args, **kwargs)
