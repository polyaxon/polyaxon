import tracker

from events.registry import superuser

tracker.subscribe(superuser.SuperUserRoleGrantedEvent)
tracker.subscribe(superuser.SuperUserRoleRevokedEvent)
