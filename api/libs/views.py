from rest_framework import generics


class BaseNestingFilterMixin(object):
    """A mixin to optionally filter a queryset by uuid."""

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.

        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


class ListCreateAPIView(generics.ListCreateAPIView):
    create_serializer_class = None

    def get_serializer_class(self):
        if self.create_serializer_class and self.request.method.lower() == 'post':
            return self.create_serializer_class
        return self.serializer_class
