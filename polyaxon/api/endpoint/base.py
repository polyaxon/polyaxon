from rest_framework import mixins
from rest_framework.generics import GenericAPIView

import auditor


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

    def get_serializer_class(self):
        if self.create_serializer_class and self.request.method == 'POST':
            return self.create_serializer_class
        return self.serializer_class

    def filter_queryset(self, queryset):
        queryset = self.enrich_queryset(queryset=queryset)
        return super().filter_queryset(queryset=queryset)

    def enrich_queryset(self, queryset):
        return queryset

    def get_object(self):
        instance = super().get_object()
        if not self.AUDITOR_EVENT_TYPES:
            return instance
        method = self.request.method
        event_type = self.AUDITOR_EVENT_TYPES.get(method)
        if method == 'GET' and event_type:
            auditor.record(event_type=event_type,
                           instance=instance,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username)
        elif method == 'DELETE' and event_type:
            auditor.record(event_type=event_type,
                           instance=instance,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        if not self.AUDITOR_EVENT_TYPES:
            return instance
        event_type = self.AUDITOR_EVENT_TYPES.get('UPDATE')
        if event_type:
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

    def validate_context(self):
        for key in self.CONTEXT_OBJECTS:
            assert hasattr(self, key)
        self._validate_context()

    def initialize_context(self, request, *args, **kwargs):
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

    def dispatch(self, request, *args, **kwargs):
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

            # Polyaxon's context initializer
            self.initialize_context(request, *args, **kwargs)

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


class CreateEndpoint(object):
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostEndpoint(object):
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        pass


class ListEndpoint(object):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveEndpoint(object):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DestroyEndpoint(object):
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UpdateEndpoint(object):
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
