import auditor
from libs.event_manager import event_types
from libs.event_manager.event import Event


class SuperUserRoleGrantedEvent(Event):
    type = event_types.SUPERUSER_ROLE_GRANTED


class SuperUserRoleRevokedEvent(Event):
    type = event_types.SUPERUSER_ROLE_REVOKED


auditor.register(SuperUserRoleGrantedEvent)
auditor.register(SuperUserRoleRevokedEvent)
