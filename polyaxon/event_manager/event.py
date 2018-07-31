import copy

from uuid import uuid1

from django.utils import timezone

from constants import user_system
from event_manager import event_context
from libs.date_utils import to_timestamp
from libs.json_utils import dumps_htmlsafe


class Attribute(object):
    def __init__(self, name, attr_type=str, is_datetime=False, is_uuid=False, is_required=True):
        assert name != 'instance'
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
    __slots__ = ['uuid', 'data', 'datetime', 'instance']

    event_type = None  # The event type should ideally follow subject.action
    attributes = ()
    actor = False
    actor_id = 'actor_id'
    actor_name = 'actor_name'

    @classmethod
    def get_event_attributes(cls):
        if cls.actor:
            return cls.attributes + (Attribute(cls.actor_id, attr_type=int),
                                     Attribute(cls.actor_name, is_required=False))
        return cls.attributes

    def __init__(self, datetime=None, instance=None, **items):
        self.uuid = uuid1()
        self.datetime = datetime or timezone.now()
        self.instance = instance

        if self.event_type is None:
            raise ValueError('Event is missing a type')

        data = {}
        for attr in self.get_event_attributes():
            # Check plain attr name
            item_value = items.pop(attr.name, None)
            if item_value is None:
                # Convert dot notation
                item_value = items.pop(attr.name.replace('.', '_'), None)

            if attr.is_required and item_value is None:
                raise ValueError('{} is required (cannot be None)'.format(
                    attr.name,
                ))
            data[attr.name] = attr.extract(item_value)

        actor_id = data.get(self.actor_id)
        actor_name = data.get(self.actor_name)
        if self.actor and actor_id is None:
            raise ValueError('Event {} requires an attribute specifying the actor_id'.format(
                self.event_type
            ))
        if self.actor and (actor_id != user_system.USER_SYSTEM_ID and actor_name is None):
            raise ValueError('Event {} requires an attribute specifying the actor_name'.format(
                self.event_type
            ))
        if self.actor and (actor_id == user_system.USER_SYSTEM_ID and actor_name is None):
            data[self.actor_name] = user_system.USER_SYSTEM_NAME

        if items:
            raise ValueError('Unknown attributes: {}'.format(
                ', '.join(items.keys()),
            ))

        self.data = data

    @classmethod
    def get_event_subject(cls):
        """Return the first part of the event_type

        e.g.

        >>> Event.event_type = 'experiment.deleted'
        >>> Event.get_event_subject() == 'experiment'
        """
        return event_context.get_event_subject(cls.event_type)

    @classmethod
    def get_event_action(cls):
        """Return the second part of the event_type

        e.g.

        >>> Event.event_type = 'experiment.deleted'
        >>> Event.get_event_action() == 'deleted'
        """
        if not cls.actor:
            return None
        return event_context.get_event_action(cls.event_type)

    def serialize(self, dumps=False, include_actor_name=True):
        _data = self.data
        if not include_actor_name and self.actor and self.actor_name in _data:
            _data = copy.deepcopy(self.data)
            _data.pop(self.actor_name)
        data = {
            'uuid': self.uuid.hex,
            'timestamp': to_timestamp(self.datetime),
            'type': self.event_type,
            'data': _data,
        }
        return dumps_htmlsafe(data) if dumps else data

    @classmethod
    def get_value_from_instance(cls, attr, instance):
        # Handle dot notation
        path = attr.split('.')
        value = instance
        for i in path:
            value = getattr(value, i, None)
            if value is None:
                break

        return value

    @classmethod
    def from_instance(cls, instance, **kwargs):
        values = {'instance': instance}
        for attr in cls.get_event_attributes():
            # Convert dot notation
            value = kwargs.get(attr.name.replace('.', '_'))
            if value is None:
                value = cls.get_value_from_instance(attr=attr.name, instance=instance)
            values[attr.name] = value
        return cls(**values)
