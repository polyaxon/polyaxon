from event_manager.event import Event, Attribute

SUPERUSER_ROLE_GRANTED = 'superuser.role.granted'
SUPERUSER_ROLE_REVOKED = 'superuser.role.revoked'


class SuperUserRoleGrantedEvent(Event):
    type = SUPERUSER_ROLE_GRANTED
    attributes = (
        Attribute('user_uuid', is_uuid=True),
        Attribute('actor_uuid', is_uuid=True)
    )


class SuperUserRoleRevokedEvent(Event):
    type = SUPERUSER_ROLE_REVOKED
    attributes = (
        Attribute('user_uuid', is_uuid=True),
        Attribute('actor_uuid', is_uuid=True)
    )
