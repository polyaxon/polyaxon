from hestia.list_utils import to_list
from rest_framework import serializers

import conf

from scopes.authentication.utils import is_user


class IsDefaultSerializerMixin(serializers.Serializer):
    default_option = None

    is_default = serializers.SerializerMethodField()

    def get_is_default(self, obj):
        defaults = to_list(self.context.get('defaults', None), check_none=True)

        if defaults is not None:
            return obj.id in defaults
        else:
            # Get the requesting user if set in the context
            request = self.context.get('request', None)
            if request and is_user(request.user):
                defaults = to_list(conf.get(self.default_option))
                return obj.id in defaults
        return False
