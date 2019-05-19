from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

SUPERUSER_ROLE_GRANTED = '{}.{}'.format(event_subjects.SUPERUSER, event_actions.GRANTED)
SUPERUSER_ROLE_REVOKED = '{}.{}'.format(event_subjects.SUPERUSER, event_actions.REVOKED)

EVENTS = {
    SUPERUSER_ROLE_GRANTED,
    SUPERUSER_ROLE_REVOKED,
}


class SuperUserRoleGrantedEvent(Event):
    event_type = SUPERUSER_ROLE_GRANTED
    actor = True
    attributes = (
        Attribute('id'),
    )


class SuperUserRoleRevokedEvent(Event):
    event_type = SUPERUSER_ROLE_REVOKED
    actor = True
    attributes = (
        Attribute('id'),
    )
