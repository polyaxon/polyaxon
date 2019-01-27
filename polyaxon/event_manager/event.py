import copy

from typing import Any, Dict, Iterable, Mapping, Optional, Union
from uuid import UUID, uuid1

from hestia.date_utils import to_datetime, to_timestamp
from hestia.datetime_typing import AwareDT

from django.db.models import Model
from django.utils import timezone

from constants import user_system
from event_manager import event_context
from libs.json_utils import dumps_htmlsafe


class Attribute(object):
    def __init__(self,
                 name: str,
                 attr_type: Any = str,
                 is_datetime: bool = False,
                 is_uuid: bool = False,
                 is_required: bool = True) -> None:
        assert name != 'instance'
        self.name = name
        self.attr_type = attr_type
        self.is_datetime = is_datetime
        self.is_uuid = is_uuid
        self.is_required = is_required

    def extract(self, value: Any) -> Any:
        if value is None:
            return value
        if self.is_datetime:
            return to_timestamp(value)
        if self.is_uuid and not isinstance(value, str):
            return value.hex
        return self.attr_type(value)


class Event(object):
    __slots__ = [
        'uuid',
        'ref_id',
        'data',
        'datetime',
        'instance',
        'instance_id',
        'instance_contenttype'
    ]

    event_type = None  # The event type should ideally follow subject.action
    attributes = ()
    actor = False
    actor_id = 'actor_id'
    actor_name = 'actor_name'

    @classmethod
    def get_event_attributes(cls) -> Iterable['Attribute']:
        attributes = cls.attributes + (Attribute('ref_id', is_uuid=True, is_required=False),)
        if cls.actor:
            return attributes + (Attribute(cls.actor_id, attr_type=int),
                                 Attribute(cls.actor_name, is_required=False))
        return attributes

    def __init__(self,
                 uid: str = None,
                 datetime: AwareDT = None,
                 instance: Any = None,
                 instance_id: int = None,
                 instance_contenttype: str = None,
                 ref_id: str = None,
                 event_data: Mapping = None,
                 **items) -> None:
        self.uuid = UUID(uid) if uid else uuid1()
        self.datetime = datetime or timezone.now()
        self.instance = instance
        self.instance_id = instance_id
        self.instance_contenttype = instance_contenttype
        self.ref_id = None
        if ref_id:
            self.ref_id = UUID(ref_id) if isinstance(ref_id, str) else ref_id

        if self.event_type is None:
            raise ValueError('Event is missing a type')

        if event_data:
            self.data = event_data
        else:
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
    def get_event_subject(cls) -> Optional[str]:
        """Return the first part of the event_type

        e.g.

        >>> Event.event_type = 'experiment.deleted'
        >>> Event.get_event_subject() == 'experiment'
        """
        return event_context.get_event_subject(cls.event_type)

    @classmethod
    def get_event_action(cls) -> Optional[str]:
        """Return the second part of the event_type

        e.g.

        >>> Event.event_type = 'experiment.deleted'
        >>> Event.get_event_action() == 'deleted'
        """
        if not cls.actor:
            return None
        return event_context.get_event_action(cls.event_type)

    def serialize(self,
                  dumps: bool = False,
                  include_actor_name: bool = True,
                  include_instance_info: bool = False) -> Union[str, Dict]:
        _data = self.data
        if not include_actor_name and self.actor and self.actor_name in _data:
            _data = copy.deepcopy(self.data)
            _data.pop(self.actor_name)
        data = {
            'uuid': self.uuid.hex,
            'timestamp': to_timestamp(self.datetime),
            'type': self.event_type,
            'ref_id': self.ref_id.hex if self.ref_id else None,
            'data': _data,
        }
        if include_instance_info:
            data['instance_id'] = self.instance_id
            data['instance_contenttype'] = self.instance_contenttype
        return dumps_htmlsafe(data) if dumps else data

    @classmethod
    def get_value_from_instance(cls, attr: str, instance: Any) -> Any:
        # Handle dot notation
        path = attr.split('.')
        value = instance
        for i in path:
            value = getattr(value, i, None)
            if value is None:
                break

        return value

    @staticmethod
    def get_instance_info(instance: Any) -> Dict:
        if isinstance(instance, Model):
            from django.contrib.contenttypes.models import ContentType
            return {
                'instance_contenttype': ContentType.objects.get_for_model(instance).id,
                'instance_id': instance.id
            }
        return {}

    @classmethod
    def from_instance(cls, instance: Any, **kwargs) -> 'Event':
        values = {'instance': instance}
        if instance:
            values.update(cls.get_instance_info(instance))

        for attr in cls.get_event_attributes():
            # Convert dot notation
            value = kwargs.get(attr.name.replace('.', '_'))
            if value is None:
                value = cls.get_value_from_instance(attr=attr.name, instance=instance)
            values[attr.name] = value
        return cls(**values)

    @classmethod
    def from_event_data(cls, event_data: Mapping, **kwargs) -> 'Event':
        return cls(
            datetime=to_datetime(event_data.get('timestamp')),
            uid=event_data.get('uuid'),
            ref_id=event_data.get('ref_id'),
            event_data=event_data.get('data'),
            instance=event_data.get('instance'),
            instance_id=event_data.get('instance_id'),
            instance_contenttype=event_data.get('instance_contenttype'),
            **kwargs
        )
