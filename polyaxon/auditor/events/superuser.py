import auditor

from event_manager.events import superuser

auditor.subscribe(superuser.SuperUserRoleGrantedEvent)
auditor.subscribe(superuser.SuperUserRoleRevokedEvent)
