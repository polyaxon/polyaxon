import analytics
from event_manager.events import superuser

analytics.subscribe(superuser.SuperUserRoleGrantedEvent)
analytics.subscribe(superuser.SuperUserRoleRevokedEvent)
