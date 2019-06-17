from hestia.list_utils import to_list

import conf

from api.utils.serializers.is_default import IsDefaultSerializerMixin


class IsDefaultListMixinView(object):
    default_option = None

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if self.request.method.lower() == 'post':
            return super().get_serializer(*args, **kwargs)

        if not issubclass(serializer_class, IsDefaultSerializerMixin):
            return super().get_serializer(*args, **kwargs)

        queryset = args[0]

        if not queryset:
            return super().get_serializer(*args, **kwargs)

        defaults = to_list(conf.get(self.default_option), check_none=True)

        context = self.get_serializer_context()
        context['defaults'] = defaults
        kwargs['context'] = context
        return serializer_class(*args, **kwargs)
