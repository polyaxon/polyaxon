import tracker

from event_manager.events import superuser

tracker.subscribe(superuser.SuperUserRoleGrantedEvent)
tracker.subscribe(superuser.SuperUserRoleRevokedEvent)
