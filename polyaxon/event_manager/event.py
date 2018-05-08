from base64 import b64encode
from uuid import uuid1

from django.utils import timezone

from libs.date_utils import to_timestamp
from libs.json_utils import dumps_htmlsafe


class Attribute(object):
    def __init__(self, name, attr_type=str, is_datetime=False, is_uuid=False, is_required=True):
        self.name = name
        self.attr_type = attr_type
        self.is_datetime = is_datetime
        self.is_uuid = is_uuid
        self.is_required = is_required

    def extract(self, value):
        if value is None:
            return value
        if self.is_datetime:
            return to_timestamp(value)
        if self.is_uuid and not isinstance(value, str):
            return value.hex
        return self.attr_type(value)


class Event(object):
    __slots__ = ['uuid', 'attributes', 'data', 'datetime', 'event_type']

    event_type = None
    attributes = ()

    def __init__(self, event_type=None, datetime=None, **items):
        self.uuid = uuid1()

        self.datetime = datetime or timezone.now()
        if event_type is not None:
            self.event_type = event_type

        if self.event_type is None:
            raise ValueError('Event is missing type')

        data = {}
        for attr in self.attributes:
            nv = items.pop(attr.name, None)
            if attr.required and nv is None:
                raise ValueError('{} is required (cannot be None)'.format(
                    attr.name,
                ))
            data[attr.name] = attr.extract(nv)

        if items:
            raise ValueError('Unknown attributes: {}'.format(
                ', '.join(items.keys()),
            ))

        self.data = data

    @property
    def event_subject(self):
        """Return the first part of the event_type

        e.g.

        >>> Event.event_type = 'experiment.deleted'
        >>> Event.event_subject == 'experiment'
        """
        return self.event_type.split('.')[0]

    def serialize(self, dumps=True):
        data = {
            'uuid': b64encode(self.uuid.bytes),
            'timestamp': to_timestamp(self.datetime),
            'type': self.event_type,
            'data': self.data,
        }
        return dumps_htmlsafe(data) if dumps else data

    @classmethod
    def from_instance(cls, instance, **kwargs):
        values = {}
        for attr in cls.attributes:
            # TODO: add support for automatic dot props, e.g. 'user.id'
            values[attr.name] = kwargs.get(attr.name, getattr(instance, attr.name, None))
        return cls(**values)
