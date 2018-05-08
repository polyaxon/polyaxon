import auditor
from event_manager.events import superuser

auditor.register(superuser.SuperUserRoleGrantedEvent)
auditor.register(superuser.SuperUserRoleRevokedEvent)
