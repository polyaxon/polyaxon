import auditor

from events.registry import superuser

auditor.subscribe(superuser.SuperUserRoleGrantedEvent)
auditor.subscribe(superuser.SuperUserRoleRevokedEvent)
