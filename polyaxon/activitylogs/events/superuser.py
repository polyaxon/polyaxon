import activitylogs

from events.registry import superuser

activitylogs.subscribe(superuser.SuperUserRoleGrantedEvent)
activitylogs.subscribe(superuser.SuperUserRoleRevokedEvent)
