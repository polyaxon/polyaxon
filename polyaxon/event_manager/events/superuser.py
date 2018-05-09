from event_manager import event_subjects
from event_manager.event import Attribute, Event

SUPERUSER_ROLE_GRANTED = '{}.role.granted'.format(event_subjects.SUPER_USER)
SUPERUSER_ROLE_REVOKED = '{}.role.revoked'.format(event_subjects.SUPER_USER)


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
