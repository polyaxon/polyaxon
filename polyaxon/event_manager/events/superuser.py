from event_manager import event_subjects, event_actions
from event_manager.event import Attribute, Event

SUPERUSER_ROLE_GRANTED = '{}.{}'.format(event_subjects.SUPERUSER, event_actions.GRANTED)
SUPERUSER_ROLE_REVOKED = '{}.{}'.format(event_subjects.SUPERUSER, event_actions.REVOKED)


class SuperUserRoleGrantedEvent(Event):
    event_type = SUPERUSER_ROLE_GRANTED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('actor_id')
    )


class SuperUserRoleRevokedEvent(Event):
    event_type = SUPERUSER_ROLE_REVOKED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('actor_id')
    )
