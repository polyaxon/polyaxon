import activitylogs

from event_manager.events import superuser

activitylogs.subscribe(superuser.SuperUserRoleGrantedEvent)
activitylogs.subscribe(superuser.SuperUserRoleRevokedEvent)
