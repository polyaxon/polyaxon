from rest_framework import mixins
from rest_framework.generics import GenericAPIView

import auditor


class BaseEndpoint(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   GenericAPIView,):
    AUDITOR_EVENT_TYPES = None
    CONTEXT_KEYS = ()
    QUERY_CONTEXT_KEYS = ()

    def get_object(self):
        instance = super().get_object()
        if not self.AUDITOR_EVENT_TYPES:
            return instance
        method = self.request.method.lower()
        event_type = self.AUDITOR_EVENT_TYPES.get(method)
        if method == 'get' and event_type:
            auditor.record(event_type=event_type,
                           instance=instance,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username)
        elif method == 'delete' and event_type:
            auditor.record(event_type=event_type,
                           instance=instance,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        if not self.AUDITOR_EVENT_TYPES:
            return instance
        event_type = self.AUDITOR_EVENT_TYPES.get('update')
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

    def initialize_context(self, request, *args, **kwargs):
        """
        Initializes the endpoint with the context keys based on the passed
        and/or based on the query parameters (request.GET).
        """
        for key in self.CONTEXT_KEYS:
            setattr(self, key, kwargs.get(key))
        for key in self.QUERY_CONTEXT_KEYS:
            setattr(self, key, request.query_params.get(key))
        self._validate_context()
        self._initialize_context()

    def dispatch(self, request, *args, **kwargs):
        self.initialize_context(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class PostEndpoint(object):
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


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
