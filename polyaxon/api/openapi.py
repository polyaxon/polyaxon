import warnings

from rest_framework import exceptions, serializers
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.schemas.utils import is_list_view


class PolyaxonOpenAPISchema(AutoSchema):
    def _get_operation_id(self, path, method):
        """
        Compute an operation ID from the model, serializer or view name.
        This subclass removes the check on serializers.
        """
        method_name = getattr(self.view, 'action', method.lower())
        if is_list_view(path, method, self.view):
            action = 'List'
        elif method_name not in self.method_mapping:
            action = method_name
        else:
            action = self.method_mapping[method.lower()]

        # Try to deduce the ID from the view's model
        model = getattr(getattr(self.view, 'queryset', None), 'model', None)
        if model is not None:
            name = model.__name__

        # Fallback to the view name
        else:
            name = self.view.__class__.__name__
            if name.endswith('APIView'):
                name = name[:-7]
            elif name.endswith('View'):
                name = name[:-4]
            if name.endswith(action):  # ListView, UpdateAPIView, ThingDelete ...
                name = name[:-len(action)]

        if action == 'List' and not name.endswith('s'):  # ListThings instead of ListThing
            name += 's'

        return action + name

    @staticmethod
    def _is_non_serializable_endpoint(view):
        """Add check for instances of PostEndpoint, PostAPIView"""
        return hasattr(view, 'no_serializer') and view.no_serializer

    def _get_request_body(self, path, method):
        view = self.view

        if method not in ('PUT', 'PATCH', 'POST'):
            return {}

        # Add check for instances of PostEndpoint, PostAPIView
        if self._is_non_serializable_endpoint(view):
            return {}

        if not hasattr(view, 'get_serializer'):
            return {}

        try:
            serializer = view.get_serializer()
        except exceptions.APIException:
            serializer = None
            warnings.warn('{}.get_serializer() raised an exception during '
                          'schema generation. Serializer fields will not be '
                          'generated for {} {}.'
                          .format(view.__class__.__name__, method, path))

        if not isinstance(serializer, serializers.Serializer):
            return {}

        content = self._map_serializer(serializer)
        # No required fields for PATCH
        if method == 'PATCH':
            del content['required']
        # No read_only fields for request.
        for name, schema in content['properties'].copy().items():
            if 'readOnly' in schema:
                del content['properties'][name]

        return {
            'content': {
                ct: {'schema': content}
                for ct in self.content_types
            }
        }

    def _get_responses(self, path, method):
        # TODO: Handle multiple codes.
        content = {}
        view = self.view
        if hasattr(view, 'get_serializer') and not self._is_non_serializable_endpoint(view):
            try:
                serializer = view.get_serializer()
            except exceptions.APIException:
                serializer = None
                warnings.warn('{}.get_serializer() raised an exception during '
                              'schema generation. Serializer fields will not be '
                              'generated for {} {}.'
                              .format(view.__class__.__name__, method, path))

            if isinstance(serializer, serializers.Serializer):
                content = self._map_serializer(serializer)
                # No write_only fields for response.
                for name, schema in content['properties'].copy().items():
                    if 'writeOnly' in schema:
                        del content['properties'][name]
                        content['required'] = [f for f in content['required'] if f != name]

        return {
            '200': {
                'content': {
                    ct: {'schema': content}
                    for ct in self.content_types
                }
            }
        }
