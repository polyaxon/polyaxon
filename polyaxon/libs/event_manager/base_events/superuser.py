from libs.event_manager.event import Event

SUPERUSER_ROLE_GRANTED = 'superuser.role.granted'
SUPERUSER_ROLE_REVOKED = 'superuser.role.revoked'


class SuperUserRoleGrantedEvent(Event):
    type = SUPERUSER_ROLE_GRANTED


class SuperUserRoleRevokedEvent(Event):
    type = SUPERUSER_ROLE_REVOKED
